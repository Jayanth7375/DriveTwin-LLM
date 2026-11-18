import os
import sys
import time
import glob
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from multiprocessing import Pool, cpu_count
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from app.config import settings
from app.engine_physics.feature_extractor import PhysicsFeatureExtractor
from app.ml_models.pinn_transformer import (
    ECUPINNTelemetryTransformer,
    PINNTrainerWrapper
)

DATASET_DIR = "d:/LLM Forge/dataset"
WEIGHTS_SAVE_PATH = "d:/LLM Forge/backend/app/ml_models/pinn_weights.pt"

LABELS = list(PINNTrainerWrapper.DTC_MAPPINGS.keys())
LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}

def process_single_file_for_transformer(args):
    file_path, label_id = args
    try:
        df = pd.read_csv(file_path)
        extractor = PhysicsFeatureExtractor()
        _, feat = extractor.extract(df)
        
        # Expand 14-dim physics feature into a sequence timeline of 10 timesteps for Transformer Multi-Head Attention
        seq = np.tile(feat, (10, 1)).astype(np.float32)
        return seq, label_id
    except Exception as e:
        return np.zeros((10, 14), dtype=np.float32), label_id

def main():
    print("=" * 75, flush=True)
    print("   PYTORCH PINN TELEMETRY TRANSFORMER & LLM ENGINE - 15 GB DATASET TRAINER", flush=True)
    print("=" * 75, flush=True)
    
    device = torch.device(settings.DEVICE)
    print(f"Hardware Compute Device: {device} ({settings.GPU_NAME})", flush=True)
    
    # 1. Discover CSV files
    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory '{DATASET_DIR}' not found!", flush=True)
        sys.exit(1)
        
    csv_files = glob.glob(os.path.join(DATASET_DIR, "*", "*.csv"))
    num_files = len(csv_files)
    print(f"Found {num_files:,} telemetry sequence files in '{DATASET_DIR}'", flush=True)
    
    if num_files == 0:
        print("Error: No CSV files found!", flush=True)
        sys.exit(1)
        
    tasks = []
    for fp in csv_files:
        folder = os.path.basename(os.path.dirname(fp))
        label_id = LABEL_TO_ID.get(folder, 0)
        tasks.append((fp, label_id))
        
    num_cpus = max(1, cpu_count())
    print(f"Extracting Physics Sequences across {num_cpus} CPU cores in parallel...", flush=True)
    
    load_start = time.time()
    X_list = []
    y_list = []
    
    with Pool(processes=num_cpus) as pool:
        completed = 0
        for seq, cid in pool.imap_unordered(process_single_file_for_transformer, tasks, chunksize=50):
            X_list.append(seq)
            y_list.append(cid)
            completed += 1
            if completed % 3000 == 0 or completed == num_files:
                print(f"Physics Feature Extraction Progress: {completed}/{num_files} files ({completed/num_files*100:.1f}%)", flush=True)
                
    X_arr = np.array(X_list, dtype=np.float32)
    y_arr = np.array(y_list, dtype=np.int64)
    
    # Normalize features across dataset channels
    means = np.mean(X_arr, axis=(0, 1), keepdims=True)
    stds = np.std(X_arr, axis=(0, 1), keepdims=True) + 1e-5
    X_arr = (X_arr - means) / stds
    
    print(f"Parallel Extraction Completed in {time.time() - load_start:.2f} seconds. Physics Tensor Shape: {X_arr.shape}", flush=True)
    
    # 2. Train / Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_arr, y_arr, test_size=0.20, random_state=42, stratify=y_arr
    )
    
    print(f"Training Set: {X_train.shape[0]:,} sequences | Test Set: {X_test.shape[0]:,} sequences", flush=True)
    
    train_dataset = TensorDataset(torch.tensor(X_train), torch.tensor(y_train))
    test_dataset = TensorDataset(torch.tensor(X_test), torch.tensor(y_test))
    
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    
    # 3. Instantiate Transformer Model & Optimizer
    print("\nInitializing ECUPINNTelemetryTransformer (3-Layer Encoder, Multi-Head Self-Attention)...", flush=True)
    model = ECUPINNTelemetryTransformer(in_channels=14, d_model=64, nhead=4, num_layers=3, num_classes=8).to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)
    criterion = nn.CrossEntropyLoss()
    
    # 4. Training Loop
    epochs = 20
    print(f"\nStarting PyTorch Transformer Training for {epochs} Epochs on 15 GB Dataset...", flush=True)
    start_time = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            logits, _ = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * batch_x.size(0)
            preds = torch.argmax(logits, dim=1)
            correct += (preds == batch_y).sum().item()
            total += batch_y.size(0)
            
        scheduler.step()
        train_acc = (correct / total) * 100.0
        avg_loss = running_loss / total
        
        # Test Evaluation
        model.eval()
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for test_x, test_y in test_loader:
                test_x, test_y = test_x.to(device), test_y.to(device)
                t_logits, _ = model(test_x)
                t_preds = torch.argmax(t_logits, dim=1)
                test_correct += (t_preds == test_y).sum().item()
                test_total += test_y.size(0)
                
        test_acc = (test_correct / test_total) * 100.0
        print(f"Epoch [{epoch:02d}/{epochs:02d}] | Loss: {avg_loss:.4f} | Train Acc: {train_acc:.2f}% | Test Acc: {test_acc:.2f}%", flush=True)
        
    elapsed = time.time() - start_time
    print(f"\nTransformer Training Finished in {elapsed:.2f} seconds.", flush=True)
    
    # 5. Save Trained Transformer Weights
    os.makedirs(os.path.dirname(WEIGHTS_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), WEIGHTS_SAVE_PATH)
    print(f"Successfully saved PyTorch PINN Transformer weights to:\n  -> {os.path.abspath(WEIGHTS_SAVE_PATH)}", flush=True)
    print("=" * 75, flush=True)

if __name__ == "__main__":
    main()
