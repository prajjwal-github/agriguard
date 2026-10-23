# Scientific Evaluation Report: apple (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:41:23.539785+00:00  
**Test Set Samples:** 27  

## Summary Performance
- **Overall Accuracy:** 77.78%
- **Macro Precision:** 86.67%
- **Macro Recall:** 77.78%
- **Macro F1-Score:** 0.7833
- **Weighted F1-Score:** 0.7833
- **Inference Latency (Avg):** 5.17 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `healthy` | 60.0% | 100.0% | 0.7500 | 9.0 |
| `minor_blemish` | 100.0% | 66.7% | 0.8000 | 9.0 |
| `rot_decay` | 100.0% | 66.7% | 0.8000 | 9.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['healthy', 'minor_blemish', 'rot_decay']

```text
     9     0     0
     3     6     0
     3     0     6
```