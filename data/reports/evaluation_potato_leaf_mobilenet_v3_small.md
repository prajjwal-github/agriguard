# Scientific Evaluation Report: potato_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:21:06.305283+00:00  
**Test Set Samples:** 33  

## Summary Performance
- **Overall Accuracy:** 93.94%
- **Macro Precision:** 94.87%
- **Macro Recall:** 93.94%
- **Macro F1-Score:** 0.9389
- **Weighted F1-Score:** 0.9389
- **Inference Latency (Avg):** 17.29 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `early_blight` | 100.0% | 100.0% | 1.0000 | 11.0 |
| `healthy` | 84.6% | 100.0% | 0.9167 | 11.0 |
| `late_blight` | 100.0% | 81.8% | 0.9000 | 11.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['early_blight', 'healthy', 'late_blight']

```text
    11     0     0
     0    11     0
     0     2     9
```