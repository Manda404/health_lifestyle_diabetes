from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import DataFrame

logger = get_logger("fe.LifestyleFeatureEngineer")


class LifestyleFeatureEngineer:
    """
    Crée des variables comportementales liées à l’hygiène de vie.

    Objectif :
    ----------
    Quantifier l’impact des habitudes (activité, sommeil, alcool, tabac)
    sur le risque métabolique global.

    Justification médicale :
    ------------------------
    Un mode de vie sain améliore la sensibilité à l’insuline,
    réduit l’inflammation chronique et favorise la prévention du diabète.

    Pertinence métier :
    -------------------
    Ces indicateurs permettent d’intégrer une dimension comportementale
    dans les modèles prédictifs et les tableaux de bord de prévention.
    """

    def __init__(self):
        self.logger = logger

    def _compute_lifestyle_score(self, df: DataFrame) -> DataFrame:
        def lifestyle(row):
            score = 0
            score += 2 if row["diet_score"] >= 6 else 0
            score += 2 if row["physical_activity_minutes_per_week"] >= 150 else 0
            score += 2 if 7 <= row["sleep_hours_per_day"] <= 9 else 0
            score += 2 if row["alcohol_consumption_per_week"] <= 2 else 0
            score += 2 if row["smoking_status"] == "Never" else 0
            return score

        df["lifestyle_score"] = df.apply(lifestyle, axis=1)
        return df

    def _compute_sleep_efficiency(self, df: DataFrame) -> DataFrame:
        df["sleep_efficiency"] = (
            df["sleep_hours_per_day"] / (df["screen_time_hours_per_day"] + 1)
        ).clip(upper=2)
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Application des transformations lifestyle...")
        df = self._compute_lifestyle_score(df)
        df = self._compute_sleep_efficiency(df)
        self.logger.info("Transformations lifestyle complétées.")
        return df
