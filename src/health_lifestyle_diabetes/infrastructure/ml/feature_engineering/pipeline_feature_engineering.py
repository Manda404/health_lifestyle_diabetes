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

    def __init__(self) -> None:

        root = get_repository_root()
        config = ConfigLoader.load_config(root / "configs/preprocessing.yaml")
        age_group_strategy = config["feature_engineering"]["age_group_strategy"]

        self.demographics = DemographicsFeatureEngineer(
            age_group_strategy=age_group_strategy
        )
        self.medical = MedicalFeatureEngineer()
        self.clinical = ClinicalFeatureEngineer()
        self.lifestyle = LifestyleFeatureEngineer()
        self.logger = get_logger("fe.FeatureEngineeringPipeline")

    def transform(self, df: DataFrame) -> DataFrame:
        df_enrich = df.copy()
        self.logger.info("Démarrage du pipeline complet de Feature Engineering...")

        # Étape 1 : Nettoyage
        df_enrich = clean_categorical_variables(df_enrich)

        # Étape 2 : Démographie
        df_enrich = self.demographics.transform(df_enrich)

        # Étape 3 : Médical
        df_enrich = self.medical.transform(df_enrich)

        # Étape 4 : Interactions physiologiques
        df_enrich = self.clinical.transform(df_enrich)

        # Étape 5 : Mode de vie
        df_enrich = self.lifestyle.transform(df_enrich)

        self.logger.info(
            f"Pipeline complet exécuté avec succès. Colonnes totales : {len(df_enrich.columns)}"
        )
        return df_enrich
