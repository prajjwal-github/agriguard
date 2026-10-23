# Scientific Evaluation Report: tomato_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:27:02.509331+00:00  
**Test Set Samples:** 45  

## Summary Performance
- **Overall Accuracy:** 93.33%
- **Macro Precision:** 93.78%
- **Macro Recall:** 93.33%
- **Macro F1-Score:** 0.9332
- **Weighted F1-Score:** 0.9332
- **Inference Latency (Avg):** 6.96 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_spot` | 100.0% | 88.9% | 0.9412 | 9.0 |
| `early_blight` | 88.9% | 88.9% | 0.8889 | 9.0 |
| `healthy` | 90.0% | 100.0% | 0.9474 | 9.0 |
| `late_blight` | 100.0% | 88.9% | 0.9412 | 9.0 |
| `septoria_leaf_spot` | 90.0% | 100.0% | 0.9474 | 9.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_spot', 'early_blight', 'healthy', 'late_blight', 'septoria_leaf_spot']

```text
     8     0     0     0     1
     0     8     1     0     0
     0     0     9     0     0
     0     1     0     8     0
     0     0     0     0     9
```