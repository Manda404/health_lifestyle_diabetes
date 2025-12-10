"""
Module d’analyse exploratoire des variables catégorielles.

Contient des fonctions pour :
- analyser la distribution proportionnelle d’une variable catégorielle,
- analyser automatiquement l'ensemble des colonnes catégorielles d'un DataFrame.

Auteur : HealthLifestyleData Project
"""

import pandas as pd
import plotly.express as px
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from plotly.subplots import make_subplots

logger_proportions = get_logger("eda.cat_proportions")
logger_proportions_target = get_logger("eda.cat_proportions_target")
logger_target = get_logger("eda.target_distribution")
logger_cumulative = get_logger("eda.cumulative_dist")


def plot_categorical_proportions(df: pd.DataFrame, column: str):
    """
    Analyse et visualise la répartition proportionnelle d'une variable catégorielle.

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame contenant la variable.
    column : str
        Le nom de la colonne catégorielle à analyser.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        La figure Plotly générée (bar plot proportionnel).
    """

    if column not in df.columns:
        raise ValueError(f"La colonne '{column}' est introuvable dans le DataFrame.")

    # ---- Calcul des proportions ----
    counts = df[column].value_counts(normalize=True)
    prop = pd.DataFrame(
        {column: counts.index.astype(str), "proportion": (counts.values * 100).round(2)}
    ).sort_values("proportion", ascending=False)

    logger_proportions.info(f"Proportions pour {column} (%%) :\n {prop}")

    # ---- Graphe ----
    fig = px.bar(
        prop,
        x=column,
        y="proportion",
        text="proportion",
        color=column,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Répartition proportionnelle de '{column}' (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        xaxis_title=column, yaxis_title="Proportion (%)", showlegend=False
    )
    logger_proportions.info(
        f"Visualisation de la variable catégorielle {column} terminée.\n"
    )

    return fig


def plot_target_distribution_within_category(
    df: pd.DataFrame, cat_col: str, target_col: str
):
    """
    Visualise la répartition de la target pour chaque catégorie,
    avec un bar plot séparé par catégorie (pas superposé, pas groupé).

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame contenant les données.
    cat_col : str
        La colonne catégorielle.
    target_col : str
        La colonne cible (binaire ou multi-classes).

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Figure Plotly avec bar plot proportionnel.
    """
    if cat_col not in df or target_col not in df:
        raise ValueError("Colonne introuvable.")

    logger_proportions_target.info(
        f"Analyse cat -> target avec facettes : {cat_col} → {target_col}"
    )

    # ---- Tableau croisé ----
    crosstab = df.groupby([cat_col, target_col]).size().rename("count").reset_index()

    # ---- Normalisation (%) par catégorie ----
    crosstab["proportion"] = crosstab.groupby(cat_col)["count"].transform(
        lambda x: (x / x.sum() * 100).round(2)
    )

    # ---- Plot en facettes (1 graphique par catégorie) ----
    fig = px.bar(
        crosstab,
        x=target_col,
        y="proportion",
        color=target_col,
        text="proportion",
        color_discrete_sequence=px.colors.qualitative.Set2,
        facet_col=cat_col,  # <-- Séparation des graphiques par catégorie
        facet_col_wrap=4,  # nombre max de colonnes (modulable)
        title=f"Répartition de '{target_col}' pour chaque catégorie de '{cat_col}' (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

    fig.update_layout(
        yaxis_title="Proportion (%)", xaxis_title="Valeur cible", showlegend=False
    )

    return fig


def plot_target_distribution(df: pd.DataFrame, target_col: str):
    if target_col not in df:
        raise ValueError(f"Colonne cible '{target_col}' introuvable.")

    logger_target.info(f"Distribution de la cible '{target_col}'.")

    counts = df[target_col].value_counts(dropna=False)
    percent = round(counts / len(df) * 100, 2)

    summary = pd.DataFrame(
        {
            "category": counts.index.astype(str),
            "count": counts.values,
            "percent": percent.values,
        }
    )

    # ------------------------------
    # ✔️ 1. Générer une palette cohérente
    # ------------------------------
    unique_categories = summary["category"].unique()
    base_colors = px.colors.qualitative.Plotly  # palette Plotly standard
    color_map = {
        cat: base_colors[i % len(base_colors)]
        for i, cat in enumerate(unique_categories)
    }

    # ------------------------------
    # ✔️ 2. Construire la figure
    # ------------------------------
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "domain"}]],
        subplot_titles=["Répartition brute", "Répartition proportionnelle"],
    )

    # ------------------------------
    # ✔️ 3. Bar chart (couleurs synchronisées)
    # ------------------------------
    bar = px.bar(
        summary,
        x="category",
        y="count",
        text="percent",
        color="category",
        color_discrete_map=color_map,  # <- COULEURS IDENTIQUES
    )
    for trace in bar.data:
        fig.add_trace(trace, row=1, col=1)

    # ------------------------------
    # ✔️ 4. Pie chart (couleurs synchronisées)
    # ------------------------------
    pie = px.pie(
        summary,
        names="category",
        values="count",
        color="category",
        color_discrete_map=color_map,  # <- COULEURS IDENTIQUES
    )
    for trace in pie.data:
        fig.add_trace(trace, row=1, col=2)

    # ------------------------------
    # ✔️ 5. Mise en forme
    # ------------------------------
    fig.update_traces(texttemplate="%{text:.2f}%", row=1, col=1)
    fig.update_layout(title=f"Distribution de '{target_col}'", showlegend=True)

    return fig


def plot_cumulative_distribution(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df:
        raise ValueError(f"Colonne '{col}' introuvable.")

    logger_cumulative.info(f"Fréquence cumulée de '{col}'.")

    counts = df[col].value_counts(dropna=False)
    percent = round(counts / len(df) * 100, 2)

    summary = (
        pd.DataFrame(
            {"category": counts.index, "count": counts.values, "percent": percent}
        )
        .sort_values("count")
        .reset_index(drop=True)
    )
    summary["cumulative_percent"] = summary["percent"].cumsum()

    px.line(summary, x="category", y="cumulative_percent", markers=True).show()

    return summary
