import pandas as pd
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from pandas import Series
from sklearn.ensemble import RandomForestClassifier


class RandomForestTrainer(ModelTrainerPort):

    def __init__(self, params: dict):
        self.params = params

    def train(self, X: pd.DataFrame, y: pd.Series):
        model = RandomForestClassifier(**self.params)
        model.fit(X, y)
        return model

    def predict_proba(self, model, X: pd.DataFrame) -> Series:
        return Series(model.predict_proba(X)[:, 1], index=X.index, name="proba")
