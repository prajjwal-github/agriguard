# Scientific Evaluation Report: orange (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:19:20.023415+00:00  
**Test Set Samples:** 18  

## Summary Performance
- **Overall Accuracy:** 94.44%
- **Macro Precision:** 95.24%
- **Macro Recall:** 94.44%
- **Macro F1-Score:** 0.9441
- **Weighted F1-Score:** 0.9441
- **Inference Latency (Avg):** 15.07 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `healthy` | 100.0% | 83.3% | 0.9091 | 6.0 |
| `minor_blemish` | 100.0% | 100.0% | 1.0000 | 6.0 |
| `rot_decay` | 85.7% | 100.0% | 0.9231 | 6.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['healthy', 'minor_blemish', 'rot_decay']

```text
     5     0     1
     0     6     0
     0     0     6
```