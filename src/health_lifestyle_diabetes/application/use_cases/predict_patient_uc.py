from typing import Any, Dict

from health_lifestyle_diabetes.application.dto.prediction_request_dto import (
    PredictionRequestDTO,
)
from health_lifestyle_diabetes.domain.entities.diabetes_prediction import (
    DiabetesPrediction,
)
from health_lifestyle_diabetes.domain.ports.feature_engineering_port import (
    FeatureEngineeringPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.ports.model_trainer_port import ModelTrainerPort
from health_lifestyle_diabetes.domain.services.prediction_service import (
    PredictionService,
)


class PredictPatientUseCase:
    """
    Use case responsable de la prédiction du risque de diabète pour un patient.

    Rôle :
    ------
    - recevoir une requête utilisateur sous forme de DTO,
    - préparer les données pour le modèle,
    - exécuter la prédiction,
    - transformer la sortie en résultat métier interprétable.

    Clean Architecture :
    --------------------
    - aucune dépendance à Pandas / Sklearn,
    - dépend uniquement de ports et de services métier.
    """

    def __init__(
        self,
        feature_engineer: FeatureEngineeringPort,
        model_trainer: ModelTrainerPort,
        prediction_service: PredictionService,
        logger: LoggerPort,
    ):
        self.feature_engineer = feature_engineer
        self.model_trainer = model_trainer
        self.prediction_service = prediction_service
        self.logger = logger

    def execute(self, request: PredictionRequestDTO) -> DiabetesPrediction:
        """
        Lance la prédiction pour un patient.

        Parameters
        ----------
        request : PredictionRequestDTO
            Données patient envoyées par l'utilisateur.

        Returns
        -------
        DiabetesPrediction
            Résultat métier de la prédiction.
        """

        self.logger.info("Démarrage de la prédiction patient.")

        # -------------------------------------------------
        # 1. DTO → structure tabulaire (infra-friendly)
        # -------------------------------------------------
        record: Dict[str, Any] = request.__dict__

        # -------------------------------------------------
        # 2. Feature engineering
        # -------------------------------------------------
        self.logger.info("Application du feature engineering.")
        features = self.feature_engineer.transform(record)

        # -------------------------------------------------
        # 3. Prédiction (probabilité)
        # -------------------------------------------------
        self.logger.info("Calcul de la probabilité de diabète.")
        proba = self.model_trainer.predict_proba(features)

        # -------------------------------------------------
        # 4. Logique métier de prédiction
        # -------------------------------------------------
        prediction = self.prediction_service.create_prediction(proba)

        self.logger.info("Prédiction terminée.")

        return prediction
