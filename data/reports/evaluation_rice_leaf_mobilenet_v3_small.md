# Scientific Evaluation Report: rice_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:35:26.429421+00:00  
**Test Set Samples:** 16  

## Summary Performance
- **Overall Accuracy:** 87.50%
- **Macro Precision:** 90.48%
- **Macro Recall:** 86.67%
- **Macro F1-Score:** 0.8611
- **Weighted F1-Score:** 0.8698
- **Inference Latency (Avg):** 4.56 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_leaf_blight` | 100.0% | 100.0% | 1.0000 | 6.0 |
| `brown_spot` | 100.0% | 60.0% | 0.7500 | 5.0 |
| `leaf_smut` | 71.4% | 100.0% | 0.8333 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_leaf_blight', 'brown_spot', 'leaf_smut']

```text
     6     0     0
     0     3     2
     0     0     5
```