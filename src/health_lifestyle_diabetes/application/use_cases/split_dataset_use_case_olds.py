from typing import Any, Tuple

from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class SplitDatasetUseCase:
    """
    Use case : appliquer un split train / test sur un dataset.
    """

    def __init__(
        self,
        splitter: DatasetSplitterPort,
        logger: LoggerPort,
    ):
        self.splitter = splitter
        self.logger = logger

    def execute(self, df: Any) -> Tuple[Any, Any]:
        self.logger.info("Démarrage du split dataset.")

        train_df, test_df = self.splitter.split(df)

        self.logger.info(
            f"Split terminé : train={train_df.shape}, test={test_df.shape}"
        )

        return train_df, test_df
