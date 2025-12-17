import numpy as np
from pandas import DataFrame
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)


class MetabolicFeatureEngineer:
    """
    Génère des indicateurs métaboliques avancés à partir des biomarqueurs
    glycémiques, lipidiques et anthropométriques.

    Objectif :
    ----------
    Capturer la charge métabolique globale et le cumul de facteurs de risque
    cardio-métaboliques associés au diabète de type 2.

    Justification médicale :
    ------------------------
    Le diabète est rarement expliqué par un seul biomarqueur, mais par
    l'accumulation de déséquilibres :
    - surcharge pondérale
    - dyslipidémie
    - hypertension
    - hyperglycémie

    Ces indicateurs s'inspirent des recommandations :
    - NCEP-ATP III
    - OMS
    - ADA (American Diabetes Association)

    Pertinence métier :
    -------------------
    Améliore la performance prédictive tout en conservant
    une explicabilité clinique claire.
    """

    def __init__(self):
        self.logger = LoguruLoggerAdapter("fe.MetabolicFeatureEngineer")

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Création des features métaboliques avancées...")

        # ------------------------------------------------------------------
        # 1. Charge glycémique simplifiée
        # ------------------------------------------------------------------
        df["glycemic_load"] = df["glucose_fasting"] * df["bmi"]
        """
        Interprétation :
        - Combine glycémie et surcharge pondérale
        - Proxy de la pression métabolique exercée sur l'organisme
        """

        # ------------------------------------------------------------------
        # 2. Dyslipidémie clinique (flag)
        # ------------------------------------------------------------------
        df["dyslipidemia_flag"] = (
            (df["triglycerides"] >= 150) | (df["hdl_cholesterol"] < 40)
        ).astype(int)
        """
        Critères NCEP-ATP III :
        - Triglycérides élevés OU HDL bas
        """

        # ------------------------------------------------------------------
        # 3. Score de charge cardio-métabolique cumulée
        # ------------------------------------------------------------------
        df["cardiometabolic_burden_score"] = (
            (df["bmi"] >= 30).astype(int)
            + (df["systolic_bp"] >= 130).astype(int)
            + (df["glucose_fasting"] >= 110).astype(int)
            + (df["triglycerides"] >= 150).astype(int)
            + (df["hdl_cholesterol"] < 40).astype(int)
        )
        """
        Score entier [0–5]
        Plus le score est élevé, plus le risque cardio-métabolique est élevé.
        """

        # ------------------------------------------------------------------
        # 4. Ratio pression artérielle
        # ------------------------------------------------------------------
        df["bp_ratio"] = df["systolic_bp"] / df["diastolic_bp"].replace(0, np.nan)
        """
        Permet de capturer les profils de rigidité artérielle
        indépendamment des seuils catégoriels.
        """

        self.logger.info("Features métaboliques avancées générées.")
        return df
