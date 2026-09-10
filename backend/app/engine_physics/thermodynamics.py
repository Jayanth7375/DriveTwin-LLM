import numpy as np
import pandas as pd
from typing import Dict, Any

class ThermodynamicsEngine:
    """
    Thermodynamic & Fluid Mechanics Analysis Engine.
    Implements Ideal Gas Law, Volumetric Efficiency, Turbocharger Boost Ratio,
    and Dual-Bank Lambda balance equations.
    """
    def __init__(self, displacement_liters: float = 3.0, stoich_afr: float = 14.7):
        self.displacement_m3 = displacement_liters * 1e-3
        self.stoich_afr = stoich_afr
        self.R_air = 287.05  # J/(kg*K)
        
    def calculate_volumetric_efficiency(self, rpm: np.ndarray, map_kpa: np.ndarray) -> np.ndarray:
        """
        Empirical Volumetric Efficiency (VE) map function for I6 Turbo Engines.
        VE varies non-linearly with RPM and Manifold Pressure.
        """
        # Baseline VE curve peaking around 4000 RPM and 150 kPa MAP
        rpm_norm = np.clip(rpm / 4000.0, 0.2, 1.8)
        map_norm = np.clip(map_kpa / 100.0, 0.3, 2.5)
        
        ve = 0.85 * np.exp(-0.5 * ((rpm_norm - 1.0)**2)) * (0.8 + 0.2 * np.tanh(map_norm - 1.0))
        return np.clip(ve, 0.4, 0.98)

    def analyze_fluid_thermodynamics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes airflow, Diesel common rail fuel metering, VGT boost ratio, and thermal balance.
        """
        # 1. Mass Air Flow (MAF) vs Theoretical Ideal Flow
        rpm = df["RPM"].values if "RPM" in df.columns else np.full(len(df), 2000.0)
        map_kpa = df["MAP"].values if "MAP" in df.columns else np.full(len(df), 120.0)
        maf_actual = df["MAF"].values if "MAF" in df.columns else np.full(len(df), 25.0)       # g/s
        iat_c = df["IAT"].values if "IAT" in df.columns else np.full(len(df), 30.0)             # deg C
        
        # Convert IAT to Kelvin
        iat_k = iat_c + 273.15
        map_pa = map_kpa * 1000.0
        
        ve = self.calculate_volumetric_efficiency(rpm, map_kpa)
        
        # m_dot_theoretical (kg/s) = (V_d * RPM/60 * MAP * VE) / (2 * R * T)
        maf_theoretical_gs = ((self.displacement_m3 * (rpm / 60.0) * map_pa * ve) / (2 * self.R_air * iat_k)) * 1000.0
        
        maf_residual_ratio = float(np.mean((maf_actual - maf_theoretical_gs) / (maf_theoretical_gs + 1e-6)))
        
        # 2. Diesel Dual-Bank Lambda / AFR Variance (Typical Diesel Lean Lambda 1.2 to 2.2)
        lambda_b1 = df["Lambda_B1"].values if "Lambda_B1" in df.columns else np.full(len(df), 1.35)
        lambda_b2 = df["Lambda_B2"].values if "Lambda_B2" in df.columns else np.full(len(df), 1.35)
        
        lambda_bank_delta = float(np.mean(np.abs(lambda_b1 - lambda_b2)))
        bank1_mean = float(np.mean(lambda_b1))
        bank2_mean = float(np.mean(lambda_b2))
        
        # 3. Turbocharger Boost Pressure Ratio
        boost_pressure = df["Boost_Pressure"].values if "Boost_Pressure" in df.columns else map_kpa - 101.3
        boost_pressure = np.maximum(boost_pressure, 0.0)
        wastegate_duty = df["Wastegate_Duty"].values if "Wastegate_Duty" in df.columns else np.full(len(df), 50.0)
        
        pressure_ratio = (map_kpa + 1e-6) / 101.3
        expected_pr = 1.0 + (wastegate_duty / 100.0) * 1.2
        boost_residual = float(np.mean(pressure_ratio - expected_pr))
        
        # 4. Thermal Balance & Heat Rejection
        coolant_temp = df["Coolant_Temp"].values if "Coolant_Temp" in df.columns else np.full(len(df), 90.0)
        oil_temp = df["Oil_Temp"].values if "Oil_Temp" in df.columns else np.full(len(df), 95.0)
        
        thermal_delta = float(np.mean(oil_temp - coolant_temp))
        overheating = float(np.max(coolant_temp)) > 110.0
        
        return {
            "maf_actual_mean_gs": round(float(np.mean(maf_actual)), 2),
            "maf_theoretical_mean_gs": round(float(np.mean(maf_theoretical_gs)), 2),
            "maf_residual_ratio": round(maf_residual_ratio, 4),
            "lambda_bank_delta": round(lambda_bank_delta, 4),
            "lambda_bank1_mean": round(bank1_mean, 3),
            "lambda_bank2_mean": round(bank2_mean, 3),
            "boost_pressure_max_bar": round(float(np.max(boost_pressure)) / 100.0, 2),
            "boost_residual": round(boost_residual, 3),
            "thermal_delta_c": round(thermal_delta, 2),
            "max_coolant_temp_c": round(float(np.max(coolant_temp)), 1),
            "overheating_flag": overheating
        }
