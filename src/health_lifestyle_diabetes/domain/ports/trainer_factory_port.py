# src/health_lifestyle_diabetes/domain/ports/trainer_factory_port.py

from typing import Protocol

from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort


class TrainerFactoryPort(Protocol):
    """
    Port de fabrique de ModelTrainer.

    Rôle :
    ------
    Fournir dynamiquement une implémentation de ModelTrainerPort
    en fonction d'un identifiant de modèle (ex: "catboost", "xgboost").

    Pourquoi une Factory ?
    ----------------------
    - éviter les `if/else` ou `match` dans les use cases,
    - respecter l'inversion de dépendance (DIP),
    - permettre l'ajout de nouveaux modèles sans modifier l'application.

    Ce port est défini dans le domaine car :
    --------------------------------------
    - le domaine a besoin de créer un "entraîneur",
    - le domaine ne doit PAS connaître les classes concrètes (CatBoostTrainer, etc.).
    """

    def create(self, model_name: str) -> ModelTrainerPort:
        """
        Retourne une implémentation concrète de ModelTrainerPort
        correspondant au modèle demandé.

        Parameters
        ----------
        model_name : str
            Identifiant logique du modèle (ex: "catboost", "xgboost").

        Returns
        -------
        ModelTrainerPort
            Entraîneur du modèle demandé.

        Raises
        ------
        ValueError
            Si le modèle demandé n'est pas supporté.
        """
        ...
