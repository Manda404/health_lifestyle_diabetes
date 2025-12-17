"""
Port (interface) pour les repositories de datasets.

Objectif :
----------
Définir ce que le domaine attend d'un service de chargement/sauvegarde
de datasets, sans imposer la technologie (CSV, Parquet, SQL, S3…).

L'infrastructure fournira une implémentation concrète :
- CSVDatasetRepository
- SQLDatasetRepository
- etc.
"""

from pathlib import Path
from typing import Any, Protocol


class DatasetRepositoryPort(Protocol):
    """
    Interface d'un repository de datasets.
    """

    def load_dataset(self) -> Any:
        """
        Charge un dataset complet depuis une source (fichier, base, etc.).

        Retour
        ------
        Any
            Représentation tabulaire du dataset (ex: DataFrame côté infra).
        """
        ...

    def save_dataset(self, data: Any, path: Path) -> None:
        """
        Sauvegarde un dataset vers une destination (fichier, répertoire, etc.).

        Paramètres
        ----------
        data : Any
            Dataset dans le format manipulé par l'infrastructure.
        path : Path
            Chemin de sauvegarde cible.
        """
        ...
