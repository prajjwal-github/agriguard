# AgriGuard AI — Scientific Reliability, Calibration & OOD Safety Audit

## 1. Split Integrity & Cryptographic Leakage Verification
| Crop | Train N | Val N | Isolated Test N | ID Overlap | Perceptual dHash Leakage | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **apple** | 126 | 27 | 27 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **apple_leaf** | 84 | 16 | 20 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **banana** | 126 | 27 | 27 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **chilli_leaf** | 70 | 14 | 16 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **grape_leaf** | 84 | 16 | 20 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **maize_leaf** | 84 | 16 | 20 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **orange** | 126 | 27 | 27 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **potato_leaf** | 135 | 27 | 33 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **rice_leaf** | 62 | 13 | 16 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |
| **tomato_leaf** | 210 | 45 | 45 | 0 | 0 | `VERIFIED ZERO LEAKAGE (0.0%)` |

## 2. Confidence Calibration & Uncertainty Quantification
> [!IMPORTANT]
> As established by Guo et al. (2017), modern deep neural network softmax outputs reflect relative class separation rather than true Bayesian posterior probabilities. AgriGuard AI couples confidence thresholds with Shannon entropy quantification to safeguard clinical decisions.

| Crop | Isolated Test N | Empirical Accuracy | Mean Softmax Conf | Expected Calibration Error (ECE) | Brier Score | Reliability Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **apple** | 27 | 88.9% | 88.7% | 0.1098 | 0.2157 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **apple_leaf** | 20 | 95.0% | 79.1% | 0.1929 | 0.1158 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **banana** | 27 | 92.6% | 85.6% | 0.1260 | 0.0872 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **chilli_leaf** | 16 | 62.5% | 73.6% | 0.1774 | 0.4215 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **grape_leaf** | 20 | 85.0% | 69.7% | 0.2051 | 0.2234 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **maize_leaf** | 20 | 90.0% | 80.0% | 0.1531 | 0.1580 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **orange** | 27 | 88.9% | 83.8% | 0.0791 | 0.1935 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **potato_leaf** | 33 | 75.8% | 90.9% | 0.1872 | 0.3516 | Uncalibrated Softmax Overconfidence; requires entropy thresholding and clinical expert triage |
| **rice_leaf** | 16 | 62.5% | 43.9% | 0.2912 | 0.5512 | Small-Sample Indicative Only (N<30); uncalibrated softmax cannot be interpreted as posterior certainty |
| **tomato_leaf** | 45 | 88.9% | 83.4% | 0.1087 | 0.1792 | Uncalibrated Softmax Overconfidence; requires entropy thresholding and clinical expert triage |

## 3. Out-of-Distribution (OOD) Safety & False-Positive Rejection Tests
| OOD Test Input | Predicted Condition | Confidence | Shannon Entropy | Rejection Triggered (`is_reliable: False`) | Safety Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `gaussian_noise` | bacterial_leaf_blight | 37.9% | 1.090 | **True** | `PASSED (False Positive Prevented)` |
| `uniform_gray` | bacterial_leaf_blight | 39.5% | 1.090 | **True** | `PASSED (False Positive Prevented)` |
| `checkerboard` | bacterial_leaf_blight | 44.2% | 1.068 | **True** | `PASSED (False Positive Prevented)` |