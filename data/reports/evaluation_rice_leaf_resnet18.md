# Scientific Evaluation Report: rice_leaf (resnet18)
**Evaluation Date:** 2026-10-23T14:37:11.498485+00:00  
**Test Set Samples:** 16  

## Summary Performance
- **Overall Accuracy:** 93.75%
- **Macro Precision:** 95.24%
- **Macro Recall:** 93.33%
- **Macro F1-Score:** 0.9373
- **Weighted F1-Score:** 0.9364
- **Inference Latency (Avg):** 25.56 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_leaf_blight` | 85.7% | 100.0% | 0.9231 | 6.0 |
| `brown_spot` | 100.0% | 80.0% | 0.8889 | 5.0 |
| `leaf_smut` | 100.0% | 100.0% | 1.0000 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_leaf_blight', 'brown_spot', 'leaf_smut']

```text
     6     0     0
     1     4     0
     0     0     5
```