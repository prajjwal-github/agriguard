# Scientific Evaluation Report: chilli_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-11T09:41:26.848680+00:00  
**Test Set Samples:** 16  

## Summary Performance
- **Overall Accuracy:** 62.50%
- **Macro Precision:** 78.57%
- **Macro Recall:** 62.50%
- **Macro F1-Score:** 0.5636
- **Weighted F1-Score:** 0.5636
- **Inference Latency (Avg):** 6.4 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_spot` | 100.0% | 25.0% | 0.4000 | 8.0 |
| `healthy` | 57.1% | 100.0% | 0.7273 | 8.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_spot', 'healthy']

```text
     2     6
     0     8
```