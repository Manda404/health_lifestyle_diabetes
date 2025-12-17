# src/health_lifestyle_diabetes/presentation/api/schemas/prediction_input.py

from pydantic import BaseModel, Field
from typing import Literal
from health_lifestyle_diabetes.application.dto.prediction_request import PredictionRequestDTO


class PredictionInput(BaseModel):
    """
    Schéma d'entrée de l'API /predict.

    Ce modèle définit toutes les variables nécessaires à la prédiction
    et valide strictement les types + les valeurs possibles.
    Il représente la structure attendue par l'API :
    - données démographiques
    - données lifestyle
    - historique médical
    - mesures cliniques

    Ce schéma garantit :
    - une API stable (contrat entre client et backend)
    - la validation automatique des entrées
    - une conversion propre vers le DTO métier utilisé dans les use cases
    """

    # ------------------------------
    #         DÉMOGRAPHIE
    # ------------------------------
    age: int = Field(..., ge=0, le=120)
    gender: Literal["Male", "Female", "Other"]
    ethnicity: Literal["Asian", "White", "Hispanic", "Black", "Other"]
    education_level: Literal["Highschool", "Graduate", "Postgraduate", "No formal"]
    income_level: Literal["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
    employment_status: Literal["Employed", "Unemployed", "Retired", "Student"]

    # ------------------------------
    #       LIFESTYLE
    # ------------------------------
    smoking_status: Literal["Never", "Former", "Current"]
    alcohol_consumption_per_week: int = Field(..., ge=0)
    physical_activity_minutes_per_week: int = Field(..., ge=0)
    diet_score: float = Field(..., ge=0, le=10)
    sleep_hours_per_day: float = Field(..., ge=0, le=24)
    screen_time_hours_per_day: float = Field(..., ge=0, le=24)

    # ------------------------------
    #      HISTORIQUE MÉDICAL
    # ------------------------------
    family_history_diabetes: int = Field(..., ge=0, le=1)
    hypertension_history: int = Field(..., ge=0, le=1)
    cardiovascular_history: int = Field(..., ge=0, le=1)

    # ------------------------------
    #     MESURES CLINIQUES
    # ------------------------------
    bmi: float = Field(..., ge=5, le=80)
    waist_to_hip_ratio: float = Field(..., ge=0.4, le=2.0)
    systolic_bp: int = Field(..., ge=50, le=250)
    diastolic_bp: int = Field(..., ge=30, le=150)
    heart_rate: int = Field(..., ge=20, le=250)
    cholesterol_total: int = Field(..., ge=50, le=400)
    hdl_cholesterol: int = Field(..., ge=10, le=150)
    ldl_cholesterol: int = Field(..., ge=10, le=300)
    triglycerides: int = Field(..., ge=20, le=2000)
    glucose_fasting: int = Field(..., ge=40, le=400)
    glucose_postprandial: int = Field(..., ge=40, le=600)
    insulin_level: float = Field(..., ge=0)
    hba1c: float = Field(..., ge=2, le=20)
    # diabetes_risk_score: float = Field(..., ge=0, le=100)

    # ------------------------------
    #   MÉTHODE DE CONVERSION DTO
    # ------------------------------
    def to_dto(self) -> PredictionRequestDTO:
        """
        Convertit l'input API en DTO destiné aux use cases.

        Pourquoi ?
        - L'API ne doit jamais manipuler la logique métier.
        - Le DTO est une structure interne aux use cases.
        - Cette méthode garantit une séparation nette API/domain.

        Retour :
            PredictionRequestDTO : objet interne utilisé par le use case Prediction
        """
        return PredictionRequestDTO(**self.dict())