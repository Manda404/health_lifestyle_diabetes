import pandas as pd
from pandas import DataFrame
from typing import List, Tuple
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

logger_summary = get_logger("eda.dataset_summary")
logger_features = get_logger("eda.feature_identifier")


def summarize_dataset(df: DataFrame, max_examples: int = 5) -> DataFrame:
    """
    Fournit un résumé structuré du dataset :
    - dtype
    - nombre et % de valeurs manquantes
    - cardinalité
    - échantillon de valeurs

    Le but est d’obtenir une vue claire du dataset sans calculs coûteux.
    """
    if df is None or df.empty:
        logger_summary.warning("Dataset vide ou non fourni.")
        return pd.DataFrame(
            columns=[
                "Column",
                "Type",
                "Missing",
                "% Missing",
                "Cardinality",
                "Examples",
            ]
        )

    logger_summary.info(
        f"Résumé du dataset : {df.shape[0]} lignes, {df.shape[1]} colonnes."
    )

    total_rows = len(df)
    rows = []

    # dtypes précalculés (accès O(1))
    dtypes = df.dtypes.to_dict()

    for col in df.columns:
        series = df[col]
        col_type = dtypes[col]

        missing = series.isna().sum()
        missing_pct = round((missing / total_rows) * 100, 2)
        cardinality = series.nunique(dropna=True)

        # valeurs uniques limitées
        examples = series.dropna().unique()[:max_examples]

        rows.append(
            [col, col_type, missing, missing_pct, cardinality, examples.tolist()]
        )

    summary_df = pd.DataFrame(
        rows,
        columns=["Column", "Type", "Missing", "% Missing", "Cardinality", "Examples"],
    ).sort_values(by="Missing", ascending=False)

    logger_summary.info("Résumé généré avec succès.")
    return summary_df


def identify_feature_types(df: DataFrame) -> Tuple[List[str], List[str]]:
    """
    Identifie rapidement les colonnes numériques et catégorielles.
    """
    if df is None or df.empty:
        logger_features.warning("Dataset vide.")
        return [], []

    numeric_cols = df.select_dtypes(
        include=["int", "float", "int64", "float64"]
    ).columns.tolist()
    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    logger_features.info(
        f"Types identifiés : {len(numeric_cols)} numériques, {len(categorical_cols)} catégorielles."
    )

    return numeric_cols, categorical_cols
