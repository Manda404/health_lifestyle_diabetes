# src/health_lifestyle_diabetes/infrastructure/ml/model_trainers/xgboost_trainer.py

from typing import Any, Dict

from pandas import DataFrame, Series
from xgboost import XGBClassifier

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger


class XGBoostTrainer(ModelTrainerPort):
    """
    Implémentation infrastructure du port ModelTrainerPort
    pour l'entraînement d'un modèle XGBoost.

    Responsabilités :
    -----------------
    - validation minimale des données d'entrée,
    - instanciation du modèle XGBoost,
    - entraînement avec ou sans validation,
    - journalisation via LoggerPort (Clean Architecture).
    """

    def __init__(self, params: Dict[str, Any], logger: LoggerPort):
        """
        Parameters
        ----------
        params : dict
            Hyperparamètres du modèle XGBoost.
        logger : LoggerPort
            Service de logging injecté (adapter infrastructure).
        """
        self.params = params
        self.logger = get_logger("trainer.XGBoostTrainer")
        self.model_name = "xgboost"

    def train(
        self,
        X_train: DataFrame,
        y_train: Series,
        X_valid: DataFrame | None = None,
        y_valid: Series | None = None,
    ) -> XGBClassifier:
        """
        Entraîne un modèle XGBoost.

        Parameters
        ----------
        X_train : DataFrame
            Features d'entraînement.
        y_train : Series
            Labels d'entraînement.
        X_valid : DataFrame, optionnel
            Features de validation.
        y_valid : Series, optionnel
            Labels de validation.

        Returns
        -------
        XGBClassifier
            Modèle XGBoost entraîné.
        """

        # -------------------------
        # Validation minimale
        # -------------------------
        if X_train.empty or y_train.empty:
            raise ValueError("X_train ou y_train est vide.")

        if X_valid is not None and y_valid is not None:
            if len(X_valid) != len(y_valid):
                raise ValueError("X_valid et y_valid doivent avoir la même taille.")

        self.logger.info(
            f"Entraînement XGBoost | train={X_train.shape}, "
            f"valid={X_valid.shape if X_valid is not None else 'N/A'}"
        )

        # -------------------------
        # Création du modèle
        # -------------------------
        model = XGBClassifier(
            **self.params,
            eval_metric="logloss",  # obligatoire pour éviter les warnings
            tree_method="hist",  # rapide sur CPU récents
            use_label_encoder=False,
        )

        # -------------------------
        # Entraînement
        # -------------------------
        self.logger.info("Démarrage de l'entraînement XGBoost.")

        if X_valid is not None and y_valid is not None:
            model.fit(
                X_train,
                y_train,
                eval_set=[(X_valid, y_valid)],
                verbose=False,
            )
        else:
            model.fit(X_train, y_train)

        self.logger.info("Entraînement XGBoost terminé.")

        return model
