# Scientific Evaluation Report: rice_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T08:07:52.684851+00:00  
**Test Set Samples:** 16  

## Summary Performance
- **Overall Accuracy:** 62.50%
- **Macro Precision:** 58.33%
- **Macro Recall:** 60.00%
- **Macro F1-Score:** 0.5820
- **Weighted F1-Score:** 0.5992
- **Inference Latency (Avg):** 5.26 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_leaf_blight` | 75.0% | 100.0% | 0.8571 | 6.0 |
| `brown_spot` | 50.0% | 40.0% | 0.4444 | 5.0 |
| `leaf_smut` | 50.0% | 40.0% | 0.4444 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_leaf_blight', 'brown_spot', 'leaf_smut']

```text
     6     0     0
     1     2     2
     1     2     2
```