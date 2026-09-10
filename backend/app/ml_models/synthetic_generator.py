import numpy as np
import pandas as pd
from typing import Dict, Any

class ECUSyntheticGenerator:
    """
    Realistic ECU Telemetry Generator for 6-Cylinder Inline Engines.
    Synthesizes sensor timelines (RPM, MAP, MAF, Crank Accel, Lambda, Boost, Temp)
    for healthy engines and specific injected engine faults.
    """
    FAULT_TYPES = {
        "NO_ISSUE": "Normal Healthy Engine Operation",
        "CYL_3_IGNITION_MISFIRE": "Cylinder 3 Ignition Coil / Spark Plug Failure",
        "CYL_5_INJECTOR_CLOGGING": "Cylinder 5 Fuel Injector Restriction",
        "TURBO_BOOST_LEAK": "Intake Charge Pipe / Intercooler Boost Pressure Leak",
        "MAF_SENSOR_DRIFT": "Mass Air Flow Sensor Positive Calibration Drift",
        "EGR_VALVE_STUCK_OPEN": "EGR Valve Stuck Open (Excessive Inert Gas Recirculation)",
        "HEAD_GASKET_BREACH": "Head Gasket Coolant Channel Leak (Thermal Anomaly)",
        "HPFP_PRESSURE_DROP": "High Pressure Fuel Pump Rail Pressure Drop"
    }

    def generate(self, fault_type: str = "NO_ISSUE", num_samples: int = 300) -> pd.DataFrame:
        if fault_type not in self.FAULT_TYPES:
            fault_type = "NO_ISSUE"
            
        np.random.seed(42)
        time = np.linspace(0, 30, num_samples)
        
        # Base RPM sweep from 1500 to 5000 RPM
        base_rpm = 2000.0 + 1500.0 * np.sin(time / 5.0) + np.random.normal(0, 15, num_samples)
        map_kpa = 100.0 + (base_rpm / 5000.0) * 80.0 + np.random.normal(0, 2.0, num_samples)
        
        # Baseline air mass flow g/s
        maf = (base_rpm / 1000.0) * 12.5 + np.random.normal(0, 0.5, num_samples)
        
        # Individual Cylinder Crank Accelerations (Healthy baseline around 15.0 rad/s^2)
        crank_accel = {f"Crank_Accel_C{i}": 15.0 + np.random.normal(0, 0.4, num_samples) for i in range(1, 7)}
        
        lambda_b1 = np.ones(num_samples) + np.random.normal(0, 0.01, num_samples)
        lambda_b2 = np.ones(num_samples) + np.random.normal(0, 0.01, num_samples)
        
        boost_press = map_kpa - 101.3
        boost_press = np.maximum(boost_press, 0.0)
        wastegate_duty = (boost_press / 100.0) * 60.0 + 20.0
        
        coolant_temp = 88.0 + (time / 30.0) * 4.0 + np.random.normal(0, 0.2, num_samples)
        oil_temp = 92.0 + (time / 30.0) * 5.0 + np.random.normal(0, 0.2, num_samples)
        iat = 25.0 + np.random.normal(0, 0.3, num_samples)
        
        # --- Apply Specific Fault Mutators ---
        if fault_type == "CYL_3_IGNITION_MISFIRE":
            # Significant drop in Cylinder 3 acceleration
            crank_accel["Crank_Accel_C3"] -= 6.5 + np.random.normal(0, 0.8, num_samples)
            base_rpm += np.random.normal(0, 60.0, num_samples)  # Rough idle
            lambda_b1 += 0.08  # Unburnt oxygen causing lean reading on Bank 1 (Cyl 1-3)
            
        elif fault_type == "CYL_5_INJECTOR_CLOGGING":
            # Moderate drop in Cylinder 5 acceleration + lean reading on Bank 2 (Cyl 4-6)
            crank_accel["Crank_Accel_C5"] -= 4.2 + np.random.normal(0, 0.5, num_samples)
            lambda_b2 += 0.12
            
        elif fault_type == "TURBO_BOOST_LEAK":
            # Boost pressure drops, wastegate duty cycle climbs to max (95%)
            boost_press *= 0.45
            wastegate_duty = np.full(num_samples, 95.0)
            maf *= 0.75
            
        elif fault_type == "MAF_SENSOR_DRIFT":
            # MAF reads artificially high (+35%) compared to actual engine air intake
            maf *= 1.35
            lambda_b1 -= 0.05
            lambda_b2 -= 0.05
            
        elif fault_type == "EGR_VALVE_STUCK_OPEN":
            # Excess inert gas drops MAP and causes minor acceleration dip on all cylinders
            map_kpa *= 0.78
            maf *= 0.70
            for i in range(1, 7):
                crank_accel[f"Crank_Accel_C{i}"] -= 1.8
                
        elif fault_type == "HEAD_GASKET_BREACH":
            # Rapid rise in coolant temp and thermal delta
            coolant_temp += (time / 30.0) * 28.0  # Climbs past 116 C
            oil_temp += (time / 30.0) * 15.0
            crank_accel["Crank_Accel_C2"] -= 3.0
            crank_accel["Crank_Accel_C3"] -= 3.0
            
        elif fault_type == "HPFP_PRESSURE_DROP":
            # Lean spike across both banks under boost
            lambda_b1 += 0.18
            lambda_b2 += 0.18
            for i in range(1, 7):
                crank_accel[f"Crank_Accel_C{i}"] -= 2.0

        # Build DataFrame
        df = pd.DataFrame({
            "Time_s": np.round(time, 2),
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
            "IAT": np.round(iat, 1)
        })
        
        return df
