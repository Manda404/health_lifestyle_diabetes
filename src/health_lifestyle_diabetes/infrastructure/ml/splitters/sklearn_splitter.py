# src/health_lifestyle_diabetes/infrastructure/ml/splitters/sklearn_splitter.py

from __future__ import annotations

from typing import Any, Tuple

from sklearn.model_selection import train_test_split

from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)


class SklearnDatasetSplitter(DatasetSplitterPort):
    """
    Implémentation concrète du DatasetSplitterPort,
    utilisant sklearn.model_selection.train_test_split.

    Cette classe appartient à l'infrastructure car elle dépend :
    - de Pandas (implicitement via le DataFrame),
    - de sklearn,
    - de la logique technique de stratification.

    Le domaine et l'application ne connaîtront que le port DatasetSplitterPort.
    """

    def split(
        self,
        dataset: Any,
        train_size: float,
        target_column: str,
        random_state: int,
    ) -> Tuple[Any, Any]:

        if target_column not in dataset.columns:
            raise ValueError(f"Colonne cible introuvable : {target_column}")

        train_data, test_data = train_test_split(
            dataset,
            train_size=train_size,
            random_state=random_state,
            shuffle=True,
            stratify=dataset[target_column],
        )

        return train_data, test_data
