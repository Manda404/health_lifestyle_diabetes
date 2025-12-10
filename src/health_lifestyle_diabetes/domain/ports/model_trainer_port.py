# src/health_lifestyle_diabetes/domain/ports/model_trainer_port.py
from typing import Any, Protocol

from pandas import DataFrame, Series


class ModelTrainerPort(Protocol):
    """
    Port définissant ce que le domaine attend d’un service d'entraînement
    et d'inférence pour un modèle ML.
    """

    def train(
        self,
        X_train: DataFrame,
        y_train: Series,
        X_valid: DataFrame,
        y_valid: Series,
    ) -> Any:
        """
        Entraîne un modèle et retourne l'instance entraînée.
        """
        ...

    def predict_proba(self, model: Any, X: DataFrame) -> Series:
        """
        Génère les probabilités prédites pour la classe positive.
        """
        ...
