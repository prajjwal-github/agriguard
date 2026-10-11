# Dataset Audit Report: rice_leaf (grain_crop_leaf)
**Dataset Provenance:** Prajapati, H. B. et al., Rice Leaf Diseases Dataset, Computers & Electronics in Agriculture (2017)  
**License:** CC BY 4.0 / Open Academic Research Access  
**Audit Timestamp:** 2026-10-11T08:01:55+00:00  
**Quality Gate Status:** ✅ PASSED  

## Summary Metrics
- **Total Acquired Samples:** 105
- **Quarantined (Aspect Ratio / Dimension Violations):** 14
- **Usable Verified Samples:** 91
- **Exact & Perceptual Duplicates Detected:** 0
- **Total Classes:** 3 (`bacterial_leaf_blight`, `brown_spot`, `leaf_smut`)
- **Class Imbalance Ratio:** 1.25:1 (well within threshold <= 8.0:1)
- **Data Leakage Check:** ZERO leakage between train, val, and test splits

## Class Distribution
| Condition / Class | Sample Count | Percentage |
| :--- | :--- | :--- |
| `bacterial_leaf_blight` | 35 | 38.5% |
| `brown_spot` | 28 | 30.8% |
| `leaf_smut` | 28 | 30.8% |

## Split Breakdown
| Split | Sample Count | Share | Target Ratio |
| :--- | :--- | :--- | :--- |
| `train` | 62 | 68.1% | ~70% |
| `val` | 13 | 14.3% | ~15% |
| `test` | 16 | 17.6% | ~15% |

## Resolution Statistics
- **Width:** Min 250px, Avg 2635.7px, Max 3081px
- **Height:** Min 88px, Avg 785.8px, Max 900px

## Quality Gate Findings
- No critical failures.
- Zero image leakage verified across hash clusters.
- All 91 images verified with RGB channel depth and valid headers.
