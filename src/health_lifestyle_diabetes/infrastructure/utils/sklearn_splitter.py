# src/health_lifestyle_diabetes/infrastructure/ml/splitters/sklearn_splitter.py

from __future__ import annotations

from typing import Any, Tuple

from sklearn.model_selection import train_test_split

from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetValidationError,
)


class SklearnDatasetSplitter(DatasetSplitterPort):
    """
    Sklearn-based implementation of DatasetSplitterPort.

    Configuration is injected via **kwargs.
    For each parameter:
    - if provided and not None → used
    - otherwise → default value is applied
    """

    DEFAULT_TRAIN_SIZE = 0.8
    DEFAULT_TARGET_COLUMN = "target"
    DEFAULT_RANDOM_STATE = 42

    def __init__(self, **kwargs: Any) -> None:
        self.logger = LoguruLoggerAdapter("dataset_split.sklearn")

        # Use provided values if not None, otherwise defaults
        self.train_size: float = (
            kwargs.get("train_size")
            if kwargs.get("train_size") is not None
            else self.DEFAULT_TRAIN_SIZE
        )

        self.target_column: str = (
            kwargs.get("target_column")
            if kwargs.get("target_column") is not None
            else self.DEFAULT_TARGET_COLUMN
        )

        self.random_state: int = (
            kwargs.get("random_state")
            if kwargs.get("random_state") is not None
            else self.DEFAULT_RANDOM_STATE
        )

        # Minimal validation
        if not 0.0 < self.train_size < 1.0:
            raise DatasetValidationError(
                f"train_size must be in ]0,1[, got {self.train_size}"
            )

        self.logger.debug(
            "SklearnDatasetSplitter initialized",
            train_size=self.train_size,
            target_column=self.target_column,
            random_state=self.random_state,
        )

    def split(self, dataset: Any) -> Tuple[Any, Any]:
        """
        Split the dataset into train and test sets.
        """

        self.logger.info("Starting dataset split")

        if self.target_column not in dataset.columns:
            self.logger.error(
                "Target column missing in dataset",
                target_column=self.target_column,
                available_columns=list(dataset.columns),
            )
            raise DatasetValidationError(
                f"Target column not found in dataset: '{self.target_column}'"
            )

        train_data, test_data = train_test_split(
            dataset,
            train_size=self.train_size,
            random_state=self.random_state,
            shuffle=True,
            stratify=dataset[self.target_column],
        )

        self.logger.info("Dataset split completed")

        self.logger.info(
            "Train dataset statistics",
            rows=train_data.shape[0],
            columns=train_data.shape[1],
        )

        self.logger.info(
            "Test dataset statistics",
            rows=test_data.shape[0],
            columns=test_data.shape[1],
        )

        return train_data, test_data