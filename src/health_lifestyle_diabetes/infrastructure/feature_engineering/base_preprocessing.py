# src/health_lifestyle_diabetes/infrastructure/ml/feature_engineering/base_preprocessing.py
from pandas import DataFrame
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


def clean_categorical_variables(df: DataFrame, logger: LoggerPort) -> DataFrame:
    """
    Nettoie et harmonise les libellés des variables catégorielles.

    Objectif :
    ----------
    Corriger les incohérences textuelles et uniformiser les catégories
    avant encodage ou modélisation.

    Justification médicale :
    ------------------------
    En santé publique, la cohérence des libellés est essentielle pour éviter
    des segmentations erronées entre sous-groupes (ex. “Former” vs “Ex-Smoker”).

    Pertinence métier :
    -------------------
    Garantit la fiabilité des analyses descriptives et la robustesse des modèles
    supervisés en réduisant la variabilité sémantique.
    """
    logger.info("Nettoyage des variables catégorielles...")
    df = df.copy()
    df["gender"] = df["gender"].replace({"Other": "Unknown"})
    df["employment_status"] = df["employment_status"].replace(
        {"Retired": "Inactive", "Unemployed": "Inactive"}
    )
    df["smoking_status"] = df["smoking_status"].replace({"Former": "Ex-Smoker"})
    logger.info("Libellés uniformisés avec succès.")
    return df
