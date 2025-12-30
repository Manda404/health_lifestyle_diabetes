# --------------------------------------------------------------
# Application : Service orchestrant l'affichage
# --------------------------------------------------------------

from typing import Any
from health_lifestyle_diabetes.domain.ports.confusion_matrix_plot_port import ConfusionMatrixPlotPort
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from health_lifestyle_diabetes.domain.entities.confusion_matrix_config import ConfusionMatrixConfig

class ConfusionMatrixService:
    """
    Use case : orchestre l'affichage des matrices de confusion.
    Ne fait qu'appeler le port ; aucune logique technique ici.
    """

    def __init__(self, plotter: ConfusionMatrixPlotPort, logger: LoggerPort):
        self.plotter = plotter
        self.logger = logger

    def run(
        self,
        model: Any,
        *,
        X_test: Any,
        y_test: Any,
        X_valid: Any = None,
        y_valid: Any = None,
        config: ConfusionMatrixConfig = ConfusionMatrixConfig(),
        run_name: str = "model_eval",
        save: bool = False,
    ) -> None:
        """Point d'entrée unique pour générer les matrices."""
        self.logger.info(f"Exécution CM avec normalisation='{config.normalization}'")

        self.plotter.plot(
            model=model,
            X_test=X_test,
            y_test=y_test,
            X_valid=X_valid,
            y_valid=y_valid,
            config=config,
            run_name=run_name,
            save=save,
        )

        self.logger.info("Matrice(s) de confusion générée(s).")