# Scientific Evaluation Report: grape_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:22:38.693560+00:00  
**Test Set Samples:** 20  

## Summary Performance
- **Overall Accuracy:** 95.00%
- **Macro Precision:** 95.83%
- **Macro Recall:** 95.00%
- **Macro F1-Score:** 0.9495
- **Weighted F1-Score:** 0.9495
- **Inference Latency (Avg):** 8.53 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `black_rot` | 83.3% | 100.0% | 0.9091 | 5.0 |
| `esca_black_measles` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `healthy` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `leaf_blight` | 100.0% | 80.0% | 0.8889 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['black_rot', 'esca_black_measles', 'healthy', 'leaf_blight']

```text
     5     0     0     0
     0     5     0     0
     0     0     5     0
     1     0     0     4
```