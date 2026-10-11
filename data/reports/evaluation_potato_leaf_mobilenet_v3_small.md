# Scientific Evaluation Report: potato_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:39:11.079158+00:00  
**Test Set Samples:** 33  

## Summary Performance
- **Overall Accuracy:** 75.76%
- **Macro Precision:** 81.25%
- **Macro Recall:** 75.76%
- **Macro F1-Score:** 0.7408
- **Weighted F1-Score:** 0.7408
- **Inference Latency (Avg):** 13.48 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `early_blight` | 100.0% | 45.5% | 0.6250 | 11.0 |
| `healthy` | 68.8% | 100.0% | 0.8148 | 11.0 |
| `late_blight` | 75.0% | 81.8% | 0.7826 | 11.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['early_blight', 'healthy', 'late_blight']

```text
     5     3     3
     0    11     0
     0     2     9
```