import os
import sys
import time
import json
import shutil
import numpy as np
import pandas as pd
from multiprocessing import Pool, cpu_count

DATASET_ROOT = "d:/LLM Forge/dataset"

FAULT_TYPES = [
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

def generate_ecu_batch(args):
    file_id, fault_type, num_samples, split_name, seed = args
    np.random.seed(seed)
    
    time_arr = np.linspace(0, 200, num_samples)
    
    # Diesel I6 Base Telemetry Signal (6.7L Platform)
    base_rpm = 1800.0 + 1200.0 * np.sin(time_arr / 12.0) + np.random.normal(0, 12, num_samples)
    map_kpa = 110.0 + (base_rpm / 3500.0) * 120.0 + np.random.normal(0, 2.5, num_samples)
    maf = (base_rpm / 1000.0) * 18.0 + np.random.normal(0, 0.6, num_samples)
    
    # 6-Cylinder Crank Accelerations (I6 Firing Order 1-5-3-6-2-4)
    crank_accel = {f"Crank_Accel_C{i}": 18.0 + np.random.normal(0, 0.5, num_samples) for i in range(1, 7)}
    
    # Diesel Lean Lambda (1.25 to 2.2)
    lambda_b1 = 1.35 + np.random.normal(0, 0.015, num_samples)
    lambda_b2 = 1.35 + np.random.normal(0, 0.015, num_samples)
    
    boost_press = map_kpa - 101.3
    boost_press = np.maximum(boost_press, 0.0)
    wastegate_duty = (boost_press / 150.0) * 70.0 + 15.0
    
    coolant_temp = 86.0 + (time_arr / 200.0) * 8.0 + np.random.normal(0, 0.2, num_samples)
    oil_temp = 90.0 + (time_arr / 200.0) * 10.0 + np.random.normal(0, 0.2, num_samples)
    iat = 28.0 + np.random.normal(0, 0.4, num_samples)
    
    # Apply Fault Physics Dynamics
    if fault_type == "CYL_3_IGNITION_MISFIRE":
        crank_accel["Crank_Accel_C3"] -= 7.5 + np.random.normal(0, 0.9, num_samples)
        base_rpm += np.random.normal(0, 75.0, num_samples)
        lambda_b1 += 0.12
    elif fault_type == "CYL_5_INJECTOR_CLOGGING":
        crank_accel["Crank_Accel_C5"] -= 5.0 + np.random.normal(0, 0.6, num_samples)
        lambda_b2 += 0.18
    elif fault_type == "TURBO_BOOST_LEAK":
        boost_press *= 0.40
        wastegate_duty = np.full(num_samples, 98.0)
        maf *= 0.70
    elif fault_type == "MAF_SENSOR_DRIFT":
        maf *= 1.40
        lambda_b1 -= 0.08
        lambda_b2 -= 0.08
    elif fault_type == "EGR_VALVE_STUCK_OPEN":
        map_kpa *= 0.75
        maf *= 0.65
        for i in range(1, 7):
            crank_accel[f"Crank_Accel_C{i}"] -= 2.2
    elif fault_type == "HEAD_GASKET_BREACH":
        coolant_temp += (time_arr / 200.0) * 32.0
        oil_temp += (time_arr / 200.0) * 20.0
        crank_accel["Crank_Accel_C2"] -= 3.5
        crank_accel["Crank_Accel_C3"] -= 3.5
    elif fault_type == "HPFP_PRESSURE_DROP":
        lambda_b1 += 0.25
        lambda_b2 += 0.25
        for i in range(1, 7):
            crank_accel[f"Crank_Accel_C{i}"] -= 2.5

    df = pd.DataFrame({
        "Time_s": np.round(time_arr, 2),
        "RPM": np.round(base_rpm, 1),
        "MAP": np.round(map_kpa, 1),
        "MAF": np.round(maf, 2),
        **{k: np.round(v, 2) for k, v in crank_accel.items()},
        "Lambda_B1": np.round(lambda_b1, 3),
        "Lambda_B2": np.round(lambda_b2, 3),
        "Boost_Pressure": np.round(boost_press, 1),
        "Wastegate_Duty": np.round(wastegate_duty, 1),
        "Coolant_Temp": np.round(coolant_temp, 1),
        "Oil_Temp": np.round(oil_temp, 1),
        "IAT": np.round(iat, 1),
        "Fault_Label": fault_type
    })
    
    target_dir = os.path.join(DATASET_ROOT, split_name, fault_type)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, f"ecu_30gb_log_{file_id:05d}.csv")
    df.to_csv(file_path, index=False)
    
    return os.path.getsize(file_path), split_name, fault_type

def main():
    print("=" * 75)
    print("      DIESEL I6 ECU 30.0 GB DATASET PARALLEL GENERATOR & ORGANIZER")
    print("=" * 75)
    
    num_cpus = max(1, cpu_count())
    print(f"Using {num_cpus} CPU cores for parallel 30 GB dataset synthesis...")
    
    start_time = time.time()
    
    # 24,000 CSV files of 10,000 telemetry rows each (~1.27 MB per file) = 30.48 GB total
    num_files = 24000
    rows_per_file = 10000
    
    # Stratified Split Distribution
    # 70% Train (16,800 files), 15% Validate (3,600 files), 15% Test (3,600 files)
    tasks = []
    for i in range(num_files):
        fault = FAULT_TYPES[i % len(FAULT_TYPES)]
        # Deterministic split allocation per batch element
        mod_100 = i % 100
        if mod_100 < 70:
            split_name = "train"
        elif mod_100 < 85:
            split_name = "validate"
        else:
            split_name = "test"
            
        tasks.append((i + 1, fault, rows_per_file, split_name, 30000 + i))
        
    total_bytes = 0
    split_counts = {"train": 0, "validate": 0, "test": 0}

    with Pool(processes=num_cpus) as pool:
        completed = 0
        for size, split_name, fault_type in pool.imap_unordered(generate_ecu_batch, tasks, chunksize=25):
            total_bytes += size
            split_counts[split_name] += 1
            completed += 1
            if completed % 1200 == 0 or completed == num_files:
                curr_mb = total_bytes / (1024 * 1024)
                curr_gb = total_bytes / (1024 * 1024 * 1024)
                print(f"30 GB Generation Progress: {completed}/{num_files} files ({completed/num_files*100:.1f}%) -> {curr_gb:.2f} GB ({curr_mb:.1f} MB)")
        
    elapsed = time.time() - start_time
    total_mb = total_bytes / (1024 * 1024)
    total_gb = total_bytes / (1024 * 1024 * 1024)
    
    # Recalculate total files in dataset/train, dataset/validate, dataset/test
    all_summary = {"train": {}, "validate": {}, "test": {}}
    grand_total_files = 0
    for split in ["train", "validate", "test"]:
        for cls in FAULT_TYPES:
            cpath = os.path.join(DATASET_ROOT, split, cls)
            cnt = len(os.listdir(cpath)) if os.path.exists(cpath) else 0
            all_summary[split][cls] = cnt
            grand_total_files += cnt

    # Save manifest
    manifest_path = os.path.join(DATASET_ROOT, "dataset_summary.json")
    manifest = {
        "dataset_name": "Diesel I6 High-Frequency Expanded Telemetry Dataset",
        "total_files": grand_total_files,
        "newly_added_30gb_files": num_files,
        "splits_ratio": "70% Train / 15% Validate / 15% Test",
        "split_counts": {
            "train_total": sum(all_summary["train"].values()),
            "validate_total": sum(all_summary["validate"].values()),
            "test_total": sum(all_summary["test"].values())
        },
        "per_class_summary": all_summary
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 75)
    print(f"SUCCESSFULLY ADDED 30.0 GB NEW DATASET TO WORKSPACE!")
    print(f"Target Directory : {os.path.abspath(DATASET_ROOT)}")
    print(f"New Files Added  : {num_files:,} CSV files ({total_gb:.2f} GB)")
    print(f"Grand Total      : {grand_total_files:,} CSV files across train/validate/test")
    print(f"  • Train Set    : {manifest['split_counts']['train_total']:,} files")
    print(f"  • Validate Set : {manifest['split_counts']['validate_total']:,} files")
    print(f"  • Test Set     : {manifest['split_counts']['test_total']:,} files")
    print(f"Generation Time  : {elapsed:.2f} seconds ({total_mb / elapsed:.1f} MB/s)")
    print("=" * 75)

if __name__ == "__main__":
    main()
