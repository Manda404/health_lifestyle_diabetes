from dataclasses import dataclass
from pandas import DataFrame

from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

# Import des fonctions EDA (infrastructure)
from health_lifestyle_diabetes.infrastructure.ml.eda.dataset_summary import (
    summarize_dataset,
    identify_feature_types,
)
from health_lifestyle_diabetes.infrastructure.ml.eda.numeric_analysis import (
    analyze_risk_distribution,
    analyze_risk_score,
    plot_numeric_vs_target,
    plot_numeric_feature_distribution,
)
from health_lifestyle_diabetes.infrastructure.ml.eda.target_analysis import (
    plot_target_distribution,
    plot_cumulative_distribution,
)

logger = get_logger("usecase.perform_eda")


@dataclass
class PerformEDAUseCase:
    """
    Cas d’usage : Orchestration complète de l’EDA.
    
    ⚠️ IMPORTANT :
    Ce use case NE contient AUCUNE logique EDA.
    Il se contente de coordonner les services EDA situés
    dans l’infrastructure et de renvoyer des données utiles.
    """

    target_col: str = "diagnosed_diabetes"
    risk_score_col: str = "diabetes_risk_score"
    diabetes_stage_col: str = "diabetes_stage"

    def execute(self, df: DataFrame):
        """
        Exécute différentes analyses EDA et renvoie
        un résumé utile pour inspection programmatique.
        """

        if df is None or df.empty:
            logger.error("Dataset vide : impossible d'exécuter l'EDA.")
            raise ValueError("Le DataFrame fourni est vide.")

        logger.info("===== DÉBUT DU USE CASE : EDA =====")

        # -------------------------------------------------------------
        # 1) Résumé global du dataset
        # -------------------------------------------------------------
        summary_df = summarize_dataset(df)
        numeric_cols, categorical_cols = identify_feature_types(df)
        logger.info("Résumé dataset + détection types terminés.")

        # -------------------------------------------------------------
        # 2) Analyse de la cible
        # -------------------------------------------------------------
        logger.info("Analyse de la variable cible...")
        plot_target_distribution(df, self.target_col)
        cumulative_df = plot_cumulative_distribution(df, self.target_col)

        # -------------------------------------------------------------
        # 3) Analyse score de risque (si présent)
        # -------------------------------------------------------------
        if self.risk_score_col in df.columns and self.diabetes_stage_col in df.columns:
            logger.info("Analyse du score de risque...")
            analyze_risk_distribution(df, self.risk_score_col, self.diabetes_stage_col)
            analyze_risk_score(df, self.risk_score_col, self.diabetes_stage_col, self.target_col)
        else:
            logger.warning("Colonnes score/stage absentes : analyse du risque ignorée.")

        # -------------------------------------------------------------
        # 4) Analyse numérique : chaque variable numérique vs cible
        # -------------------------------------------------------------
        logger.info("Analyse des variables numériques...")
        for col in numeric_cols:
            if col == self.target_col:
                continue

            try:
                plot_numeric_feature_distribution(df, col)
                plot_numeric_vs_target(df, col)
            except Exception as e:
                logger.warning(f"Impossible d'analyser '{col}' : {e}")

        logger.info("===== FIN DU USE CASE : EDA =====")

        # Ce use case renvoie des objets utiles pour inspection
        return {
            "summary": summary_df,
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "cumulative_target_distribution": cumulative_df,
        }
