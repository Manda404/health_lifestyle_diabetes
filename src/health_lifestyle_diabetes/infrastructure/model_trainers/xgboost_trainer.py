# src/health_lifestyle_diabetes/infrastructure/model_trainers/xgboost_trainer.py

from typing import Any, Dict, Optional

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    XGBoostTrainingError,
)
from pandas import DataFrame, Series
from xgboost import XGBClassifier


class XGBoostTrainer(ModelTrainerPort):
    """
    Implémentation infrastructure du port ModelTrainerPort
    pour l'entraînement d'un modèle XGBoost.
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
        self.logger = logger
        self.logger.info("XGBoostTrainer initialisé avec les paramètres fournis.")

    def train(
        self,
        X_train: DataFrame,
        y_train: Series,
        X_valid: Optional[DataFrame] = None,
        y_valid: Optional[Series] = None,
    ) -> XGBClassifier:
        """
        Entraîne un modèle XGBoost.

        Parameters
        ----------
        X_train : DataFrame
            Matrice de caractéristiques d'entraînement.
        y_train : Series
            Vecteur cible d'entraînement.
        X_valid : DataFrame, optional
            Matrice de caractéristiques de validation.
        y_valid : Series, optional
            Vecteur cible de validation.

        Returns
        -------
        XGBClassifier
            Modèle XGBoost entraîné.
        """

        # -------------------------
        # 1. Validation minimale
        # -------------------------
        if X_train.empty or y_train.empty:
            raise ValueError("X_train ou y_train est vide.")

        if len(X_train) != len(y_train):
            raise ValueError("X_train et y_train doivent avoir la même taille.")

        if X_valid is not None and y_valid is not None:
            if len(X_valid) != len(y_valid):
                raise ValueError("X_valid et y_valid doivent avoir la même taille.")
        # -------------------------
        # 2. Protection contre les effets de bord (copy)
        # -------------------------
        X_train = X_train.copy()
        if X_valid is not None:
            X_valid = X_valid.copy()

        # -------------------------
        # 3. Conversion catégorielle contrôlée
        # -------------------------
        cat_cols = X_train.select_dtypes(exclude="number").columns.tolist()
        for col in cat_cols:
            X_train[col] = X_train[col].astype("category")
            if X_valid is not None and col in X_valid.columns:
                X_valid[col] = X_valid[col].astype("category")

        # -------------------------
        # 4. Logging
        # -------------------------
        self.logger.info(
            f"XGBoost - Entraînement | train={X_train.shape}, "
            f"valid={X_valid.shape if X_valid is not None else 'N/A'}"
        )
        self.logger.debug(f"XGBoost - Hyperparamètres: {self.params}")

        # -------------------------
        # 5. Initialisation du modèle
        # -------------------------
        if cat_cols is not None and len(cat_cols) > 0:
            self.logger.info(
                f"XGBoost - Variables catégorielles détectées : {cat_cols}"
            )
            self.params["enable_categorical"] = True
        model = XGBClassifier(
            **self.params,
            tree_method="hist",      # optimisé CPU
        )

        # -------------------------
        # 6. Entraînement
        # -------------------------
        try:
            self.logger.info("XGBoost - Démarrage de l'entraînement...")

            if X_valid is not None and y_valid is not None:
                model.fit(
                    X_train,
                    y_train,
                    eval_set=[
                        (X_train, y_train),
                        (X_valid, y_valid),
                    ],
                    #eval_metric=self.params.get("eval_metric", "logloss"),
                    #early_stopping_rounds=self.params.get("early_stopping_rounds", None),
                    verbose=True,
                )
            else:
                model.fit(X_train, y_train)

            self.logger.info("XGBoost - Entraînement terminé avec succès.")

        except Exception as e:
            self.logger.error(f"XGBoost - Erreur lors du fit : {e}")
            raise XGBoostTrainingError(
                f"Échec de l'entraînement du modèle XGBoost: {e}"
            ) from e

        return model
