from dataclasses import dataclass, field

import pandas as pd
from pandas import DataFrame

from health_lifestyle_diabetes.application.use_cases.perform_eda_uc import (
    PerformEDAUseCase,
)
from health_lifestyle_diabetes.domain.ports import EDAServicePort


@dataclass
class FakeEDAService(EDAServicePort):
    summary_df: DataFrame
    numeric_cols: list[str]
    categorical_cols: list[str]
    target_summary: DataFrame = field(
        default_factory=lambda: DataFrame({"category": [], "count": []})
    )
    risk_distribution_called: bool = False
    risk_score_called: bool = False
    target_distribution_called: bool = False
    numeric_distribution_calls: list[str] = field(default_factory=list)
    numeric_vs_target_calls: list[str] = field(default_factory=list)
    categorical_proportion_calls: list[str] = field(default_factory=list)
    target_within_category_calls: list[str] = field(default_factory=list)

    def summarize_dataset(self, df: DataFrame) -> DataFrame:
        return self.summary_df

    def identify_feature_types(self, df: DataFrame) -> tuple[list[str], list[str]]:
        return self.numeric_cols, self.categorical_cols

    def analyze_risk_distribution(
        self, df: DataFrame, risk_score_col: str, diabetes_stage_col: str
    ) -> None:
        self.risk_distribution_called = True

    def analyze_risk_score(
        self,
        df: DataFrame,
        risk_score_col: str,
        diabetes_stage_col: str,
        target_col: str,
    ) -> None:
        self.risk_score_called = True

    def plot_numeric_feature_distribution(self, df: DataFrame, column: str) -> None:
        self.numeric_distribution_calls.append(column)

    def plot_numeric_vs_target(self, df: DataFrame, column: str) -> None:
        self.numeric_vs_target_calls.append(column)

    def plot_target_distribution(self, df: DataFrame, target_col: str):
        self.target_distribution_called = True
        return None, self.target_summary

    def plot_categorical_proportions(self, df: DataFrame, column: str):
        self.categorical_proportion_calls.append(column)
        return None, DataFrame({"category": ["x"], "proportion": [100]})

    def plot_target_distribution_within_category(
        self, df: DataFrame, cat_col: str, target_col: str
    ):
        self.target_within_category_calls.append((cat_col, target_col))
        return None, DataFrame({"cat": [cat_col], "target": [target_col], "count": [1]})


class TestPerformEDAUseCase:
    def test_execute_runs_all_steps_with_risk_columns(self):
        df = pd.DataFrame(
            {
                "diagnosed_diabetes": [0, 1, 0],
                "diabetes_risk_score": [0.2, 0.8, 0.5],
                "diabetes_stage": ["A", "B", "A"],
                "age": [30, 45, 60],
                "bmi": [22.5, 27.4, 30.1],
                "gender": ["F", "M", "F"],
            }
        )

        fake_service = FakeEDAService(
            summary_df=pd.DataFrame({"Column": ["age"], "Type": ["int"]}),
            numeric_cols=["age", "bmi"],
            categorical_cols=["diabetes_stage", "gender"],
            target_summary=pd.DataFrame({"category": [0, 1], "count": [2, 1]}),
        )

        use_case = PerformEDAUseCase(fake_service)
        result = use_case.execute(df)

        assert result["summary"].equals(fake_service.summary_df)
        assert result["numeric_columns"] == ["age", "bmi"]
        assert result["categorical_columns"] == ["diabetes_stage", "gender"]
        assert result["target_distribution_summary"].equals(fake_service.target_summary)
        assert len(result["categorical_analysis"]) == 2

        assert fake_service.risk_distribution_called
        assert fake_service.risk_score_called
        assert fake_service.target_distribution_called
        assert fake_service.numeric_distribution_calls == ["age", "bmi"]
        assert fake_service.numeric_vs_target_calls == ["age", "bmi"]
        assert fake_service.categorical_proportion_calls == ["diabetes_stage", "gender"]
        assert fake_service.target_within_category_calls == [
            ("diabetes_stage", "diagnosed_diabetes"),
            ("gender", "diagnosed_diabetes"),
        ]

    def test_execute_raises_on_empty_dataframe(self):
        use_case = PerformEDAUseCase(
            FakeEDAService(pd.DataFrame(), [], []),
        )

        empty_df = pd.DataFrame()
        try:
            use_case.execute(empty_df)
        except ValueError as exc:
            assert "DataFrame fourni est vide" in str(exc)
        else:
            raise AssertionError("Expected ValueError for empty DataFrame")
