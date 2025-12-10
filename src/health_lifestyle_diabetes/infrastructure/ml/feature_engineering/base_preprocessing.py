from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import DataFrame

logger = get_logger("fe.base_preprocessing")


def clean_categorical_variables(df: DataFrame) -> DataFrame:
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
