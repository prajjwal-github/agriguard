# Scientific Evaluation Report: apple_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:12:58.242727+00:00  
**Test Set Samples:** 20  

## Summary Performance
- **Overall Accuracy:** 95.00%
- **Macro Precision:** 95.83%
- **Macro Recall:** 95.00%
- **Macro F1-Score:** 0.9495
- **Weighted F1-Score:** 0.9495
- **Inference Latency (Avg):** 8.32 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `apple_scab` | 100.0% | 80.0% | 0.8889 | 5.0 |
| `black_rot` | 83.3% | 100.0% | 0.9091 | 5.0 |
| `cedar_apple_rust` | 100.0% | 100.0% | 1.0000 | 5.0 |
| `healthy` | 100.0% | 100.0% | 1.0000 | 5.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['apple_scab', 'black_rot', 'cedar_apple_rust', 'healthy']

```text
     4     1     0     0
     0     5     0     0
     0     0     5     0
     0     0     0     5
```