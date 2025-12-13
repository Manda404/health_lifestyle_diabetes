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

    age: int
    gender: str
    ethnicity: str
    education_level: str
    income_level: str
    employment_status: str
    smoking_status: str

    alcohol_consumption_per_week: int
    physical_activity_minutes_per_week: int
    diet_score: float
    sleep_hours_per_day: float
    screen_time_hours_per_day: float

    family_history_diabetes: int
    hypertension_history: int
    cardiovascular_history: int

    bmi: float
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int

    cholesterol_total: int
    hdl_cholesterol: int
    ldl_cholesterol: int
    triglycerides: int

    glucose_fasting: int
    glucose_postprandial: int
    insulin_level: float
    hba1c: float

    waist_to_hip_ratio: float
