from typing import List, Tuple

from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import DataFrame

# ===========================================================
# Logger unique pour le module dataset_summary
# ===========================================================
logger = get_logger("eda.dataset")


# ===========================================================
# Résumé général du dataset
# ===========================================================
def summarize_dataset(df: DataFrame, max_examples: int = 5) -> DataFrame:
    """
    Produit un résumé structuré du dataset :
    - type de chaque colonne
    - nombre et pourcentage de valeurs manquantes
    - cardinalité
    - exemples de valeurs

    Utile pour obtenir une vue claire du dataset sans calculs coûteux.
    """
    if df is None or df.empty:
        logger.warning("Dataset vide ou non fourni.")
        return DataFrame(
            columns=[
                "Column",
                "Type",
                "Missing",
                "% Missing",
                "Cardinality",
                "Examples",
            ]
        )

    logger.info(f"Résumé du dataset : {df.shape[0]} lignes, {df.shape[1]} colonnes.")
    total_rows = len(df)

    rows = []
    dtypes = df.dtypes.to_dict()  # accès plus rapide dans la boucle

    for col in df.columns:
        series = df[col]
        missing = series.isna().sum()
        missing_pct = round((missing / total_rows) * 100, 2)
        cardinality = series.nunique(dropna=True)

        # Exemple de valeurs (liste lisible)
        examples = (
            series.dropna().unique()[:max_examples].tolist()
            if not series.dropna().empty
            else []
        )

        rows.append(
            [
                col,
                dtypes[col],
                missing,
                missing_pct,
                cardinality,
                examples,
            ]
        )

    summary_df = DataFrame(
        rows,
        columns=["Column", "Type", "Missing", "% Missing", "Cardinality", "Examples"],
    ).sort_values(by="Missing", ascending=False)

    logger.info("Résumé généré avec succès.")
    return summary_df


# ===========================================================
# Identification des colonnes numériques et catégorielles
# ===========================================================
def identify_feature_types(df: DataFrame) -> Tuple[List[str], List[str]]:
    """
    Identifie rapidement les colonnes numériques et catégorielles.

    La logique est volontairement simple :
    - numériques : tout type numérique (entiers, floats, extension pandas)
    - catégorielles : strings, category, boolean
    """
    if df is None or df.empty:
        logger.warning("Dataset vide.")
        return [], []

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool", "string"]
    ).columns.tolist()

    logger.info(
        f"Types identifiés : {len(numeric_cols)} colonnes numériques, "
        f"{len(categorical_cols)} colonnes catégorielles."
    )

    return numeric_cols, categorical_cols
