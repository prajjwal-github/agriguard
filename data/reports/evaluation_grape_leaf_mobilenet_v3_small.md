# Scientific Evaluation Report: grape_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:14:50.848369+00:00  
**Test Set Samples:** 20  

## Summary Performance
- **Overall Accuracy:** 85.00%
- **Macro Precision:** 88.69%
- **Macro Recall:** 85.00%
- **Macro F1-Score:** 0.8285
- **Weighted F1-Score:** 0.8285
- **Inference Latency (Avg):** 8.19 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `black_rot` | 71.4% | 100.0% | 0.8333 | 5.0 |
| `esca_black_measles` | 83.3% | 100.0% | 0.9091 | 5.0 |
| `healthy` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `leaf_blight` | 100.0% | 40.0% | 0.5714 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['black_rot', 'esca_black_measles', 'healthy', 'leaf_blight']

```text
     5     0     0     0
     0     5     0     0
     0     0     5     0
     2     1     0     2
```