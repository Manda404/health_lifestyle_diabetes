from health_lifestyle_diabetes.domain.ports.calibrator_port import CalibrationPort
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class CalibrationService:
    """
    Service applicatif orchestrant le calibrage du modèle.
    """

    def __init__(self, calibrator: CalibrationPort, logger: LoggerPort):
        self.calibrator = calibrator
        self.logger = logger

    def calibrate_model(
        self,
        model,
        X_calib,
        y_calib,
        **kwargs
    ):
        self.logger.info("Début du calibrage modèle...")
        calibrated_model = self.calibrator.calibrate(model, X_calib, y_calib, **kwargs)
        self.logger.info("Modèle calibré prêt à l'utilisation.")
        return calibrated_model