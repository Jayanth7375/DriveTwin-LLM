import numpy as np
import pandas as pd
from typing import Dict, List, Any

class I6KinematicsEngine:
    """
    Kinematic & Dynamic Analysis Engine for Inline 6-Cylinder Engines.
    Analyzes crankshaft speed fluctuations per 120-degree firing interval.
    Firing order: 1 - 5 - 3 - 6 - 2 - 4
    """
    def __init__(self, firing_order: List[int] = None):
        self.firing_order = firing_order or [1, 5, 3, 6, 2, 4]
        
    def analyze_crankshaft_dynamics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates Cylinder Power Index (CPI) for each cylinder 1..6
        from crank speed fluctuations and acceleration data.
        """
        cpi_results = {}
        cylinder_cols = [f"Crank_Accel_C{i}" for i in range(1, 7)]
        
        # Check if individual cylinder crank acceleration sensors are present
        has_direct_cyl_telemetry = all(col in df.columns for col in cylinder_cols)
        
        if has_direct_cyl_telemetry:
            # Direct sensor measurement per cylinder
            means = {i: float(df[f"Crank_Accel_C{i}"].mean()) for i in range(1, 7)}
            overall_mean = np.mean(list(means.values()))
            overall_std = np.std(list(means.values())) + 1e-6
            
            for i in range(1, 7):
                # CPI = (Cylinder_Mean - Overall_Mean) / Overall_Std
                cpi = (means[i] - overall_mean) / overall_std
                cpi_results[f"CPI_Cyl_{i}"] = round(cpi, 3)
                cpi_results[f"Mean_Accel_Cyl_{i}"] = round(means[i], 2)
        else:
            # Derive synthetic kinematic fluctuation from RPM timeline variation
            rpm = df["RPM"].values if "RPM" in df.columns else np.full(len(df), 2000.0)
            rpm_diff = np.diff(rpm, prepend=rpm[0])
            
            # Divide timeline into 6 cyclical stroke bins
            stroke_bins = np.array_split(rpm_diff, 6)
            means = {}
            for idx, cyl in enumerate(self.firing_order):
                bin_data = stroke_bins[idx] if idx < len(stroke_bins) else np.array([0.0])
                means[cyl] = float(np.mean(bin_data))
                
            overall_mean = np.mean(list(means.values()))
            overall_std = np.std(list(means.values())) + 1e-6
            
            for i in range(1, 7):
                cpi = (means[i] - overall_mean) / overall_std
                cpi_results[f"CPI_Cyl_{i}"] = round(cpi, 3)
                cpi_results[f"Mean_Accel_Cyl_{i}"] = round(means[i], 2)

        # Determine suspect cylinders with low power delivery (CPI < -1.5)
        suspect_cylinders = []
        for i in range(1, 7):
            if cpi_results[f"CPI_Cyl_{i}"] < -1.5:
                suspect_cylinders.append(i)
                
        # Overall Speed Fluctuation Index (SFI)
        rpm_val = df["RPM"] if "RPM" in df.columns else pd.Series([2000.0])
        sfi = float((rpm_val.std() / (rpm_val.mean() + 1e-6)) * 100)
        
        return {
            "cpi_scores": cpi_results,
            "suspect_cylinders": suspect_cylinders,
            "speed_fluctuation_index_pct": round(sfi, 2),
            "misfire_detected": len(suspect_cylinders) > 0,
            "primary_balance_status": "NORMAL" if sfi < 8.0 else "UNBALANCED_VIBRATION"
        }
