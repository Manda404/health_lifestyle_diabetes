# src/health_lifestyle_diabetes/application/use_cases/train_model_uc.py

from __future__ import annotations

from typing import Any, Optional

from health_lifestyle_diabetes.domain.ports.dataset_repository_port import (
    DatasetRepositoryPort,
)
from health_lifestyle_diabetes.domain.ports.dataset_splitter_port import (
    DatasetSplitterPort,
)
from health_lifestyle_diabetes.domain.ports.feature_engineering_port import (
    FeatureEngineeringPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.model_repository_port import (
    ModelRepositoryPort,
)
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort


class TrainModelUseCase:
    """
    Use case responsable de l'orchestration complète de l'entraînement d'un modèle ML.

    Responsabilités :
    -----------------
    - charger les données brutes,
    - appliquer le feature engineering,
    - diviser les données (train / validation),
    - entraîner le modèle via un ModelTrainerPort,
    - sauvegarder le modèle entraîné,
    - journaliser toutes les étapes.

    Clean Architecture :
    --------------------
    - aucune dépendance vers Pandas, Sklearn, CatBoost, XGBoost,
    - aucune logique métier ou ML technique,
    - dépend uniquement des ports du domaine.
    """

    def __init__(
        self,
        dataset_repo: DatasetRepositoryPort,
        feature_engineer: FeatureEngineeringPort,
        model_trainer: ModelTrainerPort,
        model_repo: ModelRepositoryPort,
        logger: LoggerPort,
        dataset_splitter: Optional[DatasetSplitterPort] = None,
    ):
        self.dataset_repo = dataset_repo
        self.feature_engineer = feature_engineer
        self.model_trainer = model_trainer
        self.model_repo = model_repo
        self.logger = logger
        self.dataset_splitter = dataset_splitter

    def execute(
        self,
        *,
        target_column: str,
        model_name: str,
        train_size: float = 0.8,
        random_state: int = 42,
        save_model: bool = True,
    ) -> Any:
        """
        Lance l'entraînement du modèle.

        Parameters
        ----------
        target_column : str
            Nom de la colonne cible.
        model_name : str
            Nom logique du modèle (utilisé pour la sauvegarde).
        train_size : float
            Proportion du dataset utilisée pour l'entraînement.
        random_state : int
            Graine pour la reproductibilité.
        save_model : bool
            Sauvegarder ou non le modèle entraîné.

        Returns
        -------
        Any
            Modèle entraîné (type concret dépend de l'infrastructure).
        """

        self.logger.info("=== DÉMARRAGE DU TRAINING ===")

        # --------------------------------------------------
        # 1. Chargement du dataset brut
        # --------------------------------------------------
        self.logger.info("Chargement des données brutes.")
        raw_dataset = self.dataset_repo.load_dataset()

        # --------------------------------------------------
        # 2. Feature Engineering
        # --------------------------------------------------
        self.logger.info("Application du feature engineering.")
        processed_dataset = self.feature_engineer.transform(raw_dataset)

        # --------------------------------------------------
        # 3. Séparation X / y
        # --------------------------------------------------
        self.logger.info("Séparation des features et de la cible.")
        X = processed_dataset.drop(columns=[target_column])
        y = processed_dataset[target_column]

        # --------------------------------------------------
        # 4. Split train / validation (optionnel)
        # --------------------------------------------------
        if self.dataset_splitter is not None:
            self.logger.info("Split train / validation.")
            X_train, X_valid = self.dataset_splitter.split(
                dataset=X,
                train_size=train_size,
                target_column=None,  # pas de stratification ici
                random_state=random_state,
            )
            y_train, y_valid = self.dataset_splitter.split(
                dataset=y,
                train_size=train_size,
                target_column=None,
                random_state=random_state,
            )
        else:
            self.logger.warning(
                "Aucun splitter fourni → entraînement sur dataset complet."
            )
            X_train, y_train = X, y
            X_valid, y_valid = None, None

        # --------------------------------------------------
        # 5. Entraînement du modèle
        # --------------------------------------------------
        self.logger.info("Lancement de l'entraînement du modèle.")
        model = self.model_trainer.train(
            X_train=X_train,
            y_train=y_train,
            X_valid=X_valid,
            y_valid=y_valid,
        )

        # --------------------------------------------------
        # 6. Sauvegarde du modèle
        # --------------------------------------------------
        if save_model:
            self.logger.info("Sauvegarde du modèle entraîné.")
            self.model_repo.save(model, model_name)

        self.logger.info("=== FIN DU TRAINING ===")

        return model
