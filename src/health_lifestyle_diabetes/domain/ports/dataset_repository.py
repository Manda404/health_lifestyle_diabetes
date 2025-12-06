# src/health_lifestyle_diabetes/domain/ports/dataset_repository.py

from typing import Protocol
from pandas import DataFrame
from pathlib import Path

class DatasetRepositoryPort(Protocol):
    """
    Port (interface) décrivant ce que le domaine attend d'un repository
    de chargement de datasets.

    Toute implémentation (CSV, Parquet, SQL, S3, FeatureStore, etc.)
    doit respecter ce contrat.
    """

    def load_csv(self) -> DataFrame:
        """
        Charge un dataset brut depuis une source donnée.

        Returns
        -------
        DataFrame
            Le dataset sous forme de DataFrame.
        """
        ...


    def save_csv(self, data: DataFrame, path: Path) -> None:
        """
        Sauvegarde un dataset sous forme de DataFrame vers une destination donnée.
        Parameters
        ----------
        data : DataFrame
            Le dataset à sauvegarder.
        path : Path
            Le chemin de destination où sauvegarder le dataset.
        """
        ...