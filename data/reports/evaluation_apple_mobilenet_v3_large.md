# Scientific Evaluation Report: apple (mobilenet_v3_large)
**Evaluation Date:** 2026-10-23T14:33:33.970870+00:00  
**Test Set Samples:** 27  

## Summary Performance
- **Overall Accuracy:** 88.89%
- **Macro Precision:** 91.67%
- **Macro Recall:** 88.89%
- **Macro F1-Score:** 0.8857
- **Weighted F1-Score:** 0.8857
- **Inference Latency (Avg):** 11.25 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `healthy` | 75.0% | 100.0% | 0.8571 | 9.0 |
| `minor_blemish` | 100.0% | 66.7% | 0.8000 | 9.0 |
| `rot_decay` | 100.0% | 100.0% | 1.0000 | 9.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['healthy', 'minor_blemish', 'rot_decay']

```text
     9     0     0
     3     6     0
     0     0     9
```