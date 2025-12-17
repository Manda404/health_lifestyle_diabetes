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
from src.health_lifestyle_diabetes.infrastructure.services.experiment_tracking_service import (
    ExperimentTrackingService,
)


class TrainModelUseCase:
    """
    Use case responsable de l'orchestration complète de l'entraînement d'un modèle ML.

    Clean Architecture :
    --------------------
    - aucune dépendance vers MLflow, sklearn, pandas
    - tracking géré via un service applicatif
    """

    def __init__(
        self,
        dataset_repo: DatasetRepositoryPort,
        feature_engineer: FeatureEngineeringPort,
        model_trainer: ModelTrainerPort,
        model_repo: ModelRepositoryPort,
        logger: LoggerPort,
        tracking: ExperimentTrackingService,
        dataset_splitter: Optional[DatasetSplitterPort] = None,
    ):
        self.dataset_repo = dataset_repo
        self.feature_engineer = feature_engineer
        self.model_trainer = model_trainer
        self.model_repo = model_repo
        self.logger = logger
        self.tracking = tracking
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

        self.logger.info("=== DÉMARRAGE DU TRAINING ===")

        # 0. Démarrage tracking
        self.tracking.start_experiment(
            experiment_name="health_lifestyle_diabetes",
            run_name=f"train_{model_name}",
        )

        # --------------------------------------------------
        # 1. Chargement du dataset brut
        # --------------------------------------------------
        self.logger.info("Chargement des données brutes.")
        raw_dataset = self.dataset_repo.load_dataset()

        self.tracking.log_training_context(
            model_name=model_name,
            params={
                "train_size": train_size,
                "random_state": random_state,
            },
        )

        # --------------------------------------------------
        # 2. Feature Engineering
        # --------------------------------------------------
        self.logger.info("Application du feature engineering.")
        processed_dataset = self.feature_engineer.transform(raw_dataset)

        # --------------------------------------------------
        # 3. Séparation X / y
        # --------------------------------------------------
        X = processed_dataset.drop(columns=[target_column])
        y = processed_dataset[target_column]

        # --------------------------------------------------
        # 4. Split train / validation
        # --------------------------------------------------
        if self.dataset_splitter is not None:
            X_train, X_valid = self.dataset_splitter.split(
                dataset=X,
                train_size=train_size,
                random_state=random_state,
            )
            y_train, y_valid = self.dataset_splitter.split(
                dataset=y,
                train_size=train_size,
                random_state=random_state,
            )
        else:
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
            self.model_repo.save(model, model_name)
            self.tracking.log_artifact(
                path=self.model_repo.get_model_path(model_name)
            )

        # 7. Fermeture tracking
        self.tracking.log_evaluation(
            {
                "n_train": len(X_train),
                "n_features": X_train.shape[1],
            }
        )
        self.tracking.close()

        self.logger.info("=== FIN DU TRAINING ===")

        return model
