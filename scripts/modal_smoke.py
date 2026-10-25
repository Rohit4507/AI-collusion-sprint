"""One paid Modal GPU invocation, only when explicitly run on an authenticated machine.

Install requirements-modal.txt, then:
  modal run scripts/modal_smoke.py --output outputs/modal-smoke-001.json
No credentials should be supplied in arguments or saved in this repository.
"""

from __future__ import annotations

import json
from pathlib import Path

import modal

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
PROMPTS = (
    ("Return only one digit: 0 if 2 + 2 = 4, otherwise 1.", "0"),
    ("Return only one digit: 1 if 3 + 3 = 6, otherwise 0.", "1"),
    ("Return only one digit: 0 if 5 is less than 9, otherwise 1.", "0"),
    ("Return only one digit: 1 if 8 is greater than 2, otherwise 0.", "1"),
)

app = modal.App("collusion-infrastructure-smoke")
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "torch==2.8.0",
    "transformers==4.57.1",
    "huggingface-hub==0.36.0",
    "accelerate==1.11.0",
)


@app.function(
    image=image,
    gpu="T4",
    timeout=600,
    retries=0,
    max_containers=1,
    scaledown_window=2,
)
def smoke(revision: str) -> dict:
    import importlib.metadata
    import time

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    started = time.perf_counter()
    if not revision or len(revision) != 40:
        raise ValueError("Expected resolved 40-character Hugging Face model commit")
    if not torch.cuda.is_available():
        raise RuntimeError("GPU unavailable: stop rather than silently change hardware")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL, revision=revision, trust_remote_code=False
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL,
        revision=revision,
        trust_remote_code=False,
        torch_dtype=torch.float16,
    ).to("cuda")
    model.eval()
    load_seconds = time.perf_counter() - started
    records = []
    for prompt, expected in PROMPTS:
        rendered = tokenizer.apply_chat_template(
            [
                {"role": "system", "content": "Follow the requested output format exactly."},
                {"role": "user", "content": prompt},
            ],
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tokenizer(rendered, return_tensors="pt").to("cuda")
        torch.cuda.synchronize()
        before = time.perf_counter()
        with torch.inference_mode():
            tokens = model.generate(
                **inputs,
                do_sample=False,
                max_new_tokens=8,
                pad_token_id=tokenizer.eos_token_id,
            )
        torch.cuda.synchronize()
        suffix = tokens[0, inputs["input_ids"].shape[1] :]
        raw = tokenizer.decode(suffix, skip_special_tokens=True)
        parsed = raw.strip() if raw.strip() in {"0", "1"} else None
        records.append(
            {
                "prompt": prompt,
                "expected": expected,
                "raw_output": raw,
                "parsed": parsed,
                "correct": parsed == expected,
                "new_tokens": len(suffix),
                "generation_seconds": time.perf_counter() - before,
            }
        )
    return {
        "scope": "infrastructure control only; no behavioral or collusion claim",
        "model": MODEL,
        "revision": revision,
        "gpu": torch.cuda.get_device_name(0),
        "load_seconds": load_seconds,
        "total_remote_seconds": time.perf_counter() - started,
        "versions": {
            package: importlib.metadata.version(package)
            for package in ("torch", "transformers", "huggingface-hub", "accelerate")
        },
        "records": records,
        "gate_passed": all(row["correct"] for row in records),
        "billing_verified": False,
    }


@app.local_entrypoint()
def main(output: str = "outputs/modal-smoke-001.json"):
    from huggingface_hub import HfApi

    destination = Path(output).expanduser()
    if destination.exists():
        raise FileExistsError("Use a fresh output file; no remote call started")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Resolve before allocating the paid GPU; record the immutable snapshot.
    revision = HfApi().model_info(MODEL).sha
    if revision is None or len(revision) != 40:
        raise ValueError("Could not resolve model revision; no GPU call started")
    manifest = destination.with_suffix(".request.json")
    with manifest.open("x", encoding="utf-8") as stream:
        json.dump({"model": MODEL, "revision": revision, "scope": "smoke"}, stream, indent=2)
    print("Starting ONE paid GPU invocation. Timeout is not a dollar spending cap.")
    result = smoke.remote(revision)
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(f"Saved {destination}; correctness gate={result['gate_passed']}")
    print("Check Modal actual charges and container shutdown before any further run.")
