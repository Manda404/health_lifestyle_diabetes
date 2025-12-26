# src/health_lifestyle_diabetes/infrastructure/ml/feature_engineering/clinical_features.py
import numpy as np
from pandas import DataFrame
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class ClinicalFeatureEngineer:
    """
    Gère les variables issues d'interactions physiologiques :
    ratios lipidiques, variation glycémique, interaction IMC × glycémie.

    Objectif :
    ----------
    Capturer les relations quantitatives entre biomarqueurs.

    Justification médicale :
    ------------------------
    Ces indicateurs traduisent l’équilibre métabolique (lipides, glucose)
    et les effets croisés de la surcharge pondérale.

    Pertinence métier :
    -------------------
    Permet d’identifier des profils complexes (ex. obésité sans dyslipidémie)
    utiles en prévention personnalisée.
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Calcul des ratios et interactions cliniques...")
        df["hdl_to_ldl_ratio"] = df["hdl_cholesterol"] / df["ldl_cholesterol"].replace(
            0, np.nan
        )
        df["cholesterol_ratio"] = df["cholesterol_total"] / df[
            "hdl_cholesterol"
        ].replace(0, np.nan)
        df["bmi_glucose_interaction"] = df["bmi"] * df["glucose_fasting"]
        df["glucose_diff"] = df["glucose_postprandial"] - df["glucose_fasting"]
        self.logger.info("Variables cliniques ajoutées avec succès.")
        return df
