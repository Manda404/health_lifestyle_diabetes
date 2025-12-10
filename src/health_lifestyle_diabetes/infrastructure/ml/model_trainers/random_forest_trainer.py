import pandas as pd
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from sklearn.ensemble import RandomForestClassifier


class RandomForestTrainer(ModelTrainerPort):

    def __init__(self, params: dict):
        self.params = params

    def train(self, X: pd.DataFrame, y: pd.Series):
        model = RandomForestClassifier(**self.params)
        model.fit(X, y)
        return model

    def predict(self, model, X: pd.DataFrame):
        return model.predict_proba(X)[:, 1]
