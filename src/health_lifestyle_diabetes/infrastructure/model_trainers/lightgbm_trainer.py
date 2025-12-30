from typing import Any, Dict, Optional

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.utils.exceptions import LightGBMTrainingError
from lightgbm import LGBMClassifier
from pandas import DataFrame, Series


class LightGBMTrainer(ModelTrainerPort):
    """
    Entraîne un modèle LightGBM.
    Gère automatiquement les colonnes catégorielles.
    """

    def __init__(self, params: Dict[str, Any], logger: LoggerPort):
        self.params = params
        self.logger = logger
        self.model_name = "lightgbm"
        self.logger.info("Initialisation LightGBMTrainer terminée.")

    def train(
        self,
        X_train: DataFrame,
        y_train: Series,
        X_valid: Optional[DataFrame] = None,
        y_valid: Optional[Series] = None,
    ) -> LGBMClassifier:

        self.logger.debug("Début de la méthode train()")

        # ---------- VALIDATION ----------
        self.logger.info("Validation des données...")
        if X_train.empty or y_train.empty:
            self.logger.error("X_train ou y_train est vide.")
            raise LightGBMTrainingError("X_train ou y_train est vide.")
        if len(X_train) != len(y_train):
            raise LightGBMTrainingError("X_train et y_train doivent avoir la même taille.")
        if X_valid is not None and y_valid is not None and len(X_valid) != len(y_valid):
            raise LightGBMTrainingError("X_valid et y_valid doivent avoir la même taille.")

        self.logger.info(f"Taille train: {X_train.shape}")
        self.logger.info(f"Taille valid: {X_valid.shape if X_valid is not None else 'N/A'}")

        # ---------- COPY FOR SAFETY (fix pandas warnings) ----------
        X_train = X_train.copy()
        if X_valid is not None:
            X_valid = X_valid.copy()

        # ---------- CATEGORICAL FEATURES ----------
        self.logger.info("Détection et conversion des colonnes catégorielles...")
        cat_cols = list(X_train.select_dtypes(include="number").columns)

        if cat_cols:
            self.logger.debug(f"Colonnes catégorielles détectées: {cat_cols[:2]}")

        # ---------- MODEL INIT ----------
        self.logger.info("Initialisation du modèle LightGBM...")
        self.logger.debug(f"Hyperparamètres LightGBM: {self.params}")
        self.params.update({
            "force_col_wise": True
        })
        model = LGBMClassifier(**self.params)

        # ---------- TRAINING ----------
        self.logger.info("Début de l'entraînement LightGBM...")
        try:
            if X_valid is not None and y_valid is not None:
                self.logger.debug("Mode avec validation.")
                model.fit(
                    X_train,
                    y_train,
                    eval_set=[(X_train, y_train), (X_valid, y_valid)],
                    eval_names=["train", "valid"],
                    eval_metric=self.params.get("eval_metric", "logloss"),
                    categorical_feature=cat_cols if cat_cols else None,
                )
            else:
                self.logger.debug("Mode sans validation.")
                model.fit(
                    X_train,
                    y_train,
                    categorical_feature=cat_cols if cat_cols else None,
                )

        except Exception as e:
            self.logger.error(f"Erreur pendant l'entraînement: {e}")
            raise LightGBMTrainingError(f"Échec de l'entraînement LightGBM: {e}") from e

        self.logger.info("LightGBM - Entraînement terminé avec succès.")
        self.logger.debug("Fin de train().")
        return model