from pandas import DataFrame
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)

class BehavioralFeatureEngineer:
    """
    Génère des indicateurs comportementaux dérivés des habitudes de vie.

    Objectif :
    ----------
    Quantifier les déséquilibres comportementaux modernes
    (sédentarité, écrans, sommeil, activité physique).

    Justification médicale :
    ------------------------
    Les habitudes de vie influencent directement :
    - la sensibilité à l'insuline
    - l'inflammation chronique
    - le métabolisme énergétique

    Pertinence métier :
    -------------------
    Introduit une dimension préventive et modifiable
    dans les modèles de risque diabétique.
    """
    def __init__(self):
        self.logger = LoguruLoggerAdapter("fe.BehavioralFeatureEngineer")

    def transform(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        self.logger.info("Création des features comportementales avancées...")

        # ------------------------------------------------------------------
        # 1. Ratio d'adéquation de l'activité physique
        # ------------------------------------------------------------------
        df["activity_adequacy_ratio"] = (
            df["physical_activity_minutes_per_week"] / 150
        ).clip(upper=3)
        """
        - 150 min / semaine = recommandation OMS
        - <1 : insuffisant
        - >=1 : conforme ou protecteur
        """

        # ------------------------------------------------------------------
        # 2. Déséquilibre écran / sommeil
        # ------------------------------------------------------------------
        df["screen_sleep_ratio"] = (
            df["screen_time_hours_per_day"] / df["sleep_hours_per_day"]
        ).clip(upper=5)
        """
        Un ratio élevé est associé à :
        - perturbation circadienne
        - résistance à l'insuline
        """

        # ------------------------------------------------------------------
        # 3. Sédentarité ajustée
        # ------------------------------------------------------------------
        df["sedentary_risk_flag"] = (
            (df["screen_time_hours_per_day"] >= 6)
            & (df["physical_activity_minutes_per_week"] < 150)
        ).astype(int)
        """
        Identifie les profils à forte exposition sédentaire
        malgré une activité physique insuffisante.
        """

        self.logger.info("Features comportementales avancées générées.")
        return df