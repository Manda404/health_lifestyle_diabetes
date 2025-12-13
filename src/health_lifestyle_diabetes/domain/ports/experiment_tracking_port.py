"""
experiment_tracking_port.py
===========================

Ce fichier définit le PORT de tracking d’expériences ML.

📌 Rôle dans la Clean Architecture
---------------------------------
- Le domaine exprime ici un BESOIN, pas une implémentation.
- Il dit : "je veux pouvoir tracer des expériences, des paramètres,
  des métriques et des artefacts".
- Il ne sait PAS comment c’est fait (MLflow, autre outil, etc.).

Ce port sera implémenté dans la couche Infrastructure
(ex: via MLflow, WandB, ou autre).
"""
"""
experiment_tracking_port.py
===========================

📌 RÔLE :
---------
Définir le CONTRAT de tracking d’expériences ML attendu par le domaine.

📌 PRINCIPES CLEAN ARCHITECTURE :
--------------------------------
- Le domaine exprime un BESOIN.
- Il ne connaît AUCUNE technologie (MLflow, WandB, etc.).
- Toute implémentation devra respecter ce contrat.

👉 Ce port est implémenté par l’infrastructure.
"""
from typing import Any, Mapping, Protocol


class ExperimentTrackingPort(Protocol):
    """
    Port (contrat) pour le tracking d’expériences ML.

    Toute implémentation DOIT respecter ce contrat
    pour pouvoir être utilisée par l’application.
    """

    def setup_experiment(self, name: str) -> str:
        """
        Crée ou récupère une expérience.

        Parameters
        ----------
        name : str
            Nom logique de l’expérience (ex: "health_lifestyle_diabetes").

        Returns
        -------
        str
            Identifiant unique de l’expérience.
        """
        ...

    def start_run(self, run_name: str | None = None) -> None:
        """
        Démarre une nouvelle run de tracking.

        Parameters
        ----------
        run_name : str | None
            Nom optionnel de la run.
        """
        ...

    def log_params(self, params: Mapping[str, Any]) -> None:
        """
        Log des paramètres (hyperparamètres, config).

        Parameters
        ----------
        params : Mapping[str, Any]
            Dictionnaire clé / valeur.
        """
        ...

    def log_metrics(self, metrics: Mapping[str, float]) -> None:
        """
        Log des métriques numériques.

        Parameters
        ----------
        metrics : Mapping[str, float]
            Exemple : {"auc": 0.87, "f1": 0.78}
        """
        ...

    def log_artifact(self, path: str) -> None:
        """
        Log d’un artefact (fichier).

        Parameters
        ----------
        path : str
            Chemin du fichier à sauvegarder.
        """
        ...

    def end_run(self) -> None:
        """
        Termine la run active.
        """
        ...
