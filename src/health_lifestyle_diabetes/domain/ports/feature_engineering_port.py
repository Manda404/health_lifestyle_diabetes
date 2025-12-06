from typing import Protocol
import pandas as pd

class FeatureEngineeringPort(Protocol):
    """
    Décrit ce que le système attend du feature engineering.
    """

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        ...
