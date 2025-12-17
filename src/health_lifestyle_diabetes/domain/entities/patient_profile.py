# src/health_lifestyle_diabetes/domain/entities/patient_profile.py
"""
1. Représentation métier d'un patient au sein du système.

Cette entité est un **objet métier pur** :
- elle ne dépend d'aucune technologie (Pandas, NumPy, Sklearn…)
- elle représente un patient tel qu'il apparaît dans le dataset
- elle sert d'entrée aux use cases de prédiction, d'analyse et de profilage
- elle est immuable (frozen=True)

Elle **ne contient aucune règle de calcul**, aucun ML, aucune logique EDA.

Elle correspond exactement aux colonnes décrivant un patient
dans ton dataset d’entraînement.

2. Représentation métier d'un patient dans le système de prédiction de diabète.

Cette entité est :
- totalement indépendante des technologies (pas de Pandas, Sklearn, etc.),
- alignée sur les colonnes de ton dataset,
- utilisée comme support pour les use cases de prédiction, profilage, audit.

Elle ne contient **aucune logique ML**, uniquement des données.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PatientProfile:
    """
    Profil complet d'un patient.

    Contient l'ensemble des variables démographiques, cliniques,
    biologiques et comportementales décrivant un patient. (Représentation métier d’un patient réel.)

    Important :
    - La variable cible `diagnosed_diabetes` est volontairement absente,
      car une entité métier ne doit pas contenir la vérité terrain d'entraînement.

    À utiliser dans :
    - l'API de prédiction
    - les use cases de prédiction
    - les contrôles métier (âge, biomarqueurs, plausibilité clinique)

    Remarque :
    ----------
    La variable cible `diagnosed_diabetes` n'apparaît pas ici,
    car cette entité représente un patient à prédire, pas une ligne d'entraînement.
    """

    # Démographie
    Age: int
    gender: str
    ethnicity: str
    education_level: str
    income_level: str
    employment_status: str
    smoking_status: str

    # Mode de vie
    alcohol_consumption_per_week: int
    physical_activity_minutes_per_week: int
    diet_score: float
    sleep_hours_per_day: float
    screen_time_hours_per_day: float

    # Antécédents médicaux
    family_history_diabetes: int
    hypertension_history: int
    cardiovascular_history: int

    # Mesures physiques
    bmi: float
    waist_to_hip_ratio: float

    # Tension/artère et rythme
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int

    # Lipides
    cholesterol_total: int
    hdl_cholesterol: int
    ldl_cholesterol: int
    triglycerides: int

    # Glycémie / insuline
    glucose_fasting: int
    glucose_postprandial: int
    insulin_level: float
    hba1c: float

    # Score et stade
    # diabetes_risk_score: float
    # diabetes_stage: str
