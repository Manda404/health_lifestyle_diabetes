"""
Service EDA conforme au port `EDAServicePort`.

Il encapsule les fonctions EDA existantes pour éviter de les importer
directement dans la couche application.
"""

import pandas as pd
from health_lifestyle_diabetes.domain.ports.eda_service_port import EDAServicePort
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
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
from pandas import DataFrame


class PlotlyEDAService(EDAServicePort):
    def __init__(self, logger: LoggerPort) -> None:
        self.logger = logger

    def summarize_dataset(self, df: DataFrame) -> DataFrame:
        return summarize_dataset(df)

    def identify_feature_types(self, df: DataFrame):
        return identify_feature_types(df)

    def analyze_risk_distribution(
        self, df: DataFrame, score_col: str, stage_col: str
    ) -> None:
        self.logger.debug(
            "Analyse distribution du risque: score=%s, stage=%s",
            score_col,
            stage_col,
        )
        analyze_risk_distribution(df, score_col, stage_col)

    def analyze_risk_score(
        self, df: DataFrame, score_col: str, stage_col: str, diag_col: str
    ) -> None:
        self.logger.debug(
            "Analyse score de risque: score=%s, stage=%s, diag=%s",
            score_col,
            stage_col,
            diag_col,
        )
        analyze_risk_score(df, score_col, stage_col, diag_col)

    def plot_numeric_feature_distribution(self, df: pd.DataFrame, column: str) -> None:
        self.logger.debug("Distribution numérique pour %s", column)
        plot_numeric_feature_distribution(df, column)

    def plot_numeric_vs_target(self, df: pd.DataFrame, column: str) -> None:
        self.logger.debug("Analyse numeric vs target pour %s", column)
        plot_numeric_vs_target(df, column)
