import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple, List
import os

from ..config import settings

class PositionalEncoding1D(nn.Module):
    """
    Sinusoidal Positional Encoding for Temporal ECU Telemetry Sequences.
    """
    def __init__(self, d_model: int, max_len: int = 1000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]


class ECUPINNTelemetryTransformer(nn.Module):
    """
    Custom Physics-Informed Neural Network (PINN) & Telemetry Transformer built from scratch.
    Processes multi-channel high-frequency ECU telemetry timelines using 1D Convolutions
    and Multi-Head Self-Attention layers.
    """
    def __init__(
        self,
        in_channels: int = 14,
        d_model: int = 64,
        nhead: int = 4,
        num_layers: int = 3,
        num_classes: int = 8
    ):
        super().__init__()
        self.in_channels = in_channels
        self.d_model = d_model
        
        # 1. 1D Temporal Convolution Projection Layer
        self.conv_proj = nn.Conv1d(in_channels, d_model, kernel_size=3, padding=1)
        self.pos_encoder = PositionalEncoding1D(d_model)
        
        # 2. Multi-Head Self-Attention Encoder Stack
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=0.1,
            activation='gelu',
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 3. Physics-Aware Diagnostic Classification Head
        self.classifier_head = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(64, num_classes)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x_trans = x.transpose(1, 2)
        proj = self.conv_proj(x_trans).transpose(1, 2)
        x_pos = self.pos_encoder(proj)
        attn_features = self.transformer_encoder(x_pos)
        pooled = torch.mean(attn_features, dim=1)
        logits = self.classifier_head(pooled)
        return logits, attn_features


class PhysicsInformedLoss(nn.Module):
    """
    PINN Loss Function combining CrossEntropy Classification Loss
    with Diesel Thermodynamic & Kinetic Energy Balance Constraints.
    """
    def __init__(self, lambda_air: float = 0.15, lambda_torque: float = 0.10):
        super().__init__()
        self.ce_loss = nn.CrossEntropyLoss()
        self.lambda_air = lambda_air
        self.lambda_torque = lambda_torque

    def forward(
        self,
        logits: torch.Tensor,
        targets: torch.Tensor,
        raw_sequences: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        l_ce = self.ce_loss(logits, targets)
        
        # Airflow ideal gas physics constraint
        rpm = raw_sequences[:, :, 0]
        map_kpa = raw_sequences[:, :, 1]
        maf = raw_sequences[:, :, 2]
        
        air_proxy = (rpm / 1000.0) * (map_kpa / 100.0) * 12.0
        l_air = torch.mean(torch.square((maf - air_proxy) / (air_proxy + 1e-4)))
        
        # Kinematic torque conservation constraint Sum(CPI_1..6) = 0
        c1_c6 = raw_sequences[:, :, 4:10]
        cpi_sum = torch.sum(c1_c6, dim=2)
        cpi_mean_target = torch.mean(c1_c6, dim=(1, 2), keepdim=True)
        l_torque = torch.mean(torch.square(cpi_sum - 6.0 * cpi_mean_target.squeeze(-1)))
        
        total_loss = l_ce + self.lambda_air * l_air + self.lambda_torque * l_torque
        
        return total_loss, {
            "ce_loss": float(l_ce.item()),
            "air_physics_loss": float(l_air.item()),
            "torque_physics_loss": float(l_torque.item()),
            "total_loss": float(total_loss.item())
        }


class PINNTrainerWrapper:
    """
    Wrapper for training, fine-tuning, loading, and performing inference with
    the Custom PyTorch PINN Telemetry Transformer on SAE DTC Fault Codes.
    """
    DTC_MAPPINGS = {
        "NO_ISSUE": "SYSTEM_NOMINAL",
        "CYL_3_IGNITION_MISFIRE": "P0303 - Cylinder 3 Misfire",
        "CYL_5_INJECTOR_CLOGGING": "P0275 - Cylinder 5 Injector Contribution",
        "TURBO_BOOST_LEAK": "P0299 - Turbocharger Underboost",
        "MAF_SENSOR_DRIFT": "P0101 - MAF Sensor Range/Performance",
        "EGR_VALVE_STUCK_OPEN": "P0401 - EGR Flow Insufficient / Stuck Open",
        "HEAD_GASKET_BREACH": "P0217 - Engine Coolant Over-Temperature",
        "HPFP_PRESSURE_DROP": "P0087 - Fuel Rail Pressure Too Low"
    }

    def __init__(self):
        self.device = torch.device(settings.DEVICE)
        self.model = ECUPINNTelemetryTransformer().to(self.device)
        self.is_trained = False
        self.weights_path = os.path.join(os.path.dirname(__file__), "pinn_weights.pt")
        
        if os.path.exists(self.weights_path):
            try:
                self.model.load_state_dict(torch.load(self.weights_path, map_location=self.device))
                self.model.eval()
                self.is_trained = True
            except Exception as e:
                print(f"[PINN Trainer] Weight load notice: {e}")
                self.train_pinn_from_scratch()
        else:
            self.train_pinn_from_scratch()

    def train_pinn_from_scratch(self, epochs: int = 25):
        """
        Trains/Fine-tunes PyTorch PINN Transformer on SAE DTC fault codes & telemetry sequences.
        """
        from .synthetic_generator import ECUSyntheticGenerator
        generator = ECUSyntheticGenerator()
        
        labels = list(self.DTC_MAPPINGS.keys())
        label_to_id = {l: i for i, l in enumerate(labels)}
        
        X_seqs = []
        y_seqs = []
        
        # Build 45 training sequence iterations per DTC class
        for l in labels:
            cid = label_to_id[l]
            for s in range(45):
                df = generator.generate(fault_type=l, num_samples=100)
                cols = ["RPM", "MAP", "MAF", "Boost_Pressure", 
                        "Crank_Accel_C1", "Crank_Accel_C2", "Crank_Accel_C3",
                        "Crank_Accel_C4", "Crank_Accel_C5", "Crank_Accel_C6",
                        "Lambda_B1", "Lambda_B2", "Coolant_Temp", "Oil_Temp"]
                vals = df[cols].values.astype(np.float32)
                vals = (vals - np.mean(vals, axis=0)) / (np.std(vals, axis=0) + 1e-5)
                X_seqs.append(vals)
                y_seqs.append(cid)
                
        X_tensor = torch.tensor(np.array(X_seqs), dtype=torch.float32).to(self.device)
        y_tensor = torch.tensor(np.array(y_seqs), dtype=torch.long).to(self.device)
        
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3, weight_decay=1e-4)
        criterion = PhysicsInformedLoss()
        
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            logits, _ = self.model(X_tensor)
            loss, loss_dict = criterion(logits, y_tensor, X_tensor)
            loss.backward()
            optimizer.step()
            
        self.model.eval()
        self.is_trained = True
        try:
            torch.save(self.model.state_dict(), self.weights_path)
        except Exception:
            pass
        return {"status": "trained", "epochs": epochs, "final_loss": loss_dict}

    def predict_sequence(self, df) -> Dict[str, Any]:
        """
        Runs PyTorch PINN inference and returns SAE DTC code mapping.
        """
        cols = ["RPM", "MAP", "MAF", "Boost_Pressure", 
                "Crank_Accel_C1", "Crank_Accel_C2", "Crank_Accel_C3",
                "Crank_Accel_C4", "Crank_Accel_C5", "Crank_Accel_C6",
                "Lambda_B1", "Lambda_B2", "Coolant_Temp", "Oil_Temp"]
                
        for col in cols:
            if col not in df.columns:
                df[col] = 100.0 if "Temp" in col else (1.35 if "Lambda" in col else 15.0)
                
        vals = df[cols].values.astype(np.float32)
        vals = (vals - np.mean(vals, axis=0)) / (np.std(vals, axis=0) + 1e-5)
        
        if len(vals) > 100:
            indices = np.linspace(0, len(vals) - 1, 100, dtype=int)
            vals = vals[indices]
        elif len(vals) < 100:
            pad = np.repeat(vals[-1:], 100 - len(vals), axis=0)
            vals = np.vstack([vals, pad])
            
        X_in = torch.tensor(vals, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            logits, attn_feats = self.model(X_in)
            probs = F.softmax(logits, dim=1)[0].cpu().numpy()
            
        top_idx = int(np.argmax(probs))
        top_prob = float(probs[top_idx])
        
        labels = list(self.DTC_MAPPINGS.keys())
        top_fault = labels[top_idx]
        dtc_code = self.DTC_MAPPINGS[top_fault]
        
        return {
            "pinn_top_class": top_fault,
            "sae_dtc_code": dtc_code,
            "pinn_confidence_score": round(top_prob * 100.0, 1),
            "pinn_probabilities": {labels[i]: round(float(probs[i]), 4) for i in range(len(labels))},
            "pinn_device": str(self.device).upper()
        }
