# AgriGuard AI — Multi-Category Dataset & Model Coverage Audit
**Audit Generated:** 2026-10-11T11:30:47.440733+00:00  
**Standard:** Scientific honesty, zero data fabrication, strict task/organ routing.  

## Category Coverage Matrix
| Category | Crop | Plant Organ | Dataset Status | Verified Images | Trained Model | Model Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Fruit** | Apple | Fruit / Vegetable Surface | Verified Authentic | 180 | ✅ Yes | `ready` |
| **Fruit** | Banana | Fruit / Vegetable Surface | Verified Authentic | 180 | ✅ Yes | `ready` |
| **Fruit** | Orange | Fruit / Vegetable Surface | Verified Authentic | 180 | ✅ Yes | `ready` |
| **Fruit** | Mango | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Fruit** | Grapes | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Fruit Leaf** | Apple Leaf | Leaf | Verified Authentic | 120 | ✅ Yes | `ready` |
| **Fruit Leaf** | Grape Leaf | Leaf | Verified Authentic | 120 | ✅ Yes | `ready` |
| **Fruit Leaf** | Citrus / Orange Leaf | Leaf | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Fruit Leaf** | Mango Leaf | Leaf | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Fruit Leaf** | Banana Leaf | Leaf | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Vegetable** | Tomato | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Vegetable** | Potato | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Vegetable** | Chilli / Pepper | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Vegetable** | Brinjal / Eggplant | Fruit / Vegetable Surface | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Vegetable Leaf** | Tomato Leaf | Leaf | Verified Authentic | 300 | ✅ Yes | `ready` |
| **Vegetable Leaf** | Potato Leaf | Leaf | Verified Authentic | 195 | ✅ Yes | `ready` |
| **Vegetable Leaf** | Chilli / Pepper Leaf | Leaf | Verified Authentic | 100 | ✅ Yes | `ready` |
| **Vegetable Leaf** | Brinjal Leaf | Leaf | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Grain** | Rice / Paddy Grain | Grain | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Grain** | Wheat Grain | Grain | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Grain** | Maize / Corn Grain | Grain | Planned / Curation Pending | 0 | ❌ No | `planned` |
| **Grain Crop / Leaf** | Rice / Paddy Leaf | Leaf | Verified Authentic | 91 | ✅ Yes | `ready` |
| **Grain Crop / Leaf** | Maize / Corn Leaf | Leaf | Verified Authentic | 120 | ✅ Yes | `ready` |
| **Grain Crop / Leaf** | Wheat Plant / Leaf | Leaf | Planned / Curation Pending | 0 | ❌ No | `planned` |

## Scientific Integrity Statement
1. **No Data Fabrication**: Crops designated as `planned` or lacking verified research datasets are explicitly documented as unsupported in inference rather than guessing or outputting mock disease predictions.
2. **Organ-Specific Routing**: Foliage models do not accept fruit surfaces; fruit surface models do not accept leaf foliage.
3. **Out-of-Distribution Rejection**: Images submitted to operational models that fail confidence (<55%) or exhibit high entropy (>1.85) are rejected with clear agricultural advisory notices.

## Summary of Operational Assets
- **Operational Models**: `rice_leaf` (MobileNetV3-Small, Prajapati Rice Leaf Benchmark, Test Accuracy 62.5%, Macro-F1 0.582, Latency 5.26ms).
- **Supported Categories in UI**: All 6 primary agricultural categories available in selector.
- **API Enforcement**: `/api/v1/predict` strictly validates crop/category matching and returns 400 for unvalidated models.