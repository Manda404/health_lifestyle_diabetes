from typing import Protocol, Any
import pandas as pd


class ModelTrainerPort(Protocol):
    """
    Port définissant ce que le domaine attend d’un service d'entraînement de modèle ML.
    """

    def train(self, X: pd.DataFrame, y: pd.Series) -> object:
        """
        Entraîne un modèle et retourne l'instance entraînée.
        """
        ...

    def predict(self, model: Any, X: pd.DataFrame) -> pd.Series:
        """
        Génère des prédictions à partir d'un modèle entraîné.
        """
        ...
    
    def evaluate(self,model: Any, y_true: pd.Series,):
        """
        Génère la matrix de confusion pour evaluer grafiquement les performance du model
        """
        ...