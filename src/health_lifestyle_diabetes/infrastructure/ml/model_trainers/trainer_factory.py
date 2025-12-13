# src/health_lifestyle_diabetes/infrastructure/ml/model_trainers/trainer_factory.py

from typing import Any, Dict

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.trainer_factory_port import (
    TrainerFactoryPort,
)
from health_lifestyle_diabetes.infrastructure.ml.model_trainers.catboost_trainer import (
    CatBoostTrainer,
)
from health_lifestyle_diabetes.infrastructure.ml.model_trainers.xgboost_trainer import (
    XGBoostTrainer,
)


class TrainerFactory(TrainerFactoryPort):
    """
    Implémentation concrète de TrainerFactoryPort.

    Responsabilités :
    -----------------
    - instancier les entraîneurs concrets (CatBoost, XGBoost),
    - injecter les dépendances nécessaires (logger, paramètres),
    - centraliser la logique de sélection du modèle.

    Clean Architecture :
    --------------------
    - dépend du domaine (TrainerFactoryPort),
    - dépend des implémentations ML concrètes,
    - n'est JAMAIS appelée directement par le domaine.

    Cette classe appartient à l'infrastructure car :
    -----------------------------------------------
    - elle dépend de bibliothèques ML spécifiques,
    - elle connaît les classes concrètes CatBoostTrainer / XGBoostTrainer.
    """

    def __init__(
        self,
        *,
        catboost_params: Dict[str, Any],
        xgboost_params: Dict[str, Any],
        logger: LoggerPort,
    ):
        """
        Parameters
        ----------
        catboost_params : dict
            Hyperparamètres CatBoost.
        xgboost_params : dict
            Hyperparamètres XGBoost.
        logger : LoggerPort
            Service de logging injecté.
        """
        self.catboost_params = catboost_params
        self.xgboost_params = xgboost_params
        self.logger = logger

    def create(self, model_name: str):
        """
        Crée et retourne un entraîneur de modèle.

        Parameters
        ----------
        model_name : str
            Nom logique du modèle ("catboost" ou "xgboost").

        Returns
        -------
        ModelTrainerPort
            Entraîneur du modèle demandé.

        Raises
        ------
        ValueError
            Si le modèle demandé n'est pas supporté.
        """
        self.logger.info(f"Création du trainer pour le modèle : {model_name}")

        if model_name == "catboost":
            return CatBoostTrainer(
                params=self.catboost_params,
                logger=self.logger,
            )

        if model_name == "xgboost":
            return XGBoostTrainer(
                params=self.xgboost_params,
                logger=self.logger,
            )

        raise ValueError(f"Modèle inconnu : {model_name}")
