# AgriGuard AI — Dataset Engineering Guide

## 1. Provenance and Licensing
All datasets ingested by AgriGuard AI originate from verified, open scientific repositories under permissive academic licenses:
- **Rice Leaf Diseases Dataset**: Prajapati et al. (Computers and Electronics in Agriculture, 2017). CC BY 4.0. Contains Bacterial Leaf Blight, Brown Spot, and Leaf Smut foliage images.
- **PlantVillage Open Research Dataset**: Hughes & Salathé (Penn State, 2015). CC BY 4.0. Contains multi-crop leaf condition datasets for Apple, Grape, Tomato, Potato, and Maize foliage.

## 2. Dataset Pipeline Stages
Execute the automated dataset pipeline:
```bash
python -m scripts.run_pipeline --config configs/dataset.yaml --crop rice_leaf --samples-per-class 35
```

Stages executed:
1. **Discovery**: Verifies remote repository connectivity and licensing terms.
2. **Concurrent Download**: Fetches authentic images using a thread pool with retry logic.
3. **Image Validation**: Checks raster headers, minimum dimensions (64x64), maximum dimensions (4096), and aspect ratios (<= 3.5). Violations are quarantined to `data/interim/corrupt/`.
4. **Label Normalization**: Canonicalizes folder names to standard taxonomy (`datasets/taxonomy.yaml`).
5. **Deduplication**: Calculates cryptographic MD5 and perceptual dHash (Hamming distance threshold = 4) to identify duplicates and near-duplicates.
6. **Master Manifest**: Exports `data/manifests/master_manifest.json` with hash cluster mappings.
7. **Leakage-Resistant Splitting**: Groups near-duplicate clusters to ensure 0% data leakage between Train (70%), Validation (15%), and Test (15%) splits.
8. **Audit & Readiness Gate**: Verifies class representation, imbalance ratio (<= 8.0:1), and outputs markdown and JSON audit summaries.
