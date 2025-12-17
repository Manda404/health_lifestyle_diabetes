# src/health_lifestyle_diabetes/infrastructure/ml/model_trainers/catboost_trainer.py

from typing import Any, Dict, Optional, List

from catboost import CatBoostClassifier
from pandas import DataFrame, Series

from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.infrastructure.logging.loguru_logger_adapter import (
    LoguruLoggerAdapter,
)


class CatBoostTrainer(ModelTrainerPort):
    """
    Implémentation infrastructure du port ModelTrainerPort dédiée à l'entraînement
    d'un modèle CatBoostClassifier.

    Cette classe encapsule :
    - la validation robuste des données d'entrée (train / validation),
    - la détection automatique des variables catégorielles,
    - la configuration et l'entraînement conditionnel du modèle CatBoost,
    - la journalisation des étapes clés de l'entraînement.

    Elle supporte aussi bien un entraînement simple (train uniquement)
    qu'un entraînement avec jeu de validation et sélection du meilleur modèle.
    """

    def __init__(self, params: Dict[str, Any]):
        """
        Initialise le trainer CatBoost.

        Paramètres
        ----------
        params : dict
            Dictionnaire de paramètres CatBoost (learning_rate, depth,
            iterations, loss_function, etc.).
        """
        self.params = params
        self.logger = LoguruLoggerAdapter("boost.catboost")

    def train(
        self,
        X_train: Optional[DataFrame],
        y_train: Optional[Series],
        X_valid: Optional[DataFrame] = None,
        y_valid: Optional[Series] = None,
    ) -> CatBoostClassifier:
        """
        Entraîne un modèle CatBoostClassifier à partir des données fournies.

        La méthode :
        - valide la cohérence et la non-nullité des données d'entraînement,
        - vérifie que les jeux de validation sont fournis de manière cohérente,
        - détecte automatiquement les variables catégorielles si elles ne sont
          pas explicitement définies dans les paramètres du modèle,
        - entraîne le modèle avec ou sans jeu de validation,
        - active la sélection du meilleur modèle lorsque la validation est présente.

        Paramètres
        ----------
        X_train : DataFrame
            Jeu de données d'entraînement contenant les features.
        y_train : Series
            Variable cible associée au jeu d'entraînement.
        X_valid : DataFrame, optionnel
            Jeu de données de validation contenant les features.
            Doit être fourni conjointement avec `y_valid`.
        y_valid : Series, optionnel
            Variable cible associée au jeu de validation.
            Doit être fourni conjointement avec `X_valid`.

        Retours
        -------
        CatBoostClassifier
            Modèle CatBoost entraîné, prêt à être utilisé pour l'inférence
            ou l'évaluation.

        Exceptions
        ----------
        ValueError
            Levée si les données sont nulles, vides ou incohérentes
            (tailles incompatibles, validation partielle, etc.).
        """

        # =========================
        # Validation des entrées
        # =========================
        if X_train is None or y_train is None:
            raise ValueError("X_train et y_train ne peuvent pas être None.")

        if X_train.empty or y_train.empty:
            raise ValueError("X_train ou y_train est vide.")

        if len(X_train) != len(y_train):
            raise ValueError("X_train et y_train doivent avoir la même taille.")

        if (X_valid is None) ^ (y_valid is None):
            raise ValueError(
                "X_valid et y_valid doivent être fournis ensemble ou être tous les deux None."
            )

        if X_valid is not None:
            if X_valid.empty or y_valid.empty:
                raise ValueError("X_valid ou y_valid est vide.")

            if len(X_valid) != len(y_valid):
                raise ValueError("X_valid et y_valid doivent avoir la même taille.")

        # =========================
        # Logging sécurisé
        # =========================
        self.logger.info(
            "Entraînement CatBoost | "
            f"train_shape={X_train.shape} | "
            f"valid_shape={X_valid.shape if X_valid is not None else 'N/A'}"
        )

        # =========================
        # Préparation des paramètres
        # =========================
        params = dict(self.params)  # évite les effets de bord

        cat_features: List[str] = (
            X_train.select_dtypes(exclude="number").columns.tolist()
        )

        if cat_features and "cat_features" not in params:
            self.logger.info(
                f"Détection automatique des variables catégorielles : {cat_features}"
            )
            params["cat_features"] = cat_features

        model = CatBoostClassifier(**params)

        # =========================
        # Entraînement
        # =========================
        self.logger.info("Démarrage de l'entraînement CatBoost.")

        fit_kwargs = {
            "X": X_train,
            "y": y_train,
        }

        if X_valid is not None:
            fit_kwargs.update(
                {
                    "eval_set": [(X_valid, y_valid)],
                    "use_best_model": True,
                }
            )

        model.fit(**fit_kwargs)

        self.logger.info("Entraînement CatBoost terminé.")

        return model
