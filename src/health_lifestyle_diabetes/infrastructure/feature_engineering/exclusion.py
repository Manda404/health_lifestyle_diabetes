from pandas import DataFrame
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


# ------------------------------------------------------------------
# Colonnes à exclure (data leakage)
# ------------------------------------------------------------------
LEAKAGE_COLUMNS = {
    "diabetes_stage",
    "diabetes_risk_score",
    #"diagnosed_diabetes",
}


def drop_leakage_columns(df: DataFrame, logger: LoggerPort) -> DataFrame:
    """
    Supprime les colonnes induisant un data leakage.

    Objectif :
    ----------
    Éliminer toute information qui :
    - encode directement la cible
    - résume ou prédit implicitement le diagnostic

    Colonnes exclues :
    ------------------
    - diabetes_stage
    - diabetes_risk_score
    - diagnosed_diabetes (target)

    Pertinence ML :
    ---------------
    Garantit l'intégrité de l'entraînement et
    la validité des performances du modèle.
    """
    logger.info("Vérification des colonnes à risque de data leakage...")
    present_columns = [c for c in LEAKAGE_COLUMNS if c in df.columns]

    if present_columns:
        logger.info(
            f"Suppression des colonnes à risque de leakage : {present_columns}"
        )
    else:
        logger.info("Aucune colonne de leakage détectée.")

    return df.drop(columns=present_columns)
