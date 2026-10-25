# Open-weight extension: infrastructure gate

Date: 2026-10-25. Internal exploratory plan, recorded after observing synthetic results. Not a preregistration or replacement for the failed primary experiment.

## Gate 1: smoke test only

- [Future work] Load Qwen/Qwen2.5-0.5B-Instruct on one Modal T4, resolve and record the exact model commit before GPU execution, and run four trivial binary-output prompts.
- [Hypothesis] This small model is adequate to validate infrastructure, not necessarily adequate for an interesting behavioral study. Do not upgrade models based on attractive final outcomes.
- [Future work] Use greedy decoding, at most eight new tokens per prompt, one container and one invocation; function timeout 600 seconds, no automatic retries, scaledown window 2 seconds. Modal image construction and model download can incur additional time/charges; timeout is not a dollar cap.
- [Future work] Save model revision, dependency versions, prompts, complete generated suffixes, strict parsing status, GPU name, load/generation timings and protocol designation. Refuse overwriting local artifacts. Do not log credentials.
- [Future work] Inspect actual Modal usage after one invocation. Keep a $5 pilot spending target, but do not claim programmatic dollar enforcement. Stop app/containers in dashboard if unexpected activity appears. Do not batch jobs or enable a web endpoint.
- [Not verified] Account credit, GPU availability, actual price, model access, exact remote dependency compatibility and paid execution are not verified by this repository change. User authentication on their own machine is not authentication inside the Arena sandbox.

## Go/no-go

- [Future work] Proceed only if exact revision is recorded, GPU load succeeds, all four expected binary answers parse and match, logs save, container scales down, and actual cost is acceptable. If parsing fails, investigate on development prompts only; do not report a behavioral result.
- [Statistical interpretation] Four arithmetic answers are an infrastructure control, not evidence of reasoning quality, independence, collusion, causal influence or generalization.

## Gate 2: separate behavioral protocol, not implemented here

- [Future work] Before any behavioral generation, freeze task instances, sample size, prompts, primary estimand, task-group split, independent RNG strategy, failure policy and calibration/test boundaries. Compare no peer, legitimate evidence, incorrect peer advice, and talk-only conditions on matched objectively scored tasks. Verify no indirect peer information in independent controls.
- [Future work] Label this scripted peer-advice influence, not emergent collusion. Keep explicit agreement, influence, task error and structural channel labels separate. Preserve synthetic main and exploratory extension results regardless of outcomes.
- [Future work] Use pilot-only tasks to resolve model/prompt feasibility, freeze final settings, then generate untouched task groups. Do not continue to expensive runs merely because GPU credits remain.
