from pandas import DataFrame

from health_lifestyle_diabetes.domain.ports.eda_service_port import EDAServicePort
from health_lifestyle_diabetes.infrastructure.ml.eda.categorical_analysis import (
    plot_categorical_proportions,
    plot_target_distribution,
    plot_target_distribution_within_category,
)
from health_lifestyle_diabetes.infrastructure.ml.eda.dataset_summary import (
    identify_feature_types,
    summarize_dataset,
)
from health_lifestyle_diabetes.infrastructure.ml.eda.numeric_analysis import (
    analyze_risk_distribution,
    analyze_risk_score,
    plot_numeric_feature_distribution,
    plot_numeric_vs_target,
)


class EDAService(EDAServicePort):
    """Implémentation concrète des fonctionnalités EDA exposées via un port."""

    def summarize_dataset(self, df: DataFrame) -> DataFrame:
        return summarize_dataset(df)

    def identify_feature_types(self, df: DataFrame) -> tuple[list[str], list[str]]:
        return identify_feature_types(df)

    def analyze_risk_distribution(
        self, df: DataFrame, risk_score_col: str, diabetes_stage_col: str
    ) -> None:
        analyze_risk_distribution(df, risk_score_col, diabetes_stage_col)

    def analyze_risk_score(
        self,
        df: DataFrame,
        risk_score_col: str,
        diabetes_stage_col: str,
        target_col: str,
    ) -> None:
        analyze_risk_score(df, risk_score_col, diabetes_stage_col, target_col)

    def plot_numeric_feature_distribution(self, df: DataFrame, column: str) -> None:
        plot_numeric_feature_distribution(df, column)

    def plot_numeric_vs_target(self, df: DataFrame, column: str) -> None:
        plot_numeric_vs_target(df, column)

    def plot_target_distribution(self, df: DataFrame, target_col: str):
        return plot_target_distribution(df, target_col)

    def plot_categorical_proportions(self, df: DataFrame, column: str):
        return plot_categorical_proportions(df, column)

    def plot_target_distribution_within_category(
        self, df: DataFrame, cat_col: str, target_col: str
    ):
        return plot_target_distribution_within_category(df, cat_col, target_col)
