"""End-to-End multi-crop live inference verification test."""

import glob
import requests
from pathlib import Path

def test_all_operational_crops():
    base_url = "http://127.0.0.1:8080"

    # 1. Health check
    health_res = requests.get(f"{base_url}/api/v1/health")
    assert health_res.status_code == 200, f"Health check failed: {health_res.text}"
    print(f"[HEALTH CHECK PASSED]: {health_res.json()}")

    crops_to_test = [
        ("fruit", "apple", "data/raw/apple/rot_decay/*.jpg"),
        ("fruit", "banana", "data/raw/banana/rot_decay/*.jpg"),
        ("fruit", "orange", "data/raw/orange/rot_decay/*.jpg"),
        ("fruit_leaf", "apple_leaf", "data/raw/apple_leaf/apple_scab/*.[jJ][pP]*"),
        ("fruit_leaf", "grape_leaf", "data/raw/grape_leaf/black_rot/*.[jJ][pP]*"),
        ("vegetable_leaf", "tomato_leaf", "data/raw/tomato_leaf/early_blight/*.[jJ][pP]*"),
        ("vegetable_leaf", "potato_leaf", "data/raw/potato_leaf/early_blight/*.[jJ][pP]*"),
        ("vegetable_leaf", "chilli_leaf", "data/raw/chilli_leaf/bacterial_spot/*.[jJ][pP]*"),
        ("grain_crop_leaf", "rice_leaf", "data/raw/rice_leaf/bacterial_leaf_blight/*.[jJ][pP]*"),
        ("grain_crop_leaf", "maize_leaf", "data/raw/maize_leaf/common_rust/*.[jJ][pP]*"),
    ]

    print(f"\nRunning live inference verification across {len(crops_to_test)} crops...")
    verified_count = 0

    for cat, crop, pattern in crops_to_test:
        matches = glob.glob(pattern)
        if not matches:
            print(f"FAILED: No sample image found for {crop} matching {pattern}")
            continue

        sample_file = matches[0]
        with open(sample_file, "rb") as f:
            res = requests.post(
                f"{base_url}/api/v1/predict",
                files={"file": f},
                data={"category": cat, "crop": crop},
            )

        assert res.status_code == 200, f"Inference failed for {crop}: {res.status_code} {res.text}"
        data = res.json()

        pred_cond = data.get("predicted_condition")
        display_name = data.get("display_name")
        conf = data.get("confidence")
        is_reliable = data.get("is_reliable")
        gradcam = bool(data.get("gradcam_heatmap"))
        plant_part = data.get("plant_part")
        latency = data.get("processing_time_ms")

        print(
            f"  [OK] {cat:15} -> {crop:12}: Pred='{pred_cond}' ({display_name}), "
            f"Conf={conf*100:.1f}%, Part='{plant_part}', GradCAM={gradcam}, Latency={latency:.1f}ms"
        )
        verified_count += 1

    print(f"\nSuccessfully verified {verified_count}/{len(crops_to_test)} operational models live!")

if __name__ == "__main__":
    test_all_operational_crops()
