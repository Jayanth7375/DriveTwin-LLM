import os
import sys
import glob
import shutil
import json
import numpy as np

DATASET_ROOT = "d:/LLM Forge/dataset"

CLASSES = [
    "NO_ISSUE",
    "CYL_3_IGNITION_MISFIRE",
    "CYL_5_INJECTOR_CLOGGING",
    "TURBO_BOOST_LEAK",
    "MAF_SENSOR_DRIFT",
    "EGR_VALVE_STUCK_OPEN",
    "HEAD_GASKET_BREACH",
    "HPFP_PRESSURE_DROP"
]

SPLIT_RATIOS = {
    "train": 0.70,
    "validate": 0.15,
    "test": 0.15
}

def main():
    print("=" * 75)
    print("      DIESEL I6 ECU TELEMETRY DATASET ORGANIZER (TRAIN / VALIDATE / TEST)")
    print("=" * 75)
    
    # Target directories
    train_dir = os.path.join(DATASET_ROOT, "train")
    val_dir = os.path.join(DATASET_ROOT, "validate")
    test_dir = os.path.join(DATASET_ROOT, "test")
    
    # Create target split directories for each class
    for split in ["train", "validate", "test"]:
        for cls in CLASSES:
            os.makedirs(os.path.join(DATASET_ROOT, split, cls), exist_ok=True)
            
    summary_stats = {split: {cls: 0 for cls in CLASSES} for split in ["train", "validate", "test"]}
    total_processed = 0

    np.random.seed(42)

    for cls in CLASSES:
        # Search for CSV files belonging to this class in dataset_15gb, dataset_5gb, or class root
        search_patterns = [
            os.path.join(DATASET_ROOT, "dataset_15gb", cls, "*.csv"),
            os.path.join(DATASET_ROOT, "dataset_5gb", cls, "*.csv"),
            os.path.join(DATASET_ROOT, cls, "*.csv")
        ]
        
        class_files = []
        for pat in search_patterns:
            class_files.extend(glob.glob(pat))
            
        # Deduplicate by absolute path
        class_files = list(set(class_files))
        num_files = len(class_files)
        
        if num_files == 0:
            print(f"Warning: No files found for class '{cls}'")
            continue

        # Shuffle deterministically
        np.random.shuffle(class_files)

        n_train = int(num_files * SPLIT_RATIOS["train"])
        n_val = int(num_files * SPLIT_RATIOS["validate"])
        # n_test gets remainder
        
        train_files = class_files[:n_train]
        val_files = class_files[n_train:n_train + n_val]
        test_files = class_files[n_train + n_val:]
        
        # Move files to respective destination folders
        for src in train_files:
            dst = os.path.join(train_dir, cls, os.path.basename(src))
            shutil.move(src, dst)
            summary_stats["train"][cls] += 1

        for src in val_files:
            dst = os.path.join(val_dir, cls, os.path.basename(src))
            shutil.move(src, dst)
            summary_stats["validate"][cls] += 1

        for src in test_files:
            dst = os.path.join(test_dir, cls, os.path.basename(src))
            shutil.move(src, dst)
            summary_stats["test"][cls] += 1

        total_cls = len(train_files) + len(val_files) + len(test_files)
        total_processed += total_cls
        print(f"Class '{cls:25s}': {total_cls:5,d} files -> Train: {len(train_files):5,d} | Val: {len(val_files):4,d} | Test: {len(test_files):4,d}")

    # Clean up empty source directories if empty
    for dname in ["dataset_15gb", "dataset_5gb"]:
        sub_path = os.path.join(DATASET_ROOT, dname)
        if os.path.exists(sub_path):
            try:
                shutil.rmtree(sub_path)
                print(f"Cleaned up legacy folder '{dname}'")
            except Exception as e:
                pass

    for cls in CLASSES:
        old_cls_dir = os.path.join(DATASET_ROOT, cls)
        if os.path.exists(old_cls_dir) and not os.listdir(old_cls_dir):
            os.rmdir(old_cls_dir)

    # Save metadata summary manifest
    manifest_path = os.path.join(DATASET_ROOT, "dataset_summary.json")
    manifest = {
        "dataset_name": "Diesel I6 High-Frequency Telemetry Dataset",
        "total_files": total_processed,
        "splits_ratio": "70% Train / 15% Validate / 15% Test",
        "split_counts": {
            "train_total": sum(summary_stats["train"].values()),
            "validate_total": sum(summary_stats["validate"].values()),
            "test_total": sum(summary_stats["test"].values())
        },
        "per_class_summary": summary_stats
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 75)
    print("      DATASET ORGANIZATION COMPLETE")
    print("=" * 75)
    print(f"Total Telemetry Files Organized : {total_processed:,}")
    print(f"  • Train Set    (70%)          : {manifest['split_counts']['train_total']:,} files")
    print(f"  • Validate Set (15%)          : {manifest['split_counts']['validate_total']:,} files")
    print(f"  • Test Set     (15%)          : {manifest['split_counts']['test_total']:,} files")
    print(f"\nSaved Dataset Manifest to: {os.path.abspath(manifest_path)}")
    print("=" * 75)

if __name__ == "__main__":
    main()
