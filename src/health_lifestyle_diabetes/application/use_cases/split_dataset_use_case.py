from pathlib import Path
from typing import Any, Tuple, Dict, Optional

from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.infrastructure.utils.config_loader import (
    YamlConfigLoader,
)
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

# Get repository root path
root = get_repository_root()

# Load configuration
config_loader = YamlConfigLoader()
paths = config_loader.load_config(f"{root}/configs/paths.yaml")
# Define train and test dataset paths
PATHS : Dict[str, Path] = {
    "train": root / Path(paths["data"]["input"]["train_dataset"]),
    "test": root / Path(paths["data"]["input"]["test_dataset"]),
}

class SplitDatasetUseCase:
    """
    Use case : Splitter un dataset selon la config chargée.
    """

    def __init__(self, splitter: DatasetSplitterPort, logger: LoggerPort, save: bool = True, save_paths: Optional[Dict[str, Path]] = None):
        self.splitter = splitter
        self.logger = logger
        self.save = save
        self.save_paths = save_paths or PATHS

    def execute(self, df: Any) -> Tuple[Any, Any]:
        """
        Applique le split et retourne (train, test).
        """

        self.logger.info("Démarrage du split dataset...")

        train_df, valid_df = self.splitter.split(df)

        self.logger.info(f"Split terminé : "
                         f"train={train_df.shape}, test={valid_df.shape}")
        if self.save:
            self.logger.info("Sauvegarde des datasets splittés...")
            # Implémenter la logique de sauvegarde ici si nécessaire.
            train_df.to_csv(PATHS["train"], index=False)
            valid_df.to_csv(PATHS["test"], index=False)
            self.logger.info("Datasets sauvegardés avec succès.")

        return train_df, valid_df