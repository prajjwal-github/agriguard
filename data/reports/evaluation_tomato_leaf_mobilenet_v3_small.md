# Scientific Evaluation Report: tomato_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:40:44.301478+00:00  
**Test Set Samples:** 45  

## Summary Performance
- **Overall Accuracy:** 88.89%
- **Macro Precision:** 90.78%
- **Macro Recall:** 88.89%
- **Macro F1-Score:** 0.8869
- **Weighted F1-Score:** 0.8869
- **Inference Latency (Avg):** 5.85 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_spot` | 100.0% | 88.9% | 0.9412 | 9.0 |
| `early_blight` | 100.0% | 66.7% | 0.8000 | 9.0 |
| `healthy` | 75.0% | 100.0% | 0.8571 | 9.0 |
| `late_blight` | 88.9% | 88.9% | 0.8889 | 9.0 |
| `septoria_leaf_spot` | 90.0% | 100.0% | 0.9474 | 9.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_spot', 'early_blight', 'healthy', 'late_blight', 'septoria_leaf_spot']

```text
     8     0     1     0     0
     0     6     1     1     1
     0     0     9     0     0
     0     0     1     8     0
     0     0     0     0     9
```