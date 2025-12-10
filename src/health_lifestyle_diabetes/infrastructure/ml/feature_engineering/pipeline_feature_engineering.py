from pathlib import Path

from health_lifestyle_diabetes.domain.ports.feature_engineering_port import (
    FeatureEngineeringPort,
)
from health_lifestyle_diabetes.infrastructure.ml.feature_engineering.base_preprocessing import (
    clean_categorical_variables,
)
from health_lifestyle_diabetes.infrastructure.ml.feature_engineering.clinical_features import (
    ClinicalFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.ml.feature_engineering.demographics_features import (
    DemographicsFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.ml.feature_engineering.lifestyle_features import (
    LifestyleFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.ml.feature_engineering.medical_features import (
    MedicalFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.utils.config_loader import ConfigLoader
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from pandas import DataFrame


class FeatureEngineeringPipeline(FeatureEngineeringPort):
    """
    Pipeline complet de Feature Engineering médical et comportemental.

    Objectif :
    ----------
    Orchestrer l’ensemble des transformations en suivant la logique
    physiopathologique du risque diabétique.

    Justification médicale :
    ------------------------
    Les transformations suivent le continuum santé :
    Démographie → Physiologie → Métabolisme → Comportement.

    Pertinence métier :
    -------------------
    Fournit un dataset enrichi, explicable et cohérent
    pour la modélisation prédictive ou les tableaux de bord santé.
    """

    def __init__(
        self,
        config_path: str | Path | None = None,
        config: dict | None = None,
        logger_name: str = "fe.FeatureEngineeringPipeline",
    ):
        root = get_repository_root()
        resolved_path = Path(config_path) if config_path else root / "configs/preprocessing.yaml"
        loaded_config = config or ConfigLoader.load_config(resolved_path)
        age_group_strategy = loaded_config["feature_engineering"]["age_group_strategy"]

        self.demographics = DemographicsFeatureEngineer(
            age_group_strategy=age_group_strategy
        )
        self.medical = MedicalFeatureEngineer()
        self.clinical = ClinicalFeatureEngineer()
        self.lifestyle = LifestyleFeatureEngineer()
        self.logger = get_logger(logger_name)

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Démarrage du pipeline complet de Feature Engineering...")

        # Étape 1 : Nettoyage
        df = clean_categorical_variables(df)

        # Étape 2 : Démographie
        df = self.demographics.transform(df)

        # Étape 3 : Médical
        df = self.medical.transform(df)

        # Étape 4 : Interactions physiologiques
        df = self.clinical.transform(df)

        # Étape 5 : Mode de vie
        df = self.lifestyle.transform(df)

        self.logger.info(
            f"Pipeline complet exécuté avec succès. Colonnes totales : {len(df.columns)}"
        )
        return df
