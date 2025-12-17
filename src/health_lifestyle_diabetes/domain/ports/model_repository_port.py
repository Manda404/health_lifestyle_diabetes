"""
Port (interface) pour la persistance des modèles ML.

Objectif :
----------
- Permettre au domaine de sauvegarder/charger des modèles
  sans connaître la technologie de serialization/deserialization
  (pickle, joblib, ONNX, MLflow, etc.).
"""

from pathlib import Path
from typing import Any, Protocol


class ModelRepositoryPort(Protocol):
    """
    Interface pour gérer la persistance des modèles ML.
    """

    def save_model(self, model: Any, path: Path) -> None:
        """
        Sauvegarde un modèle vers un chemin donné.

        Paramètres
        ----------
        model : Any
            Instance du modèle entraîné (ex: objet sklearn, XGBoost, CatBoost).
        path : Path
            Chemin de destination.
        """
        ...

    def load_model(self, path: Path) -> Any:
        """
        Charge un modèle depuis un chemin donné.

        Paramètres
        ----------
        path : Path
            Chemin de la ressource contenant le modèle.

        Retour
        ------
        Any
            Modèle chargé.
        """
        ...
