"""
DOCTRINE — MLFLOW ADAPTER (INFRASTRUCTURE)
=========================================

RÔLE ARCHITECTURAL
------------------
Ce fichier est un ADAPTER au sens Clean Architecture.

Il implémente le ExperimentTrackingPort défini dans le domaine
en utilisant MLflow comme technologie concrète.

RESPONSABILITÉS
---------------
- Traduire les appels abstraits → appels MLflow
- Créer ou récupérer les expériences
- Gérer l’artifact_location
- Gérer le cycle de vie des runs

AUTORISATIONS
-------------
- Peut importer MLflow
- Peut utiliser MlflowClient
- Peut utiliser le logger infrastructure

INTERDICTIONS
-------------
- Ne doit pas contenir de logique métier
- Ne doit pas appeler de use case
"""

import mlflow
from typing import Mapping, Any

from health_lifestyle_diabetes.domain.ports.experiment_tracking_port import (
    ExperimentTrackingPort,
)
from health_lifestyle_diabetes.infrastructure.tracking.mlflow_setup import (
    MLflowConfigurator,
)
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)


class MLflowTrackingAdapter(ExperimentTrackingPort):
    """
    Implémentation MLflow du port de tracking d’expériences.
    """

    def __init__(self):
        self.logger = LoguruLoggerAdapter("mlflow.adapter")
        self.client, self.artifact_location = MLflowConfigurator().configure()

    def setup_experiment(self, name: str) -> str:
        existing = self.client.get_experiment_by_name(name)

        if existing:
            exp_id = existing.experiment_id
            self.logger.info(f"Expérience existante : {name}")
        else:
            exp_id = self.client.create_experiment(
                name=name,
                artifact_location=self.artifact_location,
            )
            self.logger.info(
                f"Expérience créée : {name} "
                f"(artifact_location={self.artifact_location})"
            )

        mlflow.set_experiment(experiment_id=exp_id)
        return exp_id

    def start_run(self, run_name: str | None = None) -> None:
        mlflow.start_run(run_name=run_name)

    def log_params(self, params: Mapping[str, Any]) -> None:
        mlflow.log_params(params)

    def log_metrics(self, metrics: Mapping[str, float]) -> None:
        mlflow.log_metrics(metrics)

    def log_artifact(self, path: str) -> None:
        mlflow.log_artifact(path)

    def end_run(self) -> None:
        """
        Termine la run MLflow active (si existante).
        """
        if mlflow.active_run() is not None:
            mlflow.end_run()