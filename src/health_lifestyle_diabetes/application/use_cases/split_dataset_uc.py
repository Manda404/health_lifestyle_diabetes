import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.infrastructure.utils.paths import get_repository_root
from health_lifestyle_diabetes.infrastructure.utils.config_loader import ConfigLoader
from health_lifestyle_diabetes.domain.ports.dataset_repository import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    DatasetValidationError,
)

logger = get_logger(__name__)


class SplitDatasetUseCase:
    """
    Cas d'utilisation pour diviser un dataset en ensembles
    d'entraînement, de validation et de test.
    """

    def __init__(self, dataset_repo: DatasetRepositoryPort):
        self.dataset_repo = dataset_repo

    def execute(
        self,
        train_size: float = 0.7,
        test_size: float = 0.3,
        random_state: int = 42,
        target_column: str = "diagnosed_diabetes",
        is_save: bool = False,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Divise le dataset en train et test avec stratification.

        Parameters
        ----------
        data_path : Path
            Chemin du dataset source.
        train_size : float
            Proportion de l'ensemble d'entraînement.
        test_size : float
            Proportion de l'ensemble de test.
        target_column : str
            Colonne cible pour la stratification.
        is_save : bool
            Si False, sauvegarde automatiquement les splits.

        Returns
        -------
        (train_df, test_df)
            Deux DataFrames résultants.
        """
        if not abs(train_size + test_size - 1.0) < 1e-6:
            raise DatasetValidationError(
                "La somme des proportions train_size, val_size et test_size doit être égale à 1."
            )

        # Charger le dataset complet
        logger.info("Chargement du dataset depuis la source.")
        dataset = self.dataset_repo.load_csv()

        # Diviser en train et temp (val + test)
        train_data, test_data = train_test_split(
            dataset,
            train_size=train_size,
            random_state=random_state,
            shuffle=True,
            stratify=dataset[target_column],
        )

        if not is_save:
            root = get_repository_root()

            paths = ConfigLoader.load_config(root / "configs/paths.yaml")

            full_train_path = root / paths["data"]["output"]["train_dataset"]
            full_test_path = root / paths["data"]["output"]["test_dataset"]

            # Sauvegarder les datasets divisés
            logger.info("Sauvegarde des datasets divisés.")
            self.dataset_repo.save_csv(train_data, full_train_path)
            self.dataset_repo.save_csv(test_data, full_test_path)

        logger.info(
            f"Dataset divisé en : "
            f"train ({train_data.shape[0]} lignes) - ({train_data.shape[1]} colonnes), "
            f"test ({test_data.shape[0]} lignes) - ({test_data.shape[1]} colonnes)."
        )
        return train_data, test_data
