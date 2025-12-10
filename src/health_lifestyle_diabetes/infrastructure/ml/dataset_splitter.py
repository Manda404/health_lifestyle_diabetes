"""
Adaptateur scikit-learn pour le port DatasetSplitterPort.
"""

from typing import Tuple

import pandas as pd
from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from sklearn.model_selection import train_test_split


class SklearnDatasetSplitter(DatasetSplitterPort):
    """Implémentation du split train/test avec scikit-learn."""

    def __init__(self, logger: LoggerPort) -> None:
        self.logger = logger

    def split(
        self,
        dataset: pd.DataFrame,
        target_column: str,
        train_size: float,
        random_state: int,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if target_column not in dataset:
            raise ValueError(f"La colonne cible '{target_column}' est absente du dataset.")

        self.logger.debug(
            "Split dataset: train_size=%s, random_state=%s, target=%s",
            train_size,
            random_state,
            target_column,
        )

        return train_test_split(
            dataset,
            train_size=train_size,
            random_state=random_state,
            shuffle=True,
            stratify=dataset[target_column],
        )
