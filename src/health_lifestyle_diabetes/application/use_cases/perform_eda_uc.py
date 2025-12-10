from dataclasses import dataclass

from pandas import DataFrame

from health_lifestyle_diabetes.domain.ports.eda_service_port import EDAServicePort
from health_lifestyle_diabetes.infrastructure.utils.logger import get_logger

# from health_lifestyle_diabetes.infrastructure.ml.eda.target_analysis import (
#    plot_target_distribution,
#    plot_cumulative_distribution,
# )

logger = get_logger("usecase.perform_eda")


@dataclass
class PerformEDAUseCase:
    """
    Cas d’usage : Orchestration complète de l’EDA.

    IMPORTANT :
    Ce use case NE contient AUCUNE logique EDA.
    Il se contente de coordonner les services EDA situés
    dans l’infrastructure et de renvoyer des données utiles.
    """

    eda_service: EDAServicePort
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
        summary_df = self.eda_service.summarize_dataset(df)
        numeric_cols, categorical_cols = self.eda_service.identify_feature_types(df)
        logger.info("Résumé dataset + détection types terminés.")

        # -------------------------------------------------------------
        # 2) Analyse de la cible
        # -------------------------------------------------------------
        logger.info("Analyse de la variable cible...")
        _, target_summary = self.eda_service.plot_target_distribution(df, self.target_col)

        # -------------------------------------------------------------
        # 3) Analyse score de risque (si présent)
        # -------------------------------------------------------------
        if self.risk_score_col in df.columns and self.diabetes_stage_col in df.columns:
            logger.info("Analyse du score de risque...")
            self.eda_service.analyze_risk_distribution(
                df, self.risk_score_col, self.diabetes_stage_col
            )
            self.eda_service.analyze_risk_score(
                df, self.risk_score_col, self.diabetes_stage_col, self.target_col
            )
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
                self.eda_service.plot_numeric_feature_distribution(df, col)
                self.eda_service.plot_numeric_vs_target(df, col)
            except Exception as e:
                logger.warning(f"Impossible d'analyser '{col}' : {e}")

        # -------------------------------------------------------------
        # 5) Analyse catégorielle : répartition et cible par catégorie
        # -------------------------------------------------------------
        logger.info("Analyse des variables catégorielles...")
        categorical_analysis = []
        for col in categorical_cols:
            if col == self.target_col:
                continue

            try:
                _, proportions = self.eda_service.plot_categorical_proportions(df, col)
                _, target_cross = self.eda_service.plot_target_distribution_within_category(
                    df, col, self.target_col
                )

                categorical_analysis.append(
                    {
                        "column": col,
                        "proportions": proportions,
                        "target_crosstab": target_cross,
                    }
                )
            except Exception as e:
                logger.warning(f"Impossible d'analyser '{col}' : {e}")

        logger.info("===== FIN DU USE CASE : EDA =====")

        # Ce use case renvoie des objets utiles pour inspection
        return {
            "summary": summary_df,
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "target_distribution_summary": target_summary,
            "categorical_analysis": categorical_analysis,
        }
