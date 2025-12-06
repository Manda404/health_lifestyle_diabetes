import numpy as np
import pandas as pd
from pandas import DataFrame
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

logger = get_logger("fe.DemographicsFeatureEngineer")


class DemographicsFeatureEngineer:
    """
    Gère les variables socio-démographiques : âge, sexe, emploi, etc.

    Objectif :
    ----------
    Structurer les variables de contexte patient pour des analyses populationnelles.

    Justification médicale :
    ------------------------
    L’âge, le sexe et la situation socio-économique sont des déterminants
    majeurs de la prévalence du diabète.

    Pertinence métier :
    -------------------
    Ces variables permettent de construire des modèles de risque adaptés
    aux sous-populations et d’analyser les disparités de santé.
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
        self.logger = logger
        self.age_group_strategy = age_group_strategy

    # ----------------------------------------------------------------------
    # 1) Découpage d'âge détaillé
    # ----------------------------------------------------------------------
    def _create_age_group_detailed(self, df: DataFrame) -> DataFrame:
        bins = [0, 30, 40, 50, 60, 70, 80, np.inf]
        labels = ["<30", "30–39", "40–49", "50–59", "60–69", "70–79", "80+"]
        df["age_group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
        return df

    # ----------------------------------------------------------------------
    # 2) Découpage d'âge en 3 groupes
    # ----------------------------------------------------------------------
    def _create_age_group_coarse(self, df: DataFrame) -> DataFrame:
        bins = [0, 30, 60, np.inf]
        labels = ["Jeune", "Adulte", "Senior"]
        df["age_group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
        return df

    # ----------------------------------------------------------------------
    # 3) Sélection de la stratégie
    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    # 4) Pipeline de transformation
    # ----------------------------------------------------------------------
    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Création des variables démographiques...")

        # Ajout du découpage d'âge selon stratégie choisie
        df = self._create_age_group(df)

        self.logger.info("Variables démographiques complétées.")
        return df