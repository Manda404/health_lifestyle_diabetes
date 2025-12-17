# src/health_lifestyle_diabetes/infrastructure/ml/feature_engineering/demographics_features.py

import numpy as np
import pandas as pd
from pandas import DataFrame

from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)

class DemographicsFeatureEngineer:
    """
    Gère les variables socio-démographiques : âge, sexe, statut socio-économique.

    Objectif :
    ----------
    Structurer les variables de contexte patient afin de capturer
    les déterminants démographiques et sociaux du risque diabétique.

    Justification médicale :
    ------------------------
    L’âge et le contexte socio-économique sont des déterminants majeurs
    de la prévalence du diabète et des inégalités de santé.

    Pertinence métier :
    -------------------
    Permet d’analyser les disparités populationnelles
    et d’adapter les stratégies de prévention.
    """

    def __init__(self, age_group_strategy: str = "detailed"):
        """
        Parameters
        ----------
        age_group_strategy : str
            Choix de la granularité du découpage d'âge.
            Options :
            - "detailed" : <30, 30–39, ..., 80+
            - "coarse"   : Jeune, Adulte, Senior
        """
        self.logger = LoguruLoggerAdapter("fe.DemographicsFeatureEngineer")
        self.age_group_strategy = age_group_strategy

    # ------------------------------------------------------------------
    # 1) Découpage d'âge détaillé
    # ------------------------------------------------------------------
    def _create_age_group_detailed(self, df: DataFrame) -> DataFrame:
        bins = [0, 30, 40, 50, 60, 70, 80, np.inf]
        labels = ["<30", "30–39", "40–49", "50–59", "60–69", "70–79", "80+"]
        df["age_group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
        return df

    # ------------------------------------------------------------------
    # 2) Découpage d'âge simplifié
    # ------------------------------------------------------------------
    def _create_age_group_coarse(self, df: DataFrame) -> DataFrame:
        bins = [0, 30, 60, np.inf]
        labels = ["Jeune", "Adulte", "Senior"]
        df["age_group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
        return df

    # ------------------------------------------------------------------
    # 3) Sélection de la stratégie de découpage
    # ------------------------------------------------------------------
    def _create_age_group(self, df: DataFrame) -> DataFrame:
        if self.age_group_strategy == "detailed":
            self.logger.info("Utilisation du découpage d'âge détaillé.")
            return self._create_age_group_detailed(df)

        elif self.age_group_strategy == "coarse":
            self.logger.info("Utilisation du découpage d'âge en 3 catégories.")
            return self._create_age_group_coarse(df)

        else:
            raise ValueError(
                f"Stratégie inconnue pour age_group_strategy='{self.age_group_strategy}'. "
                "Options valides : ['detailed', 'coarse']"
            )

    # ------------------------------------------------------------------
    # 4) Pipeline de transformation démographique
    # ------------------------------------------------------------------
    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Création des variables démographiques...")

        # --------------------------------------------------------------
        # 4.1 Découpage d'âge (catégoriel)
        # --------------------------------------------------------------
        df = self._create_age_group(df)

        # --------------------------------------------------------------
        # 4.2 Non-linéarité de l'âge
        # --------------------------------------------------------------
        df["age_squared"] = df["Age"] ** 2
        """
        Capture les effets non linéaires du vieillissement
        sur le risque métabolique et diabétique.
        """

        # --------------------------------------------------------------
        # 4.3 Vulnérabilité socio-économique
        # --------------------------------------------------------------
        df["socioeconomic_vulnerability_flag"] = (
            df["income_level"].isin(["Low", "Lower-Middle"])
            & df["education_level"].isin(["No formal", "Highschool"])
        ).astype(int)
        """
        Proxy de précarité socio-économique,
        facteur reconnu d'inégalités de santé
        et de moindre accès à la prévention.
        """

        self.logger.info("Variables démographiques complétées.")
        return df
