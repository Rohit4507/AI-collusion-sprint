# Results and claim verification — 2026-10-25

## Execution evidence

- [Experimental observation] Reinstalled locked dependencies in a fresh .venv; all 39 tests passed. Reran both main and extension configs without tuning.

## observability-v1

- [Experimental observation] All deterministic artifacts match exactly; summary matches excluding runtime. Independently recomputed confusion counts, precision/recall/F1/FPR, AP, ROC-AUC, available Brier scores, thresholds, per-condition counts and primary paired bootstrap from saved predictions.
- [Experimental observation] Primary contrast: {'contrast': 'CMI minus MI FPR on common-cause negatives', 'difference': 0.07, 'ci95': [0.048, 0.092], 'channel_recall': 1.0, 'criterion_met': False}.

## observability-extension

- [Experimental observation] All deterministic artifacts match exactly; summary matches excluding runtime. Independently recomputed confusion counts, precision/recall/F1/FPR, AP, ROC-AUC, available Brier scores, thresholds, per-condition counts and primary paired bootstrap from saved predictions.
- [Experimental observation] Primary contrast: {'contrast': 'CMI minus MI FPR on common-cause negatives', 'difference': -0.05, 'ci95': [-0.09405, -0.007950000000000046], 'channel_recall': 1.0, 'criterion_met': True}.

## Verified main results

| Method | TP / 1500 | FP / 2500 | Precision | Recall | FPR | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| action_classifier | 1000 | 500 | 0.667 | 0.667 | 0.200 | 0.865 |
| combined_classifier | 1000 | 500 | 0.667 | 0.667 | 0.200 | 0.865 |
| agreement | 1000 | 500 | 0.667 | 0.667 | 0.200 | 0.866 |
| mi | 1000 | 500 | 0.667 | 0.667 | 0.200 | 0.868 |
| cmi | 1000 | 1095 | 0.477 | 0.667 | 0.438 | 0.566 |
| keyword | 0 | 500 | 0.000 | 0.000 | 0.200 | 0.400 |
| prevalence | 0 | 0 | 0.000 | 0.000 | 0.000 | 0.500 |

## Claim boundaries and audit findings

- [Verified fact — code inspection] Models exclude mechanism/seed/split IDs from features. Scaling and logistic regression fit training rows only; thresholds use calibration rows only. However run() generates all rows before fitting: absence of test use is verified from code flow, not an enforced sealed-test boundary.
- [Statistical interpretation] The main hypothesis fails: CMI has more common-cause false positives. Equal overall recall does not imply matched per-mechanism sensitivity; MI misses stochastic channels while CMI misses deterministic channels.
- [Verified fact — code inspection] Calibration conditions common and talk have identical action trajectories within each block. They are not independent calibration samples. This duplicates their weight in the calibration mixture; nominal 10% calibration FPR is a mixture operating point, not a per-condition or held-out guarantee.
- [Verified fact — protocol comparison] The protocol mentions a randomized-score reference, TF-IDF alternative, block-aware null calibration and wider robustness options. The implementation supplies none of those: keyword is the only message-only method, empirical quantile calibration is used (not permutation/null-test calibration), and no random-score reference is reported. These are implementation omissions, not completed ablations.
- [Statistical interpretation] Only a parameter shift (.1 to .25) was tested, not unseen environment/scenario-family generalization. All mechanism types appear in training. The extension is exploratory and cannot rescue the confirmatory failure.
- [Statistical interpretation] Observational-equivalence is distributional by construction, not a guarantee that finite-sample empirical histograms are equal. The channel label is structural script provenance, not intention or harm.
- [Verified fact — code inspection] Intervention statistic changes B to an independent fair bit only for known positive labels and leaves negatives unchanged. It is label-aware construction machinery, not an independently validated blind causal detector. No intervention-performance claim is justified.
- [Not verified] No real-LLM results, causal mechanism identification from natural traces, low-FPR deployment guarantee, benchmark superiority, full baseline uncertainty, new-seed robustness, class-prevalence sweep, realistic message noise, or human-independent verification.
- [Verified fact — audit scope] This numerical audit does not verify historical ordering of design freezes or whether prior external sources are accurate. Earlier conversation claimed PR #5 merged without showing merge evidence; no merge-status claim is made here.

## Conclusion

[Statistical interpretation] The saved numerical claims reproduce and the primary result is genuinely negative. Defensible claim: this small scripted artifact demonstrates specific calibration and observability failures. It does not establish a successful general collusion detector or full completion of the original research plan.
