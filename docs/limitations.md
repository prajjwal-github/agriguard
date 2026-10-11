# AgriGuard AI — Known Limitations and Scope

## 1. Controlled vs Field Domain Shift
Current open public agricultural datasets (such as PlantVillage and the classic Prajapati Rice Leaf dataset) often feature uniform studio backgrounds or lab-isolated leaf segments. While data augmentation (rotations, color jitter, mild sensor noise) helps bridge domain variance, field photography with overlapping canopies and harsh solar specularities may yield reduced confidence.

## 2. Out-of-Distribution & Uncalibrated Softmax
A standard neural network outputting softmax scores can make overconfident predictions on arbitrary objects. AgriGuard AI counters this by:
- Enforcing Shannon entropy thresholds ($H > 1.85$ triggers rejection).
- Enforcing a minimum confidence threshold ($p_{\max} < 0.55$ triggers rejection).
- Returning explicit uncertainty warnings rather than guessing a diagnosis.

## 3. Scope of Operational Models
Only crops with verified training datasets and exported checkpoints (`models/exported/`) are operational (`rice_leaf`). Crops listed as `planned` or `in development` are clearly demarcated in the UI and API. AgriGuard AI refuses to provide fabricated predictions for unvalidated crops.

## 4. Medical / Chemical Advisory Disclaimer
AgriGuard AI provides preliminary visual assessments. It does not replace on-site agricultural extension diagnostics, soil laboratory chemical tests, or statutory regulatory chemical application advice.
