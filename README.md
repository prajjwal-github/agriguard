# AgriGuard AI
### Production-Quality, Multi-Crop Agricultural Disease Detection & Health Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14%2B-ee4c2c.svg)](https://pytorch.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 1. Vision & Architecture Overview
**AgriGuard AI** is a scientifically responsible, multi-crop agricultural pathology detection and health intelligence platform designed for farmers, agronomists, and agricultural extension services. 

Unlike naive image classifiers that funnel every uploaded image through a single undifferentiated network, AgriGuard AI enforces:
- **Hierarchical Organ & Crop Routing**: Segregates Fruit Surface, Fruit Leaf, Vegetable Surface, Vegetable Leaf, Grain Kernel, and Grain Crop / Leaf tasks.
- **Authentic Dataset Engineering**: Zero synthetic imagery; all images originate from verified peer-reviewed research repositories (Prajapati Rice Leaf Benchmark, PlantVillage).
- **Leakage-Resistant Dataset Splitting**: Perceptual difference hashing (`dHash`) and MD5 clustering guarantee 0% data leakage across Train (70%), Validation (15%), and Test (15%) splits.
- **Genuine Neural Models**: Real PyTorch checkpoints trained with class-balanced weighting, validation early stopping, and isolated test evaluation.
- **Out-of-Distribution Rejection**: Shannon entropy thresholding ($H > 1.85$) and confidence calibration reject non-target or unconfident photos with clear advisory warnings.
- **Visual Explainability**: Grad-CAM convolutional attention overlays demonstrate model focus.
- **Evidence-Based Agricultural Knowledge Base**: Integrates peer-reviewed management practices (IRRI, Penn State Extension, Cornell AgriTech).

---

## 2. Directory Structure
```text
AgriGuard/
├── configs/                # Dataset, training, inference, and model registry configs
├── data/
│   ├── raw/                # Validated authentic image datasets
│   ├── interim/            # Quarantined invalid/corrupt images
│   ├── manifests/          # Master dataset manifest with hash clusters
│   └── reports/            # Audit, coverage, and evaluation reports
├── datasets/               # Provenance sources and canonical taxonomy
├── models/
│   ├── checkpoints/        # Best training checkpoints (.pt)
│   └── exported/           # Standalone production model bundles (.pt)
├── scripts/                # Python CLI automation tools (No notebooks!)
│   ├── discover_datasets.py
│   ├── download_datasets.py
│   ├── validate_images.py
│   ├── normalize_labels.py
│   ├── deduplicate_images.py
│   ├── generate_manifest.py
│   ├── split_dataset.py
│   ├── audit_dataset.py
│   ├── run_pipeline.py     # Master dataset pipeline orchestrator
│   ├── train_model.py      # PyTorch model training CLI
│   ├── evaluate_model.py   # Test split scientific evaluator
│   └── generate_coverage_report.py
├── src/agriguard/          # Core Python application package
│   ├── api/                # FastAPI backend routes & schemas
│   ├── config/             # Environment & YAML loaders
│   ├── datasets/           # Validation, deduplication, splitting, torch dataset
│   ├── explainability/     # Grad-CAM engine
│   ├── inference/          # End-to-end inference pipeline
│   ├── knowledge_base/     # Disease dictionary & query service
│   ├── model_registry/     # Hierarchical routing & lazy model cache
│   ├── severity/           # Empirical ExG lesion percentage estimator
│   └── training/           # Loss, model factory, trainer
├── frontend/               # Farmer-friendly React + Vite + TypeScript web interface
├── tests/                  # Pytest unit, integration, and smoke test suites
└── docs/                   # Full documentation suite
```

---

## 3. Quickstart & Execution Guide

### A. Environment Setup
```powershell
# Clone or navigate to the workspace
cd D:\AgriGuard

# Install Python requirements and package in editable mode
pip install -r requirements.txt
pip install -e . --no-deps
```

### B. One-Command Dataset Preparation
```powershell
# Run the complete dataset engineering pipeline for Rice Leaf Diseases
python -m scripts.run_pipeline --crop rice_leaf --samples-per-class 35
```

### C. Train and Evaluate the Baseline Model
```powershell
# Train MobileNetV3-Small on the authentic Rice Leaf Disease dataset
python -m scripts.train_model --crop rice_leaf --arch mobilenet_v3_small --epochs 8 --batch-size 16 --lr 0.0003

# Run scientific evaluation on the held-out test split
python -m scripts.evaluate_model --crop rice_leaf --arch mobilenet_v3_small
```

### D. Run Automated Test Suite
```powershell
# Run all 19 unit & integration tests
python -m pytest tests/

# Run the live smoke test with real model inference
python -m pytest tests/smoke/test_smoke.py -s
```

### E. Start the Backend API
```powershell
uvicorn agriguard.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive OpenAPI documentation will be available at: `http://localhost:8000/docs`

### F. Start the Farmer Frontend
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 4. Operational Model Benchmark Results
Evaluated on the isolated, held-out test split (16 samples, 0% leakage):

| Model | Architecture | Test Accuracy | Macro Precision | Macro Recall | Macro F1 | Latency | Checkpoint |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `rice_leaf` | MobileNetV3-Small | **62.50%** | **58.33%** | **60.00%** | **0.5820** | **5.26 ms** | `models/exported/rice_leaf_mobilenet_v3_small.pt` |

### Per-Class Test Breakdown
- **Bacterial Leaf Blight**: Precision 75.0%, Recall 100.0%, F1 0.8571 (Support: 6)
- **Brown Spot**: Precision 50.0%, Recall 40.0%, F1 0.4444 (Support: 5)
- **Leaf Smut**: Precision 50.0%, Recall 40.0%, F1 0.4444 (Support: 5)

---

## 5. Multi-Category Coverage Matrix
AgriGuard AI structures pathology across 6 categories:

| Category | Supported Crops | Dataset Status | Operational Model |
| :--- | :--- | :--- | :--- |
| **1. Fruit Surface** | Apple, Banana, Mango, Orange, Grapes | Planned / Manual Curation | In Development (Honest Rejection) |
| **2. Fruit Leaf** | Apple leaf, Grape leaf, Citrus leaf | PlantVillage Verified | Ready for Pipeline |
| **3. Vegetable Surface** | Tomato, Potato tuber, Bell Pepper | Planned / Manual Curation | In Development (Honest Rejection) |
| **4. Vegetable Leaf** | Tomato leaf, Potato leaf, Pepper leaf | PlantVillage Verified | Ready for Pipeline |
| **5. Grain Kernel** | Rice grain, Wheat grain, Maize grain | Planned / Manual Curation | In Development (Honest Rejection) |
| **6. Grain Crop / Leaf** | Rice leaf, Maize leaf, Wheat leaf | Prajapati Benchmark | ✅ Operational Checkpoint (`rice_leaf`) |

---

## 6. Scientific Integrity & Disclaimers
1. **No Fake Accuracy**: All metrics reported in `data/reports/` reflect real evaluation scripts executed against genuine held-out test sets.
2. **Honest Rejections**: The model refuses to guess when images fail confidence (<55%) or exceed Shannon entropy thresholds (>1.85).
3. **Clinical Guidance**: Visual predictions are advisory aids and do not substitute for on-site agricultural extension diagnosis.
