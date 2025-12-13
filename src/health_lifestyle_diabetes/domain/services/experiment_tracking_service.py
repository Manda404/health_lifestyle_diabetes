"""
experiment_tracking_service.py
==============================

📌 RÔLE :
---------
Service APPLICATIF pour standardiser le tracking ML.

📌 RESPONSABILITÉS :
-------------------
- Orchestrer le cycle de vie du tracking
- Appliquer des conventions (naming, structure)
- Appeler le ExperimentTrackingPort

📌 INTERDIT :
------------
- Aucune dépendance MLflow
- Aucune logique métier

Plus:
------------
Service APPLICATIF pour le tracking d’expériences ML.

📌 Rôle dans la Clean Architecture
---------------------------------
- Centralise la logique transversale de tracking.
- Ne contient AUCUNE dépendance vers MLflow.
- Appelle uniquement le ExperimentTrackingPort.

Ce service est utilisé par les use cases (train, evaluate, etc.).
"""
"""
DOCTRINE — EXPERIMENT TRACKING SERVICE (APPLICATION)
====================================================

RÔLE ARCHITECTURAL
------------------
Ce fichier appartient à la couche APPLICATION.

Il orchestre l’utilisation du tracking dans les cas d’usage,
sans jamais dépendre d’une technologie concrète.

DIFFÉRENCE AVEC LE DOMAINE
-------------------------
- Le domaine définit CE QUI est nécessaire
- L’application définit QUAND et COMMENT on l’utilise

RESPONSABILITÉS
---------------
- Centraliser les conventions de tracking
- Éviter la duplication dans les use cases
- Garder les use cases lisibles

INTERDICTIONS
-------------
- Aucune dépendance MLflow
- Aucune logique métier
- Aucune configuration technique
"""

from typing import Mapping, Any

from health_lifestyle_diabetes.domain.ports.experiment_tracking_port import (
    ExperimentTrackingPort,
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

    def start_experiment(self, *, experiment_name: str, run_name: str):
        """
        Initialise une expérience et démarre une run proprement.
        Si une run est déjà active, elle est fermée avant.
        """
        self.tracker.end_run()          # beaucoup plus sécurisation
        self.tracker.setup_experiment(experiment_name)
        self.tracker.start_run(run_name)

    def log_training_context(self, *, model_name: str, params: Mapping[str, Any]):
        """
        Logger les informations liées à l’entraînement.
        """
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
        self.tracker.log_metrics(metrics)

    def log_artifact(self, path: str):
        """
        Logger un artefact produit par le modèle.
        """
        self.tracker.log_artifact(path)

    def close(self):
        """
        Fermer proprement la run.
        """
        self.tracker.end_run()