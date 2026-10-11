# AgriGuard AI — Architecture Specification

## 1. System Philosophy
AgriGuard AI is an agricultural pathology intelligence platform that rejects naive image classification assumptions. It treats plant organs, crops, and disease manifestations as distinct taxonomic domains:
- **Hierarchical Organ & Crop Routing**: Never routes fruit skins to leaf models or cereal grains to vegetable classifiers.
- **Evidence-Based Pathology**: Predictions are strictly tied to peer-reviewed agronomic descriptions (IRRI, Penn State Extension, Cornell AgriTech).
- **Out-of-Distribution Rejection**: Any low-confidence or high-entropy image is rejected with an honest uncertainty warning.
- **Zero Data Fabrication**: Models are only marked operational when trained on legitimate, validated research datasets.

## 2. Component Architecture
```
[ Farmer / Client UI ] 
        │
        ▼ (HTTPS / REST)
[ FastAPI Gateway (main.py) ]
        │
   ┌────┴───────────────────────────┐
   ▼                                ▼
[ ImageValidator ]          [ ModelRouter ]
(Format, Resolution,               │ (Category -> Crop -> Task)
 Quarantine, Channels)              ▼
                            [ PyTorch Model Cache ]
                                   │ (Lazy Loaded)
                                   ▼
                            [ InferencePipeline ]
                                   ├── Softmax Distribution
                                   ├── Shannon Entropy (OOD)
                                   ├── SeverityEstimator (ExG Area)
                                   ├── Grad-CAM Heatmap
                                   └── KnowledgeBaseService
```

## 3. Technology Stack
- **Deep Learning**: PyTorch 2.14, Torchvision (MobileNetV3-Small / Large, ResNet-18)
- **Backend API**: FastAPI, Pydantic v2, Uvicorn
- **Data Engineering**: PIL, NumPy, Scikit-Learn, PyYAML
- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS, Lucide Icons
