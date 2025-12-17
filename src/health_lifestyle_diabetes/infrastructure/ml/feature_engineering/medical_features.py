# src/health_lifestyle_diabetes/infrastructure/ml/feature_engineering/medical_features.py
import numpy as np
import pandas as pd
from pandas import DataFrame

from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)


class MedicalFeatureEngineer:
    """
    Gère l'ensemble des transformations médicales cliniques :
    glycémie, IMC, tension artérielle, résistance à l'insuline, etc.

    Objectif :
    ----------
    Créer des indicateurs médicaux explicables à partir de mesures brutes.

    Justification médicale :
    ------------------------
    Ces indicateurs sont basés sur les recommandations internationales :
    - ADA (glucose, HbA1c)
    - OMS (IMC, pression artérielle)
    - NCEP-ATP III (syndrome métabolique)

    Pertinence métier :
    -------------------
    Ces variables traduisent la dimension physiologique du risque diabétique
    et renforcent l’explicabilité des modèles prédictifs.
    """

    def __init__(self):
        self.logger = LoguruLoggerAdapter("fe.MedicalFeatureEngineer")

    def _compute_glucose_status(self, df: DataFrame) -> DataFrame:
        df["glucose_status"] = pd.cut(
            df["glucose_fasting"],
            bins=[0, 99, 125, np.inf],
            labels=["Normal", "Pre-Diabetes", "Diabetes"],
        )
        df["hba1c_category"] = pd.cut(
            df["hba1c"],
            bins=[0, 5.7, 6.4, np.inf],
            labels=["Normal", "Pre-Diabetes", "Diabetes"],
        )
        return df

    def _compute_homa_ir(self, df: DataFrame) -> DataFrame:
        df["HOMA_IR"] = (df["glucose_fasting"] * df["insulin_level"]) / 405
        df["insulin_resistance_flag"] = (df["HOMA_IR"] > 2.5).astype(int)
        return df

    def _compute_bmi_and_bp(self, df: DataFrame) -> DataFrame:
        df["bmi_category"] = pd.cut(
            df["bmi"],
            bins=[0, 18.5, 24.9, 29.9, np.inf],
            labels=["Underweight", "Normal", "Overweight", "Obese"],
        )

        def bp_cat(row):
            if row["systolic_bp"] < 120 and row["diastolic_bp"] < 80:
                return "Normal"
            elif (120 <= row["systolic_bp"] <= 139) or (
                80 <= row["diastolic_bp"] <= 89
            ):
                return "Pre-Hypertension"
            else:
                return "Hypertension"

        df["bp_category"] = df.apply(bp_cat, axis=1)
        return df

    def _compute_metabolic_syndrome(self, df: DataFrame) -> DataFrame:
        df["metabolic_syndrome_flag"] = (
            (
                (df["bmi"] >= 30).astype(int)
                + (df["systolic_bp"] >= 130).astype(int)
                + (df["triglycerides"] >= 150).astype(int)
                + (df["hdl_cholesterol"] < 40).astype(int)
                + (df["glucose_fasting"] >= 110).astype(int)
            )
            >= 3
        ).astype(int)
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Application des transformations médicales...")
        for step in [
            self._compute_glucose_status,
            self._compute_homa_ir,
            self._compute_bmi_and_bp,
            self._compute_metabolic_syndrome,
        ]:
            df = step(df)
        self.logger.info("Transformations médicales complétées.")
        return df
