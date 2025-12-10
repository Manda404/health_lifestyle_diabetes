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
    risk_distribution_called: bool = False
    risk_score_called: bool = False
    numeric_distribution_calls: list[str] = field(default_factory=list)
    numeric_vs_target_calls: list[str] = field(default_factory=list)

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


class TestPerformEDAUseCase:
    def test_execute_runs_all_steps_with_risk_columns(self):
        df = pd.DataFrame(
            {
                "diagnosed_diabetes": [0, 1, 0],
                "diabetes_risk_score": [0.2, 0.8, 0.5],
                "diabetes_stage": ["A", "B", "A"],
                "age": [30, 45, 60],
                "bmi": [22.5, 27.4, 30.1],
            }
        )

        fake_service = FakeEDAService(
            summary_df=pd.DataFrame({"Column": ["age"], "Type": ["int"]}),
            numeric_cols=["age", "bmi"],
            categorical_cols=["diabetes_stage"],
        )

        use_case = PerformEDAUseCase(fake_service)
        result = use_case.execute(df)

        assert result["summary"].equals(fake_service.summary_df)
        assert result["numeric_columns"] == ["age", "bmi"]
        assert result["categorical_columns"] == ["diabetes_stage"]

        assert fake_service.risk_distribution_called
        assert fake_service.risk_score_called
        assert fake_service.numeric_distribution_calls == ["age", "bmi"]
        assert fake_service.numeric_vs_target_calls == ["age", "bmi"]

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
