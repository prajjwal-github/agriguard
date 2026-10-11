# Scientific Evaluation Report: maize_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:16:52.959456+00:00  
**Test Set Samples:** 20  

## Summary Performance
- **Overall Accuracy:** 90.00%
- **Macro Precision:** 92.86%
- **Macro Recall:** 90.00%
- **Macro F1-Score:** 0.8958
- **Weighted F1-Score:** 0.8958
- **Inference Latency (Avg):** 8.57 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `cercospora_leaf_spot` | 71.4% | 100.0% | 0.8333 | 5.0 |
| `common_rust` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `healthy` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `northern_leaf_blight` | 100.0% | 60.0% | 0.7500 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['cercospora_leaf_spot', 'common_rust', 'healthy', 'northern_leaf_blight']

```text
     5     0     0     0
     0     5     0     0
     0     0     5     0
     2     0     0     3
```