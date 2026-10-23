# Scientific Evaluation Report: chilli_leaf (mobilenet_v3_small)
**Evaluation Date:** 2026-10-23T14:16:57.806792+00:00  
**Test Set Samples:** 16  

## Summary Performance
- **Overall Accuracy:** 93.75%
- **Macro Precision:** 94.44%
- **Macro Recall:** 93.75%
- **Macro F1-Score:** 0.9373
- **Weighted F1-Score:** 0.9373
- **Inference Latency (Avg):** 6.06 ms / sample

## Per-Class Breakdown
| Condition | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `bacterial_spot` | 100.0% | 87.5% | 0.9333 | 8.0 |
| `healthy` | 88.9% | 100.0% | 0.9412 | 8.0 |

## Confusion Matrix
Rows represent ground-truth classes; columns represent model predictions: ['bacterial_spot', 'healthy']

```text
     7     1
     0     8
```