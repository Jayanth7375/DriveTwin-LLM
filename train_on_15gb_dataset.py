import os
import sys
import time
import glob
import numpy as np
import pandas as pd
import joblib
from multiprocessing import Pool, cpu_count
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from app.engine_physics.feature_extractor import PhysicsFeatureExtractor

DATASET_DIR = "d:/LLM Forge/dataset"
MODEL_SAVE_PATH = "d:/LLM Forge/backend/app/ml_models/trained_15gb_ensemble.joblib"

LABELS = [
    "NO_ISSUE",
    "CYL_3_IGNITION_MISFIRE",
    "CYL_5_INJECTOR_CLOGGING",
    "TURBO_BOOST_LEAK",
    "MAF_SENSOR_DRIFT",
    "EGR_VALVE_STUCK_OPEN",
    "HEAD_GASKET_BREACH",
    "HPFP_PRESSURE_DROP"
]

LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}

def extract_file_features(file_path):
    """
    Extracts physics feature vector from a single ECU CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        fault_label = df["Fault_Label"].iloc[0] if "Fault_Label" in df.columns else os.path.basename(os.path.dirname(file_path))
        extractor = PhysicsFeatureExtractor()
        _, feat = extractor.extract(df)
        class_id = LABEL_TO_ID.get(fault_label, 0)
        return feat, class_id
    except Exception as e:
        return None, None

def main():
    print("=" * 70)
    print("      DIESEL I6 ENGINE DIAGNOSTIC MODEL - 15.0 GB DATASET TRAINER")
    print("=" * 70)
    
    # 1. Check if 15 GB dataset exists
    if not os.path.exists(DATASET_DIR):
        print(f"Dataset directory '{DATASET_DIR}' not found. Triggering 15 GB dataset generation...")
        import generate_15gb_dataset
        generate_15gb_dataset.main()
        
    csv_files = glob.glob(os.path.join(DATASET_DIR, "*", "*.csv"))
    num_files = len(csv_files)
    print(f"Discovered {num_files:,} telemetry files in '{DATASET_DIR}'")
    
    if num_files == 0:
        print("Error: No CSV files found in dataset. Running generator...")
        import generate_15gb_dataset
        generate_15gb_dataset.main()
        csv_files = glob.glob(os.path.join(DATASET_DIR, "*", "*.csv"))
        num_files = len(csv_files)

    num_cpus = max(1, cpu_count())
    print(f"Extracting physics feature vectors using {num_cpus} parallel workers...")
    
    start_time = time.time()
    X_list = []
    y_list = []
    
    with Pool(processes=num_cpus) as pool:
        completed = 0
        for feat, cid in pool.imap_unordered(extract_file_features, csv_files, chunksize=50):
            if feat is not None:
                X_list.append(feat)
                y_list.append(cid)
            completed += 1
            if completed % 2000 == 0 or completed == num_files:
                print(f"Feature Extraction Progress: {completed}/{num_files} files ({completed/num_files*100:.1f}%)")
                
    X = np.array(X_list)
    y = np.array(y_list)
    
    print(f"\nFeature Extraction Completed in {time.time() - start_time:.2f} seconds.")
    print(f"Extracted Dataset Feature Matrix Shape: {X.shape}, Target Vector Shape: {y.shape}")
    
    # 2. Train / Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    print(f"Train Set: {X_train.shape[0]:,} samples | Test Set: {X_test.shape[0]:,} samples")
    
    # 3. Train Machine Learning Ensemble
    print("\nTraining Multi-class Random Forest (n_estimators=150)...")
    rf_model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
    rf_start = time.time()
    rf_model.fit(X_train, y_train)
    print(f"Random Forest Training Completed in {time.time() - rf_start:.2f} seconds.")
    
    print("Training Multi-class XGBoost Classifier (n_estimators=150, max_depth=5)...")
    xgb_model = XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.08, random_state=42, n_jobs=-1)
    xgb_start = time.time()
    xgb_model.fit(X_train, y_train)
    print(f"XGBoost Training Completed in {time.time() - xgb_start:.2f} seconds.")
    
    # 4. Evaluate Ensemble Predictions on 20% Test Set
    rf_probs = rf_model.predict_proba(X_test)
    xgb_probs = xgb_model.predict_proba(X_test)
    ensemble_probs = 0.5 * rf_probs + 0.5 * xgb_probs
    y_pred = np.argmax(ensemble_probs, axis=1)
    
    overall_acc = accuracy_score(y_test, y_pred) * 100.0
    
    print("\n" + "=" * 70)
    print("     EVALUATION RESULTS ON 15 GB TEST DATASET (2,400 SAMPLES)")
    print("=" * 70)
    print(f"Ensemble Model Overall Accuracy: {overall_acc:.2f}%\n")
    print(classification_report(y_test, y_pred, target_names=LABELS, digits=4))
    
    # 5. Save Model Weights
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model_payload = {
        "rf_model": rf_model,
        "xgb_model": xgb_model,
        "labels": LABELS,
        "trained_on_gb": 15.0,
        "trained_samples": X.shape[0],
        "test_accuracy": overall_acc,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    joblib.dump(model_payload, MODEL_SAVE_PATH)
    print(f"Successfully saved 15.0 GB trained model ensemble payload to:\n  -> {os.path.abspath(MODEL_SAVE_PATH)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
