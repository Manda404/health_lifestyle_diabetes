from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from health_lifestyle_diabetes.domain.ports.dataset_repository_port import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetValidationError,
)


@dataclass
class SplitDatasetUseCase:
    """
    Use case responsable de diviser le dataset en un ensemble d'entraînement
    et un ensemble de test, avec stratification.
    """

    dataset_repo: DatasetRepositoryPort
    splitter: DatasetSplitterPort
    logger: LoggerPort

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
        self.logger.info("Chargement du dataset via le repository.")
        dataset = self.dataset_repo.load_csv()

        # --------------------------
        # Split
        # --------------------------
        self.logger.info("Split du dataset avec stratification.")
        train_df, test_df = self.splitter.split(
            dataset=dataset,
            target_column=target_column,
            train_size=train_size,
            random_state=random_state,
        )

        # --------------------------
        # Sauvegarde éventuelle
        # --------------------------
        if save_paths is not None:
            train_path, test_path = save_paths

            self.logger.info(f"Sauvegarde du train → {train_path}")
            self.dataset_repo.save_csv(train_df, train_path)

            self.logger.info(f"Sauvegarde du test → {test_path}")
            self.dataset_repo.save_csv(test_df, test_path)

        # --------------------------
        # Logging final
        # --------------------------
        self.logger.info(
            f"Split terminé : train = {train_df.shape}, test = {test_df.shape}"
        )

        return train_df, test_df
