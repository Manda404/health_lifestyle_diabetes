import pandas as pd
from pathlib import Path
from health_lifestyle_diabetes.domain.ports.dataset_repository import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetLoadingError,
    DatasetSavingError,
)


logger = get_logger(__name__)


class CSVDatasetRepository(DatasetRepositoryPort):
    """
    Implémentation concrète du port DatasetRepositoryPort
    pour charger et sauvegarder des datasets CSV.
    """

    def __init__(self, source_path: Path):
        """
        Parameters
        ----------
        source_path : Path
            Le chemin du fichier CSV à charger.
        """
        self.source_path = source_path

    def load_csv(self):
        """
        Charge un dataset CSV depuis self.source_path.
        """
        logger.info(f"Chargement du dataset depuis : {self.source_path}")

        try:
            if not self.source_path.exists():
                raise DatasetLoadingError(f"Fichier introuvable : {self.source_path}")

            df = pd.read_csv(self.source_path)
            logger.info(
                f"Dataset chargé avec succès ({df.shape[0]} lignes, {df.shape[1]} colonnes)."
            )
            return df

        except Exception as e:
            logger.error(f"Erreur lors du chargement du dataset : {e}")
            raise DatasetLoadingError(str(e))

    def save_csv(self, data: pd.DataFrame, path: Path) -> None:
        """
        Sauvegarde un dataset au format CSV.
        """
        logger.info(f"Sauvegarde du dataset dans : {path}")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            data.to_csv(path, index=False)
            logger.info(f"Dataset sauvegardé avec succès : {path}")

        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du dataset : {e}")
            raise DatasetSavingError(str(e))
