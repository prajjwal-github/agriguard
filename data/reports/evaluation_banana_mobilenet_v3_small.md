# Scientific Evaluation Report: banana (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:18:41.450892+00:00  
**Test Set Samples:** 18  

## Summary Performance
- **Overall Accuracy:** 100.00%
- **Macro Precision:** 100.00%
- **Macro Recall:** 100.00%
- **Macro F1-Score:** 1.0000
- **Weighted F1-Score:** 1.0000
- **Inference Latency (Avg):** 13.1 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `healthy` | 100.0% | 100.0% | 1.0000 | 6.0 |
| `minor_blemish` | 100.0% | 100.0% | 1.0000 | 6.0 |
| `rot_decay` | 100.0% | 100.0% | 1.0000 | 6.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['healthy', 'minor_blemish', 'rot_decay']

```text
     6     0     0
     0     6     0
     0     0     6
```