# src/health_lifestyle_diabetes/domain/ports/model_trainer_port.py

from __future__ import annotations

from typing import Any, Protocol


class ModelTrainerPort(Protocol):
    """
    Port définissant ce que le domaine attend d’un service d'entraînement
    et d'inférence pour un modèle ML.
    """

    def train(
        self,
        X_train: Any,
        y_train: Any,
        X_valid: Any | None = None,
        y_valid: Any | None = None,
    ) -> Any:
        """
        Entraîne un modèle et retourne l'instance entraînée.
        """
        ...
