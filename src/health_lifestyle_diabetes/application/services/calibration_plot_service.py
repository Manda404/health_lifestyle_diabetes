from health_lifestyle_diabetes.domain.ports.calibration_plot_port import (
    CalibrationPlotPort,
)
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class CalibrationPlotService:
    """
    Service d'orchestration pour générer les courbes de calibration.
    """

    def __init__(self, plotter: CalibrationPlotPort, logger: LoggerPort):
        self.plotter = plotter
        self.logger = logger

    def generate(
        self,
        y_true,
        y_proba_before,
        y_proba_after,
        model_name: str,
        bins: int = 10,
        save: bool=False,
    ):
        self.logger.info("Début génération plots calibration...")
        self.plotter.plot_calibration(
            y_true,
            y_proba_before,
            y_proba_after,
            model_name=model_name,
            bins=bins,
            save=save,
        )
        self.logger.info("Plots calibration générés avec succès.")
