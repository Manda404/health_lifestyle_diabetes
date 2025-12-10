"""
Module d’analyse exploratoire des variables catégorielles.

Fonctionnalités :
- Analyse de la distribution proportionnelle d’une variable catégorielle.
- Analyse de la distribution de la cible à l'intérieur des catégories.
- Visualisation de la distribution globale de la cible (bar + pie).
- Calcul et visualisation de la distribution cumulée.

Auteur : HealthLifestyleData Project
"""

import pandas as pd
import plotly.express as px
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from plotly.subplots import make_subplots

# ===========================================================
# Logger unique pour ce module
# ===========================================================
logger = get_logger("eda.categorical")


# ===========================================================
# Helpers
# ===========================================================
def _ensure_column_exists(df: pd.DataFrame, col: str) -> None:
    """Vérifie qu'une colonne existe dans le DataFrame."""
    if df is None or df.empty:
        raise ValueError("Le DataFrame fourni est vide ou None.")
    if col not in df.columns:
        raise ValueError(f"Colonne '{col}' introuvable dans le DataFrame.")


# ===========================================================
# 1. Répartition proportionnelle d’une variable catégorielle
# ===========================================================
def plot_categorical_proportions(
    df: pd.DataFrame,
    column: str,
    show: bool = True,
):
    """
    Analyse et visualise la répartition proportionnelle d'une variable catégorielle.
    """
    _ensure_column_exists(df, column)

    logger.info(f"Analyse de la répartition proportionnelle de '{column}'.")

    counts = df[column].value_counts(normalize=True, dropna=False)
    prop = (
        pd.DataFrame(
            {
                column: counts.index.astype(str),
                "proportion": (counts.values * 100).round(2),
            }
        )
        .sort_values("proportion", ascending=False)
        .reset_index(drop=True)
    )

    fig = px.bar(
        prop,
        x=column,
        y="proportion",
        text="proportion",
        color=column,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Distribution proportionnelle de '{column}' (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(yaxis_title="Proportion (%)", showlegend=False)

    if show:
        fig.show()

    return fig, prop


# ===========================================================
# 2. Répartition de la cible à l'intérieur de chaque catégorie
# ===========================================================
def plot_target_distribution_within_category(
    df: pd.DataFrame,
    cat_col: str,
    target_col: str,
    show: bool = True,
):
    """
    Visualise la répartition de la cible pour chaque catégorie
    (un graphique par catégorie via facet plot).
    """
    _ensure_column_exists(df, cat_col)
    _ensure_column_exists(df, target_col)

    logger.info(f"Analyse '{cat_col}' → '{target_col}' par catégories (facettes).")

    # Comptage + pourcentage local par catégorie
    crosstab = df.groupby([cat_col, target_col]).size().rename("count").reset_index()
    crosstab["proportion"] = crosstab.groupby(cat_col)["count"].transform(
        lambda x: (x / x.sum() * 100).round(2)
    )

    fig = px.bar(
        crosstab,
        x=target_col,
        y="proportion",
        color=target_col,
        text="proportion",
        facet_col=cat_col,
        facet_col_wrap=4,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Distribution de '{target_col}' par catégorie de '{cat_col}' (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        yaxis_title="Proportion (%)",
        xaxis_title="Valeur du target",
        showlegend=False,
    )

    if show:
        fig.show()

    return fig, crosstab


# ===========================================================
# 3. Distribution globale de la cible (bar + pie synchronisés)
# ===========================================================
def plot_target_distribution(
    df: pd.DataFrame,
    target_col: str,
    show: bool = True,
):
    """
    Visualise la distribution globale de la cible :
    - Diagramme en barres
    - Diagramme en secteurs

    Les deux plots partagent la même palette de couleurs pour cohérence.
    """
    _ensure_column_exists(df, target_col)

    logger.info(f"Distribution globale de la cible '{target_col}'.")

    counts = df[target_col].value_counts(dropna=False)
    percent = (counts / len(df) * 100).round(2)

    summary = pd.DataFrame(
        {
            "category": counts.index.astype(str),
            "count": counts.values,
            "percent": percent.values,
        }
    )

    categories = summary["category"].unique()
    palette = px.colors.qualitative.Plotly
    color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(categories)}

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "domain"}]],
        subplot_titles=["Répartition brute", "Répartition proportionnelle"],
    )

    # Bar chart
    bar = px.bar(
        summary,
        x="category",
        y="count",
        text="percent",
        color="category",
        color_discrete_map=color_map,
    )
    for trace in bar.data:
        fig.add_trace(trace, row=1, col=1)

    # Pie chart
    pie = px.pie(
        summary,
        names="category",
        values="count",
        color="category",
        color_discrete_map=color_map,
    )
    for trace in pie.data:
        fig.add_trace(trace, row=1, col=2)

    fig.update_traces(texttemplate="%{text:.2f}%", row=1, col=1)
    fig.update_layout(title=f"Distribution de '{target_col}'", showlegend=True)

    if show:
        fig.show()

    return fig, summary


# ===========================================================
# 4. Distribution cumulée d'une variable catégorielle
# ===========================================================
def plot_cumulative_distribution(
    df: pd.DataFrame,
    col: str,
    show: bool = True,
):
    """
    Calcule et visualise la fréquence cumulée d'une variable catégorielle.
    """
    _ensure_column_exists(df, col)

    logger.info(f"Distribution cumulée de '{col}'.")

    counts = df[col].value_counts(dropna=False)
    percent = (counts / len(df) * 100).round(2)

    summary = (
        pd.DataFrame(
            {
                "category": counts.index.astype(str),
                "count": counts.values,
                "percent": percent,
            }
        )
        .sort_values("count")
        .reset_index(drop=True)
    )
    summary["cumulative_percent"] = summary["percent"].cumsum()

    fig = px.line(
        summary,
        x="category",
        y="cumulative_percent",
        markers=True,
        title=f"Fréquence cumulée de '{col}'",
    )

    if show:
        fig.show()

    return fig, summary
