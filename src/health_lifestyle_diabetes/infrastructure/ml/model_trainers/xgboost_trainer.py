import pandas as pd
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import Series
from xgboost import XGBClassifier

logger = get_logger("trainer.XGBoostTrainer")


class XGBoostTrainer(ModelTrainerPort):
    """
    Implémentation du port ModelTrainerPort pour XGBoost.
    """

    def __init__(self, params: dict):
        """
        Parameters
        ----------
        params : dict
            Dictionnaire des hyperparamètres XGBoost.
        """
        self.params = params
        self.logger = logger

    def train(self, X: pd.DataFrame, y: pd.Series):
        self.logger.info("Entraînement du modèle XGBoost...")

        model = XGBClassifier(
            **self.params,
            eval_metric="logloss",  # obligatoire pour éviter les warnings
            tree_method="hist",  # très rapide si CPU récent
        )

        model.fit(X, y)
        self.logger.info("Entraînement XGBoost terminé.")

        return model

    def predict_proba(self, model, X: pd.DataFrame) -> Series:
        """Retourne la probabilité de classe positive."""

        return Series(model.predict_proba(X)[:, 1], index=X.index, name="proba")
