# application/services/experiment_tracking_service.py

from typing import Any, Mapping

from health_lifestyle_diabetes.domain.ports.experiment_tracking_port import (
    ExperimentTrackingPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class ExperimentTrackingService:
    """
    Service applicatif orchestrant le tracking d'expériences ML.

    - Utilisé par les cas d'usage (entraînement, évaluation, etc.)
    - Ne dépend d'aucune technologie (pas de MLflow ici)
    - Pilote le cycle complet : start → log → end
    """

    def __init__(self, tracker: ExperimentTrackingPort, logger: LoggerPort):
        self.tracker = tracker
        self.logger = logger
        self.logger.info("ExperimentTrackingService initialisé.")

    # -----------------------------------------
    # Cycle de vie des expériences
    # -----------------------------------------
    def start_experiment(self, *, experiment_name: str, run_name: str) -> None:
        """Démarre une nouvelle expérience et une run associée."""
        self.logger.info(
            f"Initialisation de l'expérience '{experiment_name}' (run='{run_name}')"
        )

        self.tracker.end_run()  # sécurité (si run précédente ouverte)
        self.tracker.setup_experiment(experiment_name)
        self.tracker.start_run(run_name)

    # -----------------------------------------
    # Logging contextuel
    # -----------------------------------------
    def log_training_context(self, *, model_name: str, params: Mapping[str, Any]) -> None:
        """Log des informations relatives à l'entraînement."""
        self.logger.debug(f"Enregistrement du contexte d'entraînement pour {model_name}")
        self.tracker.log_params({"model": model_name, **params})

    def log_evaluation(self, metrics: Mapping[str, float]) -> None:
        """Log des métriques d'évaluation."""
        self.logger.info(f"Métriques d'évaluation : {metrics}")
        self.tracker.log_metrics(metrics)

    def log_artifact(self, path: str) -> None:
        """Log d'un artefact produit par le modèle (fichier)."""
        self.logger.debug(f"Enregistrement d'un artefact : {path}")
        self.tracker.log_artifact(path)

    # -----------------------------------------
    # Fermeture de la session
    # -----------------------------------------
    def close(self) -> None:
        """Fin de l'expérience en cours."""
        self.logger.info("Fermeture de l'expérience.")
        self.tracker.end_run()
