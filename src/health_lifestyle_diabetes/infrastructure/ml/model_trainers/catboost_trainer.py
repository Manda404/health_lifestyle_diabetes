from typing import Any, Dict

from catboost import CatBoostClassifier
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import DataFrame, Series


class CatBoostTrainer(ModelTrainerPort):
    """
    Implémentation du port ModelTrainerPort pour entraîner un modèle CatBoost.
    """

    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.logger = get_logger("trainer.CatBoostTrainer")
        self.model_name = "catboost"

    def train(
        self,
        X_train: DataFrame,
        y_train: Series,
        X_valid: DataFrame,
        y_valid: Series,
    ) -> CatBoostClassifier:
        # --- Validation simple ---
        if X_train.empty or y_train.empty:
            raise ValueError("X_train ou y_train est vide.")

        if len(X_valid) != len(y_valid):
            raise ValueError("X_valid et y_valid doivent avoir la même taille.")

        # --- Catégories automatiques ---
        cat_features = X_train.select_dtypes(exclude="number").columns.tolist()
        if cat_features and "cat_features" not in self.params:
            self.logger.info(
                "Détection des variables catégoriques et mise à jour des paramètres."
            )
            self.params["cat_features"] = cat_features

        self.logger.info(
            f"Taille du train set : {X_train.shape}, valid set : {X_valid.shape}"
        )

        # --- Création du modèle ---
        model = CatBoostClassifier(**self.params)

        # --- Entraînement ---
        self.logger.info("Démarrage de l'entraînement du modèle CatBoost...")
        model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], use_best_model=True)
        self.logger.info("Entraînement CatBoost terminé.")

        return model

    def predict_proba(self, model: Any, X: DataFrame) -> Series:
        return Series(model.predict_proba(X)[:, 1], index=X.index, name="proba")
