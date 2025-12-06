import numpy as np
import pandas as pd
import plotly.express as px
from pandas import DataFrame
from scipy.stats import norm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger


logger_risk_distribution = get_logger("eda.risk_distribution")
logger_risk_score = get_logger("eda.risk_score")
logger_numeric_vs_target = get_logger("eda.numeric_vs_target")
logger_numeric_feature = get_logger("eda.numeric_feature_dist")
logger_scatter = get_logger("eda.numeric_scatter")


# -------------------------
# Helpers internes
# -------------------------
def _ensure_columns(df: DataFrame, columns: list):
    for col in columns:
        if col not in df:
            raise ValueError(f"Colonne '{col}' absente du dataset.")


def _ensure_numeric(df: DataFrame, col: str):
    if not pd.api.types.is_numeric_dtype(df[col]):
        raise TypeError(f"La colonne '{col}' doit être numérique.")


# -------------------------
# 1. Analyse distribution risque par stage
# -------------------------
def analyze_risk_distribution(
    df: DataFrame,
    score_col: str = "diabetes_risk_score",
    stage_col: str = "diabetes_stage",
):
    _ensure_columns(df, [score_col, stage_col])

    logger = logger_risk_distribution
    logger.info("Analyse de distribution du score de risque.")

    df_clean = df.dropna(subset=[score_col, stage_col])
    logger.info(f"Lignes analysées : {len(df_clean)}")

    # Statistiques
    stats = df_clean.groupby(stage_col)[score_col].agg(
        ["count", "mean", "std", "min", "max"]
    )
    logger.debug(f"Statistiques :\n{stats}")

    # Histogrammes + curves
    fig = px.histogram(
        df_clean,
        x=score_col,
        color=stage_col,
        nbins=50,
        histnorm="probability density",
        barmode="overlay",
    )

    x = np.linspace(df_clean[score_col].min(), df_clean[score_col].max(), 200)
    for stage, subset in df_clean.groupby(stage_col):
        mu, sigma = subset[score_col].mean(), subset[score_col].std()
        fig.add_trace(
            go.Scatter(
                x=x, y=norm.pdf(x, mu, sigma), mode="lines", name=f"Norm {stage}"
            )
        )

    fig.update_layout(title=f"Distribution de {score_col} par {stage_col}")
    fig.show()


# -------------------------
# 2. Analyse score risque
# -------------------------
def analyze_risk_score(
    df: DataFrame,
    score_col: str = "diabetes_risk_score",
    stage_col: str = "diabetes_stage",
    diag_col: str = "diagnosed_diabetes",
):
    _ensure_columns(df, [score_col, stage_col, diag_col])

    logger = logger_risk_score
    logger.info("Analyse du score de risque.")

    # Histogramme global
    px.histogram(df, x=score_col, color=diag_col, nbins=50).show()

    # Boxplot
    px.box(df, x=stage_col, y=score_col, color=diag_col).show()

    # Analyse score
    max_val = df[score_col].max()
    if max_val <= 1:
        logger.info("Score interprété comme probabilité (0–1).")
    elif max_val <= 100:
        logger.info("Score sur une échelle 0–100.")
    else:
        logger.warning("Score non calibré (>100).")


# -------------------------
# 3. Relation variable numérique ↔ cible
# -------------------------
def plot_numeric_vs_target(df: DataFrame, x_col: str, bins: int = 40):
    target_col = "diagnosed_diabetes"
    _ensure_columns(df, [x_col, target_col])
    _ensure_numeric(df, x_col)
    _ensure_numeric(df, target_col)

    logger_numeric_vs_target.info(f"Analyse de {x_col} vs {target_col}.")

    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3])

    # Histogrammes
    hist = px.histogram(df, x=x_col, color=target_col, nbins=bins)
    for trace in hist.data:
        fig.add_trace(trace, row=1, col=1)

    # Box
    box = px.box(df, x=x_col, y=target_col, orientation="h")
    for trace in box.data:
        fig.add_trace(trace, row=1, col=2)

    fig.update_layout(title=f"Distribution & effet de {x_col} sur {target_col}")
    fig.show()


# -------------------------
# 4. Distribution simple d'une variable numérique
# -------------------------
def plot_numeric_feature_distribution(df: DataFrame, numeric_col: str):
    _ensure_columns(df, [numeric_col])
    _ensure_numeric(df, numeric_col)

    logger_numeric_feature.info(f"Distribution de {numeric_col}")

    fig = make_subplots(rows=1, cols=2)

    hist = px.histogram(df, x=numeric_col, nbins=30)
    fig.add_trace(hist.data[0], row=1, col=1)

    box = px.box(df, x=numeric_col, orientation="h")
    fig.add_trace(box.data[0], row=1, col=2)

    fig.update_layout(title=f"Distribution de {numeric_col}")
    fig.show()


# -------------------------
# 5.
# -------------------------


def plot_numeric_scatter_with_target(
    df: pd.DataFrame, x_col: str, y_col: str, target_col: str
):
    """
    Scatter plot 2D entre deux features numériques,
    avec coloration par la cible (classification).

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame contenant les données.
    x_col : str
        Colonne utilisée pour l'axe X (feature numérique).
    y_col : str
        Colonne utilisée pour l'axe Y (feature numérique).
    target_col : str
        Colonne cible pour colorer les points.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        La figure scatter 2D colorée par target.
    """

    # Vérifications
    for col in [x_col, y_col, target_col]:
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' est introuvable dans le DataFrame.")

    logger_scatter.info(
        "Visualisation scatter 2D : X=%s, Y=%s, Target=%s", x_col, y_col, target_col
    )

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=target_col,
        opacity=0.7,
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Scatter plot 2D : '{x_col}' vs '{y_col}' coloré par '{target_col}'",
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        legend_title=target_col,
    )

    return fig
