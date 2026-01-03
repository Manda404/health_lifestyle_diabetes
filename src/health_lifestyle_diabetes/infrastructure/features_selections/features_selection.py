# Liste des variables numériques (en excluant la target 'diagnosed_diabetes')
"""
Liste des features utilisées pour l'entraînement / inference.
Importable depuis n'importe quel script du projet.
"""

NUMERICAL_FEATURES = [
    "Age",
    "age_squared",
    "HOMA_IR",
    "hdl_to_ldl_ratio",
    "cholesterol_ratio",
    "bmi_glucose_interaction",
    "glucose_diff",
    "glycemic_load",
    "bp_ratio",
    "activity_adequacy_ratio",
    "screen_sleep_ratio",
    "bmi",
    "waist_to_hip_ratio",
    "alcohol_consumption_per_week",
    "physical_activity_minutes_per_week",
    "diet_score",
    "sleep_hours_per_day",
    "screen_time_hours_per_day",
    "hba1c",
    "insulin_level",
    "glucose_postprandial",
    "glucose_fasting",
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    "cholesterol_total",
    "hdl_cholesterol",
    "ldl_cholesterol",
    "triglycerides",
    "lifestyle_score",
    "sleep_efficiency",
    "cardiometabolic_burden_score",
]

# Liste des variables catégorielles (en excluant 'member_id' qui est un identifiant)
CATEGORICAL_FEATURES = [
    "gender",
    "ethnicity",
    "education_level",
    "income_level",
    "employment_status",
    "smoking_status",
    "age_group",
    "glucose_status",
    "hba1c_category",
    "bmi_category",
    "bp_category",
]

# Flags binaires → catégoriels pour modèles CatBoost/XGBoost
CATEGORICAL_FEATURES += [
    "socioeconomic_vulnerability_flag",
    "insulin_resistance_flag",
    "metabolic_syndrome_flag",
    "dyslipidemia_flag",
    "sedentary_risk_flag",
    "family_history_diabetes",
    "hypertension_history",
    "cardiovascular_history",
]

# Colonnes à exclure lors de l'entraînement
ID_COLUMN = "user_id"  # identifiant (corrigé)
TARGET_COLUMN = "diagnosed_diabetes"  # cible

# Liste des features ALL
FEATURES_ALL = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# Liste des features sélectionnées (top features)
SELECTED_FEATURES = [
    "hba1c",
    "glucose_fasting",
    "glucose_status",
    "family_history_diabetes",
    "physical_activity_minutes_per_week",
    ]
