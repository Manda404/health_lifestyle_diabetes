"""
Définition du schéma de features attendu pour un dataset patient.

Objectifs :
-----------
- Décrire la structure obligatoire d'un dataset (colonnes + types attendus),
- Fournir un contrat unique utilisé pour valider les données,
- Rester indépendant de toute technologie (aucun DataFrame ici).

Différence avec PatientProfile :
--------------------------------
- PatientProfile = un patient réel (instance)
- FeatureSchema = un contrat structurel (types par colonne)
"""

from dataclasses import dataclass
from typing import Dict, Type


@dataclass(frozen=True)
class FeatureSchema:
    """
    Schéma des features attendu par le système.

    `expected_types` mappe le nom de colonne vers le type Python attendu.
    """

    expected_types: Dict[str, Type]


FEATURE_SCHEMA = FeatureSchema(
    expected_types={
        # Démographie
        "Age": int,
        "gender": str,
        "ethnicity": str,
        "education_level": str,
        "income_level": str,
        "employment_status": str,
        "smoking_status": str,
        # Mode de vie
        "alcohol_consumption_per_week": int,
        "physical_activity_minutes_per_week": int,
        "diet_score": float,
        "sleep_hours_per_day": float,
        "screen_time_hours_per_day": float,
        # Antécédents médicaux
        "family_history_diabetes": int,
        "hypertension_history": int,
        "cardiovascular_history": int,
        # Mesures physiques
        "bmi": float,
        "waist_to_hip_ratio": float,
        # Tension/artères et rythme
        "systolic_bp": int,
        "diastolic_bp": int,
        "heart_rate": int,
        # Lipides
        "cholesterol_total": int,
        "hdl_cholesterol": int,
        "ldl_cholesterol": int,
        "triglycerides": int,
        # Glycémie / insuline
        "glucose_fasting": int,
        "glucose_postprandial": int,
        "insulin_level": float,
        "hba1c": float,
        # Score clinique
        "diabetes_risk_score": float,
        "diabetes_stage": str,
        # Cible (présente uniquement dans les datasets d'entraînement / éval)
        "diagnosed_diabetes": int,
    }
)
