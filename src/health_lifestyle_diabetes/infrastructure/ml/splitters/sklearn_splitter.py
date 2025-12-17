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
    Dataset splitter based on scikit-learn.

    This class provides a concrete implementation of the
    `DatasetSplitterPort` using `sklearn.model_selection.train_test_split`.

    It is responsible for splitting a dataset into training and testing
    subsets while optionally enforcing stratification on a target column.

    Architectural considerations
    -----------------------------
    - This class belongs to the infrastructure layer.
    - It depends on third-party libraries such as scikit-learn.
    - Configuration is injected via keyword arguments (`**kwargs`).
    - Sensible default values are applied when configuration values
      are missing or set to ``None``.

    Default configuration
    ---------------------
    - train_size: 0.8
    - target_column: "diagnosed_diabetes"
    - random_state: 42
    """

    DEFAULT_TRAIN_SIZE = 0.8
    DEFAULT_TARGET_COLUMN = "diagnosed_diabetes"
    DEFAULT_RANDOM_STATE = 42

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the dataset splitter.

        Parameters
        ----------
        **kwargs : Any
            Optional configuration parameters.

            Supported keys:
            - train_size (float): Proportion of the dataset used for training.
            - target_column (str): Name of the target column used for stratification.
            - random_state (int): Random seed for reproducibility.

            For each parameter:
            - if the key is provided and the value is not ``None``,
              the provided value is used;
            - otherwise, the default value defined in the class
              is applied.
        """

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
            f"SklearnDatasetSplitter initialized | "
            f"train_size={self.train_size}, "
            f"target_column='{self.target_column}', "
            f"random_state={self.random_state}"
        )

    def split(self, dataset: Any) -> Tuple[Any, Any]:
        """
        Split the dataset into training and testing sets.

        The split is performed using `sklearn.model_selection.train_test_split`
        with shuffling enabled and stratification applied on the target column.

        Parameters
        ----------
        dataset : Any
            A pandas-like DataFrame containing both features and the target column.

        Returns
        -------
        Tuple[Any, Any]
            A tuple containing:
            - the training dataset
            - the testing dataset

        Raises
        ------
        DatasetValidationError
            If the target column is not present in the dataset.
        """

        self.logger.info("Starting dataset split")

        if self.target_column not in dataset.columns:
            self.logger.error(
                f"Target column '{self.target_column}' missing in dataset. "
                f"Available columns: {list(dataset.columns)}"
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
            f"Train dataset -> rows={train_data.shape[0]}, "
            f"columns={train_data.shape[1]}"
        )

        self.logger.info(
            f"Test dataset  -> rows={test_data.shape[0]}, "
            f"columns={test_data.shape[1]}"
        )

        return train_data, test_data