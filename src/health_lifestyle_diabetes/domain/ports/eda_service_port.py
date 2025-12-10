"""
Port exposant les opérations EDA attendues par la couche application.
Il permet d'orchestrer les analyses sans importer directement les dépendances
graphiques ou techniques depuis l'application.
"""

from typing import List, Protocol, Tuple

import pandas as pd
from pandas import DataFrame


class EDAServicePort(Protocol):
    """Contrat pour un service dédié aux analyses EDA."""

    def summarize_dataset(self, df: DataFrame) -> DataFrame:
        ...

    def identify_feature_types(self, df: DataFrame) -> Tuple[List[str], List[str]]:
        ...

    def analyze_risk_distribution(
        self, df: DataFrame, score_col: str, stage_col: str
    ) -> None:
        ...

    def analyze_risk_score(
        self, df: DataFrame, score_col: str, stage_col: str, diag_col: str
    ) -> None:
        ...

    def plot_numeric_feature_distribution(self, df: pd.DataFrame, column: str) -> None:
        ...

    def plot_numeric_vs_target(self, df: pd.DataFrame, column: str) -> None:
        ...
