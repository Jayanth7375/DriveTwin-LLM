import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from .i6_kinematics import I6KinematicsEngine
from .thermodynamics import ThermodynamicsEngine

class PhysicsFeatureExtractor:
    """
    Unified Physics Feature Extractor.
    Takes raw ECU log dataframes and produces enriched physics metrics
    used for ML classification and RAG prompt construction.
    """
    def __init__(self):
        self.kinematics = I6KinematicsEngine()
        self.thermodynamics = ThermodynamicsEngine()

    def extract(self, df: pd.DataFrame) -> Tuple[Dict[str, Any], np.ndarray]:
        """
        Processes dataframe and returns (physics_summary_dict, ml_feature_vector).
        """
        # Ensure column names are standardized
        df = df.rename(columns=lambda x: str(x).strip())
        
        # 1. Kinematics metrics
        kin_results = self.kinematics.analyze_crankshaft_dynamics(df)
        
        # 2. Thermodynamics metrics
        thermo_results = self.thermodynamics.analyze_fluid_thermodynamics(df)
        
        # Combined summary
        physics_summary = {
            **kin_results,
            **thermo_results
        }
        
        # 3. Construct 14-element ML Feature Vector
        cpi = kin_results["cpi_scores"]
        feature_vector = np.array([
            cpi.get("CPI_Cyl_1", 0.0),
            cpi.get("CPI_Cyl_2", 0.0),
            cpi.get("CPI_Cyl_3", 0.0),
            cpi.get("CPI_Cyl_4", 0.0),
            cpi.get("CPI_Cyl_5", 0.0),
            cpi.get("CPI_Cyl_6", 0.0),
            kin_results["speed_fluctuation_index_pct"],
            thermo_results["maf_residual_ratio"],
            thermo_results["lambda_bank_delta"],
            thermo_results["lambda_bank1_mean"],
            thermo_results["lambda_bank2_mean"],
            thermo_results["boost_residual"],
            thermo_results["thermal_delta_c"],
            1.0 if thermo_results["overheating_flag"] else 0.0
        ], dtype=np.float32)
        
        return physics_summary, feature_vector
