# src/health_lifestyle_diabetes/domain/ports/dataset_splitter_port.py

from __future__ import annotations

from typing import Any, Protocol, Tuple


class DatasetSplitterPort(Protocol):
    """
    Port décrivant le contrat d’un service capable de diviser un dataset.

    Le domaine ne connaît pas Pandas, ni sklearn, ni aucune technologie.
    Il ne fait que définir l’action attendue :

        - prendre un dataset tabulaire (type abstrait),
        - le couper en train/test,
        - éventuellement de façon stratifiée.

    L’implémentation concrète se trouve dans l’infrastructure.
    """

    def split(
        self,
        dataset: Any,
        train_size: float,
        target_column: str,
        random_state: int,
    ) -> Tuple[Any, Any]:
        """
        Divise un dataset en deux ensembles (train/test).

        Parameters
        ----------
        dataset : Any
            Table de données (ex : DataFrame, Spark DataFrame…)
        train_size : float
            Proportion de l'ensemble d'entraînement
        target_column : str
            Nom de la colonne cible à utiliser pour la stratification
        random_state : int
            Graine aléatoire pour la reproductibilité

        Returns
        -------
        (train_dataset, test_dataset)
        """
        ...
