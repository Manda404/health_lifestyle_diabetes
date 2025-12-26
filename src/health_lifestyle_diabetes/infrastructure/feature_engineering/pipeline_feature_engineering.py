# src/health_lifestyle_diabetes/infrastructure/ml/feature_engineering/pipeline_feature_engineering.py

from pandas import DataFrame

from health_lifestyle_diabetes.domain.ports.feature_engineering_port import (
    FeatureEngineeringPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort

from health_lifestyle_diabetes.infrastructure.feature_engineering.base_preprocessing import (
    clean_categorical_variables,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.clinical_features import (
    ClinicalFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.demographics_features import (
    DemographicsFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.lifestyle_features import (
    LifestyleFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.medical_features import (
    MedicalFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.metabolic_features import (
    MetabolicFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.behavioral_features import (
    BehavioralFeatureEngineer,
)
from health_lifestyle_diabetes.infrastructure.feature_engineering.exclusion import (
    drop_leakage_columns,
)
from health_lifestyle_diabetes.infrastructure.utils.config_loader import YamlConfigLoader
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
root = get_repository_root()
config = YamlConfigLoader.load_config(root / "configs/preprocessing.yaml")
age_group_strategy = config["feature_engineering"]["age_group_strategy"]


class FeatureEngineeringPipeline(FeatureEngineeringPort):
    """
    Pipeline complet de Feature Engineering médical, métabolique
    et comportemental pour l’évaluation du risque diabétique.

    Objectif :
    ----------
    Orchestrer l’ensemble des transformations de manière cohérente,
    explicable et sans fuite d’information.

    Justification médicale :
    ------------------------
    Les transformations suivent le continuum physiopathologique :
    Démographie → Clinique → Métabolisme → Comportement.

    Pertinence métier :
    -------------------
    Produit un dataset enrichi, traçable et exploitable
    pour la modélisation prédictive et l’analyse de risque.
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

        # Feature engineering blocks
        self.demographics = DemographicsFeatureEngineer(
            logger=self.logger,
            age_group_strategy=age_group_strategy
        )
        self.medical = MedicalFeatureEngineer(logger=self.logger)
        self.clinical = ClinicalFeatureEngineer(logger=self.logger)
        self.metabolic = MetabolicFeatureEngineer(logger=self.logger)
        self.behavioral = BehavioralFeatureEngineer(logger=self.logger)
        self.lifestyle = LifestyleFeatureEngineer(logger=self.logger)

    def transform(self, df: DataFrame) -> DataFrame:
        df_enriched = df.copy(deep=True)
        self.logger.info("Démarrage du pipeline complet de Feature Engineering...")

        # --------------------------------------------------------------
        # Étape 0 : Suppression du data leakage
        # --------------------------------------------------------------
        df_enriched = drop_leakage_columns(df_enriched, self.logger)

        # --------------------------------------------------------------
        # Étape 1 : Nettoyage des variables catégorielles
        # --------------------------------------------------------------
        df_enriched = clean_categorical_variables(df_enriched,self.logger)

        # --------------------------------------------------------------
        # Étape 2 : Variables démographiques
        # --------------------------------------------------------------
        df_enriched = self.demographics.transform(df_enriched)

        # --------------------------------------------------------------
        # Étape 3 : Variables médicales cliniques
        # --------------------------------------------------------------
        df_enriched = self.medical.transform(df_enriched)

        # --------------------------------------------------------------
        # Étape 4 : Interactions physiologiques
        # --------------------------------------------------------------
        df_enriched = self.clinical.transform(df_enriched)

        # --------------------------------------------------------------
        # Étape 5 : Métabolisme avancé
        # --------------------------------------------------------------
        df_enriched = self.metabolic.transform(df_enriched)

        # --------------------------------------------------------------
        # Étape 6 : Comportement & mode de vie
        # --------------------------------------------------------------
        df_enriched = self.behavioral.transform(df_enriched)
        df_enriched = self.lifestyle.transform(df_enriched)

        self.logger.info(
            f"Pipeline exécuté avec succès. Nombre total de colonnes : {len(df_enriched.columns)}"
        )
        return df_enriched
