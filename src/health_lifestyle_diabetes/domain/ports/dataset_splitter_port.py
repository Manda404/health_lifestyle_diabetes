"""
Port pour déléguer la découpe train/test du dataset à une implémentation
infrastructure (scikit-learn ou autre), afin de préserver l'isolation de la
coupe application vis-à-vis des dépendances techniques.
"""

from typing import Protocol, Tuple

import pandas as pd


class DatasetSplitterPort(Protocol):
    """Contrat pour un service de split de dataset."""

    def split(
        self,
        dataset: pd.DataFrame,
        target_column: str,
        train_size: float,
        random_state: int,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        ...
