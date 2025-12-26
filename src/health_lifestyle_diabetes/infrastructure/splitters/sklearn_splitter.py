from __future__ import annotations

from typing import Any, Tuple

from sklearn.model_selection import train_test_split

from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import DatasetSplitterPort
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.exceptions import DatasetValidationError


class SklearnDatasetSplitter(DatasetSplitterPort):
    """
    Dataset splitter based on scikit-learn.

    Concrete infrastructure implementation of DatasetSplitterPort.
    """

    def __init__(
        self,
        *,
        train_size: float,
        target_column: str,
        random_state: int,
        logger: LoggerPort,
    ) -> None:
        self._train_size = train_size
        self._target_column = target_column
        self._random_state = random_state
        self._logger = logger

        if not 0.0 < self._train_size < 1.0:
            raise DatasetValidationError(
                f"train_size must be in ]0,1[, got {self._train_size}"
            )

        self._logger.debug(
            "SklearnDatasetSplitter initialized",
        )

    def split(self, dataset: Any) -> Tuple[Any, Any]:
        self._logger.info("Starting dataset split")

        if self._target_column not in dataset.columns:
            raise DatasetValidationError(
                f"Target column not found in dataset: '{self._target_column}'"
            )

        train_data, test_data = train_test_split(
            dataset,
            train_size=self._train_size,
            random_state=self._random_state,
            shuffle=True,
            stratify=dataset[self._target_column],
        )

        self._logger.info(
            f"Split done | train={train_data.shape} | test={test_data.shape}"
        )

        return train_data, test_data