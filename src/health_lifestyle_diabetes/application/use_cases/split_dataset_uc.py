from typing import Tuple

import pandas as pd
from health_lifestyle_diabetes.domain.ports.dataset_repository_port import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetValidationError,
)
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)


class SplitDatasetUseCase:
    """
    Use case responsable de diviser le dataset en un ensemble d'entraînement
    et un ensemble de test, avec stratification.
    """

    def __init__(self, dataset_repo: DatasetRepositoryPort):
        self.dataset_repo = dataset_repo

    def execute(
        self,
        train_size: float = 0.8,
        random_state: int = 42,
        target_column: str = "diagnosed_diabetes",
        save_paths: Tuple[str, str] | None = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Exécute la division du dataset en train/test.

        Parameters
        ----------
        train_size : float
            Proportion de l'ensemble d'entraînement.
        random_state : int
        target_column : str
        save_paths : tuple or None
            Si fourni → (train_path, test_path)

        Returns
        -------
        (train_df, test_df)
        """
        # --------------------------
        # Validation
        # --------------------------
        if not 0 < train_size < 1:
            raise DatasetValidationError("train_size doit être compris entre 0 et 1.")

        # --------------------------
        # Charger dataset
        # --------------------------
        logger.info("Chargement du dataset via le repository.")
        dataset = self.dataset_repo.load_csv()

        # --------------------------
        # Split
        # --------------------------
        logger.info("Split du dataset avec stratification.")
        train_df, test_df = train_test_split(
            dataset,
            train_size=train_size,
            random_state=random_state,
            shuffle=True,
            stratify=dataset[target_column],
        )

        # --------------------------
        # Sauvegarde éventuelle
        # --------------------------
        if save_paths is not None:
            train_path, test_path = save_paths

            logger.info(f"Sauvegarde du train → {train_path}")
            self.dataset_repo.save_csv(train_df, train_path)

            logger.info(f"Sauvegarde du test → {test_path}")
            self.dataset_repo.save_csv(test_df, test_path)

        # --------------------------
        # Logging final
        # --------------------------
        logger.info(f"Split terminé : train = {train_df.shape}, test = {test_df.shape}")

        return train_df, test_df
