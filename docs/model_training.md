# AgriGuard AI — Model Training and Evaluation Guide

## 1. Training Architecture
AgriGuard AI utilizes fine-tuned lightweight convolutional backbones (default `mobilenet_v3_small` with transfer learning from ImageNet features) optimized for fast CPU/edge inference.

Key features:
- **Inverse Frequency Class Weighting**: Mitigates class imbalance without synthetic data corruption.
- **AdamW Optimizer & Cosine Annealing**: Dynamic learning rate scheduling with weight decay (1e-4).
- **Validation Early Stopping**: Evaluates macro F1 on validation splits to prevent overfitting.
- **Production Bundling**: Serializes state dicts, normalization parameters, and class maps into standalone `.pt` archives in `models/exported/`.

## 2. Training Commands
```bash
# Train baseline classifier for rice leaf diseases
python -m scripts.train_model --crop rice_leaf --arch mobilenet_v3_small --epochs 8 --batch-size 16 --lr 0.0003

# Evaluate on isolated held-out test split
python -m scripts.evaluate_model --crop rice_leaf --arch mobilenet_v3_small
```

## 3. Evaluation Protocol
The evaluation suite runs on the held-out test set (16 samples for `rice_leaf`), computing:
- Accuracy (62.50%)
- Macro Precision (58.33%)
- Macro Recall (60.00%)
- Macro F1-Score (0.5820)
- Average Latency (5.26 ms / sample)
- Confusion Matrix
Reports are automatically written to `data/reports/evaluation_<crop>_<arch>.md` and `.json`.
