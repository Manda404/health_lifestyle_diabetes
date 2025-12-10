from typing import Protocol

from pandas import DataFrame


class EDAServicePort(Protocol):
    """Port définissant les fonctionnalités d'un service d'EDA.

    Ce port permet au domaine et aux use cases de dépendre d'une abstraction
    plutôt que des implémentations concrètes situées dans l'infrastructure.
    """

    def summarize_dataset(self, df: DataFrame) -> DataFrame:
        """Retourne un résumé statistique du dataset."""
        ...

    def identify_feature_types(self, df: DataFrame) -> tuple[list[str], list[str]]:
        """Identifie les colonnes numériques et catégorielles."""
        ...

    def analyze_risk_distribution(
        self, df: DataFrame, risk_score_col: str, diabetes_stage_col: str
    ) -> None:
        """Analyse la distribution du score de risque par stade de diabète."""
        ...

    def analyze_risk_score(
        self,
        df: DataFrame,
        risk_score_col: str,
        diabetes_stage_col: str,
        target_col: str,
    ) -> None:
        """Analyse la relation entre score de risque, stade et cible."""
        ...

    def plot_numeric_feature_distribution(self, df: DataFrame, column: str) -> None:
        """Trace la distribution d'une variable numérique."""
        ...

    def plot_numeric_vs_target(self, df: DataFrame, column: str) -> None:
        """Trace la relation entre une variable numérique et la cible."""
        ...
