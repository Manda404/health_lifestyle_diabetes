import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger
from pandas import DataFrame
from plotly.subplots import make_subplots
from scipy.stats import norm

# ===========================================================
# Logger unique pour tout le module EDA
# ===========================================================
logger = get_logger("eda")


# ===========================================================
# Helpers internes
# ===========================================================
def _ensure_columns(df: DataFrame, columns: list) -> None:
    """Vérifie la présence de colonnes obligatoires."""
    if df is None or df.empty:
        raise ValueError("Le DataFrame fourni est vide ou None.")

    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes absentes du dataset : {missing}")


def _ensure_numeric(df: DataFrame, columns: list) -> None:
    """Vérifie qu'une liste de colonnes est numérique."""
    non_numeric = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
    if non_numeric:
        raise TypeError(
            f"Les colonnes suivantes doivent être numériques : {non_numeric}"
        )


# ===========================================================
# 1. Distribution du score de risque par stage
# ===========================================================
def analyze_risk_distribution(
    df: DataFrame,
    score_col: str = "diabetes_risk_score",
    stage_col: str = "diabetes_stage",
    show: bool = True,
):
    """
    Analyse la distribution du score de risque par stage avec un histogramme
    et une approximation gaussienne pour chaque groupe.
    """
    _ensure_columns(df, [score_col, stage_col])
    _ensure_numeric(df, [score_col])

    logger.info("Analyse distribution du score de risque.")

    df_clean = df.dropna(subset=[score_col, stage_col])
    logger.info(f"Lignes conservées après dropna : {len(df_clean)}")

    # Convertir les catégories en string pour éviter groupby implicites via Plotly
    df_plot = df_clean.copy()
    df_plot[stage_col] = df_plot[stage_col].astype(str)

    # -------------------------------------------------------
    # Statistiques descriptives (évite le warning)
    # -------------------------------------------------------
    stats = df_clean.groupby(stage_col, observed=True)[score_col].agg(
        ["count", "mean", "std", "min", "max"]
    )

    # Histogramme
    fig = px.histogram(
        df_plot,
        x=score_col,
        color=stage_col,
        nbins=50,
        histnorm="probability density",
        barmode="overlay",
        opacity=0.6,
    )

    # Ajout de courbes normales
    x = np.linspace(df_clean[score_col].min(), df_clean[score_col].max(), 200)

    for stage, subset in df_clean.groupby(stage_col, observed=True):
        if subset[score_col].nunique() <= 1:
            continue

        mu = subset[score_col].mean()
        sigma = subset[score_col].std()

        if sigma == 0 or np.isnan(sigma):
            continue

        fig.add_trace(
            go.Scatter(
                x=x,
                y=norm.pdf(x, mu, sigma),
                mode="lines",
                name=f"Norm {stage}",
            )
        )

    fig.update_layout(
        title=f"Distribution de {score_col} par {stage_col}",
        xaxis_title=score_col,
        yaxis_title="Densité",
    )

    if show:
        fig.show()

    return fig, stats


# ===========================================================
# 2. Analyse générale du score de risque
# ===========================================================
def analyze_risk_score(
    df: DataFrame,
    score_col: str = "diabetes_risk_score",
    stage_col: str = "diabetes_stage",
    diag_col: str = "diagnosed_diabetes",
    show: bool = True,
):
    """
    Analyse globale du score de risque :
    - Histogramme par statut diagnostiqué
    - Boxplot par stage
    - Interprétation de l'échelle du score
    """

    _ensure_columns(df, [score_col, stage_col, diag_col])
    _ensure_numeric(df, [score_col])

    logger.info("Analyse générale du score de risque.")

    # Conversion pour empêcher Plotly de déclencher groupby → FutureWarning
    df_plot = df.copy()
    df_plot[stage_col] = df_plot[stage_col].astype(str)
    df_plot[diag_col] = df_plot[diag_col].astype(str)

    fig_hist = px.histogram(
        df_plot,
        x=score_col,
        color=diag_col,
        nbins=50,
        barmode="overlay",
        opacity=0.6,
        title=f"Distribution de {score_col} par {diag_col}",
    )

    fig_box = px.box(
        df_plot,
        x=stage_col,
        y=score_col,
        color=diag_col,
        title=f"{score_col} par {stage_col} et {diag_col}",
    )

    max_val = df[score_col].max()
    if max_val <= 1:
        interpretation = "probabilité (0–1)"
    elif max_val <= 100:
        interpretation = "score sur une échelle 0–100"
    else:
        interpretation = "score non calibré (>100)"

    if show:
        fig_hist.show()
        fig_box.show()

    return {
        "histogram": fig_hist,
        "boxplot": fig_box,
        "max_value": max_val,
        "interpretation": interpretation,
    }


# ===========================================================
# 3. Relation variable numérique ↔ cible
# ===========================================================
def plot_numeric_vs_target(
    df: DataFrame,
    x_col: str,
    target_col: str = "diagnosed_diabetes",
    bins: int = 20,
    show: bool = True,
):
    """
    Analyse l'effet d'une variable numérique sur une cible.
    - Panel 1 : histogramme coloré par cible
    - Panel 2 : moyenne de la cible par tranche de la variable
    """
    _ensure_columns(df, [x_col, target_col])
    _ensure_numeric(df, [x_col])

    logger.info(f"Relation {x_col} -> {target_col}")

    df_clean = df.dropna(subset=[x_col, target_col])

    # Conversion pour éviter FutureWarning via Plotly
    df_plot = df_clean.copy()
    df_plot[target_col] = df_plot[target_col].astype(str)

    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.6, 0.4],
        subplot_titles=[
            f"Distribution de {x_col} par {target_col}",
            f"Moyenne de {target_col} par tranches de {x_col}",
        ],
    )

    # Panel 1
    hist = px.histogram(
        df_plot,
        x=x_col,
        color=target_col,
        nbins=bins,
        barmode="overlay",
        opacity=0.6,
    )
    for tr in hist.data:
        fig.add_trace(tr, row=1, col=1)

    # Panel 2 : moyenne par bin
    df_clean["__bin"] = pd.cut(df_clean[x_col], bins=bins)

    grouped = (
        df_clean.groupby("__bin", observed=True)[target_col]
        .mean()
        .reset_index()
        .rename(columns={target_col: "target_mean"})
    )

    grouped["bin_str"] = grouped["__bin"].astype(str)

    fig.add_trace(
        go.Bar(
            x=grouped["bin_str"],
            y=grouped["target_mean"],
            name=f"Moyenne {target_col}",
        ),
        row=1,
        col=2,
    )

    fig.update_layout(title=f"Impact de {x_col} sur {target_col}")

    if show:
        fig.show()

    df_clean.drop(columns="__bin", inplace=True)

    return fig


# ===========================================================
# 4. Distribution simple d’une variable numérique
# ===========================================================
def plot_numeric_feature_distribution(
    df: DataFrame,
    numeric_col: str,
    show: bool = True,
):
    """
    Affiche la distribution d'une variable numérique (histogramme + boxplot).
    """
    _ensure_columns(df, [numeric_col])
    _ensure_numeric(df, [numeric_col])

    logger.info(f"Distribution de {numeric_col}.")

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            f"Histogramme de {numeric_col}",
            f"Boxplot de {numeric_col}",
        ],
    )

    hist = px.histogram(df, x=numeric_col, nbins=30)
    for tr in hist.data:
        fig.add_trace(tr, row=1, col=1)

    box = px.box(df, x=numeric_col, orientation="h")
    for tr in box.data:
        fig.add_trace(tr, row=1, col=2)

    fig.update_layout(title=f"Distribution de {numeric_col}")

    if show:
        fig.show()

    return fig


# ===========================================================
# 5. Scatter 2D entre deux variables numériques
# ===========================================================
def plot_numeric_scatter_with_target(
    df: DataFrame,
    x_col: str,
    y_col: str,
    target_col: str,
    show: bool = True,
):
    """
    Scatter plot entre deux variables numériques, coloré par la cible.
    """
    _ensure_columns(df, [x_col, y_col, target_col])
    _ensure_numeric(df, [x_col, y_col])

    logger.info(f"Scatter: {x_col} vs {y_col}, target={target_col}")

    df_plot = df.copy()
    df_plot[target_col] = df_plot[target_col].astype(str)

    # Deux couleurs vives et contrastées
    vivid_colors = ["#FF0000", "#0000FF"]  # Rouge vif, Bleu vif

    fig = px.scatter(
        df_plot,
        x=x_col,
        y=y_col,
        color=target_col,
        opacity=0.7,
        color_discrete_sequence=vivid_colors,
        title=f"{x_col} vs {y_col} coloré par {target_col}",
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
    )

    if show:
        fig.show()

    return fig
