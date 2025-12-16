"""
experiment_tracking_service.py
==============================

Service APPLICATIF pour le tracking d’expériences ML.

RÔLE ARCHITECTURAL
------------------
- Centralise la logique transversale de tracking.
- Ne contient AUCUNE dépendance vers MLflow.
- Appelle uniquement le ExperimentTrackingPort.

Ce service est utilisé par les use cases (train, evaluate, etc.).
"""

from typing import Mapping, Any

from health_lifestyle_diabetes.domain.ports.experiment_tracking_port import (
    ExperimentTrackingPort,
)
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)


class ExperimentTrackingService:
    """
    Service applicatif de tracking d’expériences ML.

    Il standardise :
    - le nom des expériences
    - le cycle start / log / end
    """

    def __init__(self, tracker: ExperimentTrackingPort):
        self.tracker = tracker
        self.logger = LoguruLoggerAdapter("application.experiment_tracking")

    def start_experiment(self, *, experiment_name: str, run_name: str):
        """
        Initialise une expérience et démarre une run proprement.
        Si une run est déjà active, elle est fermée avant.
        """
        self.logger.info(
            f"Starting experiment '{experiment_name}' with run '{run_name}'"
        )

        self.tracker.end_run()
        self.tracker.setup_experiment(experiment_name)
        self.tracker.start_run(run_name)

    def log_training_context(self, *, model_name: str, params: Mapping[str, Any]):
        """
        Logger les informations liées à l’entraînement.
        """
        self.logger.debug(
            f"Logging training context for model '{model_name}'"
        )

        self.tracker.log_params(
            {
                "model_name": model_name,
                **params,
            }
        )

    def log_evaluation(self, metrics: Mapping[str, float]):
        """
        Logger les métriques d’évaluation.
        """
        self.logger.debug(
            f"Logging evaluation metrics: {list(metrics.keys())}"
        )

        self.tracker.log_metrics(metrics)

    def log_artifact(self, path: str):
        """
        Logger un artefact produit par le modèle.
        """
        self.logger.debug(
            f"Logging artifact at path: {path}"
        )

        self.tracker.log_artifact(path)

    def close(self):
        """
        Fermer proprement la run.
        """
        self.logger.info("Closing experiment run")
        self.tracker.end_run()
