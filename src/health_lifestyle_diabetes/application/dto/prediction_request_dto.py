# src/health_lifestyle_diabetes/application/dto/prediction_request_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRequestDTO:
    """
    DTO représentant une requête de prédiction envoyée par un utilisateur.

    Ce DTO encapsule les données brutes provenant de l'extérieur (API, UI, CLI)
    dans un format stable et typé, indépendant de toute technologie.

    Règles Clean Architecture :
    ---------------------------
    - aucune logique métier,
    - aucune dépendance à Pandas / Sklearn,
    - utilisé uniquement par la couche application.
    """

    """
    DTO représentant la requête de prédiction patient.

    Ce DTO encapsule strictement les données reçues depuis
    l'extérieur (API, batch, UI) dans un format stable et typé.
    Aucune logique métier n'est autorisée ici.
    """

    # --- Démographie ---
    age: int
    gender: str
    ethnicity: str
    education_level: str
    employment_status: str
    income_level: str

    # --- Mode de vie ---
    smoking_status: str
    alcohol_consumption_per_week: int
    physical_activity_minutes_per_week: int
    diet_score: float
    sleep_hours_per_day: float
    screen_time_hours_per_day: float

    # --- Antécédents médicaux ---
    family_history_diabetes: int
    hypertension_history: int
    cardiovascular_history: int

    # --- Mesures corporelles ---
    bmi: float
    waist_to_hip_ratio: float

    # --- Signes vitaux ---
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int

    # --- Profil lipidique ---
    cholesterol_total: int
    ldl_cholesterol: int
    hdl_cholesterol: int
    triglycerides: int

    # --- Glycémie & diabète ---
    glucose_fasting: int
    glucose_postprandial: int
    hba1c: float
    insulin_level: float
    diabetes_risk_score: float
    diabetes_stage: str

    # --- Variable observée (si présente côté API) ---
    diagnosed_diabetes: int