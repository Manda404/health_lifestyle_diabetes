import pandas as pd
from catboost import CatBoostClassifier
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort

logger = get_logger("trainer.CatBoostTrainer")


class CatBoostTrainer(ModelTrainerPort):

    def __init__(self, params: dict):
        self.params = params
        self.logger = logger
        #self.model_name = "catboost"

    def train(self, X_train: pd.DataFrame, y_train: pd.Series, X_valid: pd.DataFrame, y_valid: pd.Series):


        # Identifie automatiquement les colonnes catégoriques
        cat_features = X_train.select_dtypes(exclude="number").columns.tolist()
        if len(cat_features) >=1 and "cat_features" not in self.params.keys():
            self.logger.info("Mise à jours des paramètres de fit()")
            self.params["cat_features"]=cat_features

        logger.info(f"Taille du train set : {X_train.shape}, valid set : {X_valid.shape}")
        eval_set = [(X_valid, y_valid)]

        self.logger.info("Démarrage de l'entraînement du modèle CatBoost...")
        model = CatBoostClassifier(**self.params,)
        model.fit(X_train,y_train,eval_set=eval_set)
        self.logger.info("Entraînement CatBoost terminé.")

        return model

    def predict(self, model, X: pd.DataFrame):
        return model.predict_proba(X)[:, 1]
