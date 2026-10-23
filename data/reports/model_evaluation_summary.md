# AgriGuard AI — Multi-Crop Scientific Model Evaluation Summary

| Category | Crop | Architecture | Classes | Held-Out Test N | Accuracy | Macro F1 | Macro Prec | Macro Rec | Latency | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| fruit | **Apple** (`apple`) | `resnet18` | 3 classes | 27 | **88.9%** | 0.8857 | 0.9167 | 0.8889 | 19.11 ms | `Operational` |
| fruit | **Banana** (`banana`) | `mobilenet_v3_small` | 3 classes | 18 | **100.0%** | 1.0000 | 1.0000 | 1.0000 | 13.10 ms | `Operational` |
| fruit | **Orange** (`orange`) | `mobilenet_v3_small` | 3 classes | 18 | **94.4%** | 0.9441 | 0.9524 | 0.9444 | 15.07 ms | `Operational` |
| fruit_leaf | **Apple Leaf** (`apple_leaf`) | `mobilenet_v3_small` | 4 classes | 20 | **95.0%** | 0.9495 | 0.9583 | 0.9500 | 8.32 ms | `Operational` |
| fruit_leaf | **Grape Leaf** (`grape_leaf`) | `mobilenet_v3_small` | 4 classes | 20 | **95.0%** | 0.9495 | 0.9583 | 0.9500 | 8.53 ms | `Operational` |
| vegetable_leaf | **Tomato Leaf** (`tomato_leaf`) | `mobilenet_v3_small` | 5 classes | 45 | **93.3%** | 0.9332 | 0.9378 | 0.9333 | 6.96 ms | `Operational` |
| vegetable_leaf | **Potato Leaf** (`potato_leaf`) | `mobilenet_v3_small` | 3 classes | 33 | **93.9%** | 0.9389 | 0.9487 | 0.9394 | 17.29 ms | `Operational` |
| vegetable_leaf | **Chilli / Pepper Leaf** (`chilli_leaf`) | `mobilenet_v3_small` | 2 classes | 16 | **93.8%** | 0.9373 | 0.9444 | 0.9375 | 6.06 ms | `Operational` |
| grain_crop_leaf | **Rice / Paddy Leaf** (`rice_leaf`) | `resnet18` | 3 classes | 16 | **93.8%** | 0.9373 | 0.9524 | 0.9333 | 25.56 ms | `Operational` |
| grain_crop_leaf | **Maize / Corn Leaf** (`maize_leaf`) | `mobilenet_v3_small` | 4 classes | 20 | **90.0%** | 0.8958 | 0.9286 | 0.9000 | 8.57 ms | `Operational` |