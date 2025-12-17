# src/health_lifestyle_diabetes/application/use_cases/split_dataset_uc.py

from __future__ import annotations

from typing import Any, Tuple

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


class SplitDatasetUseCase:
    """
    Use case responsable d’orchestrer la division d'un dataset en train/test.

    Clean Architecture :
    --------------------
    - ne contient aucune logique technique,
    - ne dépend ni de Pandas ni de sklearn,
    - utilise un logger abstrait (LoggerPort),
    - délègue au DatasetSplitterPort la découpe du dataset.
    """

    def __init__(
        self,
        dataset_repo: DatasetRepositoryPort,
        dataset_splitter: DatasetSplitterPort,
        logger: LoggerPort,
    ):
        self.dataset_repo = dataset_repo
        self.dataset_splitter = dataset_splitter
        self.logger = logger

    def execute(
        self,
        train_size: float = 0.8,
        random_state: int = 42,
        target_column: str = "diagnosed_diabetes",
        save_paths: Tuple[str, str] | None = None,
    ) -> Tuple[Any, Any]:

        self.logger.info("Début du split du dataset.")

        if not 0 < train_size < 1:
            self.logger.error("train_size doit être compris entre 0 et 1.")
            raise DatasetValidationError("train_size doit être compris entre 0 et 1.")

        # Charger dataset
        self.logger.info("Chargement du dataset via le repository.")
        dataset = self.dataset_repo.load_dataset()

        # Split via port
        self.logger.info("Split du dataset via DatasetSplitterPort.")
        train_data, test_data = self.dataset_splitter.split(
            dataset=dataset,
            train_size=train_size,
            target_column=target_column,
            random_state=random_state,
        )

        # Sauvegarde éventuelle
        if save_paths is not None:
            train_path, test_path = save_paths
            self.logger.info(f"Sauvegarde du train → {train_path}")
            self.dataset_repo.save_dataset(train_data, train_path)

            self.logger.info(f"Sauvegarde du test → {test_path}")
            self.dataset_repo.save_dataset(test_data, test_path)

        self.logger.info("Split terminé avec succès.")
        return train_data, test_data
