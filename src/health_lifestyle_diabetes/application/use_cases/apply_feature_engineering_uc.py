# health_lifestyle_diabetes/application/use_cases/apply_feature_engineering_uc.py

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.feature_engineering.pipeline_feature_engineering import (
    FeatureEngineeringPipeline,
)
from pandas import DataFrame


class ApplyFeatureEngineeringUseCase:
    """
    Use case applicatif responsable de l'application du feature engineering
    sur un dataset brut.
    """

    def __init__(
        self,
        pipeline: FeatureEngineeringPipeline,
        logger: LoggerPort,
    ):
        self.pipeline = pipeline
        self.logger = logger

    def execute(self, dataset: DataFrame) -> DataFrame:
        """
        Applique le pipeline de feature engineering au dataset fourni.

        Parameters
        ----------
        dataset : pd.DataFrame
            Dataset brut en entrée.

        Returns
        -------
        pd.DataFrame
            Dataset enrichi après feature engineering.
        """

        self.logger.info(
            "Début du feature engineering | "
            f"lignes={dataset.shape[0]} | "
            f"colonnes_initiales={dataset.shape[1]}"
        )

        enriched_dataset = self.pipeline.transform(dataset)

        self.logger.info(
            "Feature engineering terminé | "
            f"lignes={enriched_dataset.shape[0]} | "
            f"colonnes_finales={enriched_dataset.shape[1]} | "
            f"delta_colonnes={enriched_dataset.shape[1] - dataset.shape[1]}"
        )

        return enriched_dataset
