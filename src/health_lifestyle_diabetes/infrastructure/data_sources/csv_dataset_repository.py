# src/health_lifestyle_diabetes/infrastructure/data_sources/csv_dataset_repository.py
from pathlib import Path

from typing import Optional

from pandas import DataFrame, read_csv

from health_lifestyle_diabetes.domain.ports.dataset_repository_port import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)
from health_lifestyle_diabetes.infrastructure.utils.config_loader import ConfigLoader

from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetLoadingError,
    DatasetSavingError,
)

from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root

# Détermine la racine du projet.
root = get_repository_root()

# Charge le fichier de configuration 'paths.yaml' pour connaître les emplacements des données.
paths = ConfigLoader.load_config(root / "configs/paths.yaml")
raw_path = paths["data"]["input"][
    "raw_dataset"
]  # Extrait le chemin relatif du dataset brut.
INPUT_DATA_PATH = root / raw_path  # Construit le chemin complet du fichier CSV.


class CSVDatasetRepository(DatasetRepositoryPort):
    """
    Implémentation concrète du port DatasetRepositoryPort
    pour charger et sauvegarder des datasets CSV.
    """

    def __init__(
        self,
        source_path: Optional[Path] = None,
        logger: Optional[LoguruLoggerAdapter] = None,
    ):
        """
        Parameters
        ----------
        source_path : Path
            Le chemin du fichier CSV à charger.
        """
        self.source_path = source_path if source_path is not None else INPUT_DATA_PATH
        self.logger = self.logger = (
            logger
            if logger is not None
            else LoguruLoggerAdapter("csv.datasetrepository")
        )

    def load_dataset(self):
        """
        Charge un dataset CSV depuis self.source_path.
        """
        self.logger.info(f"Chargement du dataset depuis : {self.source_path}")

        try:
            if not self.source_path.exists():
                raise DatasetLoadingError(f"Fichier introuvable : {self.source_path}")

            df = read_csv(self.source_path)
            self.logger.info(
                f"Dataset chargé avec succès ({df.shape[0]} lignes, {df.shape[1]} colonnes)."
            )
            return df

        except Exception as e:
            self.logger.error(f"Erreur lors du chargement du dataset : {e}")
            raise DatasetLoadingError(str(e))

    def save_dataset(self, data: DataFrame, path: Path) -> None:
        """
        Sauvegarde un dataset au format CSV.
        """
        self.logger.info(f"Sauvegarde du dataset dans : {path}")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            data.to_csv(path, index=False)
            self.logger.info(f"Dataset sauvegardé avec succès : {path}")

        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du dataset : {e}")
            raise DatasetSavingError(str(e))
