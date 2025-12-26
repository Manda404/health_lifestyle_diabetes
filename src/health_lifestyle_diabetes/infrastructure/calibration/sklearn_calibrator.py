from health_lifestyle_diabetes.domain.ports.calibrator_port import CalibrationPort
from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort
from sklearn.calibration import CalibratedClassifierCV


class SklearnCalibrationAdapter(CalibrationPort):
    """
    Adapter Sklearn permettant de calibrer un modèle ML
    selon les paramètres CalibratedClassifierCV (v1.8+).
    """

    def __init__(self, logger: LoggerPort):
        self.logger = logger

    def calibrate(
        self,
        model,
        X_calib,
        y_calib,
        **kwargs
    ):
        """
        Calibre un modèle selon l'approche choisie.

        kwargs possibles :
        - method: 'sigmoid' | 'isotonic' | 'temperature'
        - cv: int | None ('auto' = 5 folds)
        - ensemble: True | False | 'auto'
        """

        method = kwargs.get("method", "sigmoid")
        cv = kwargs.get("cv", 5)
        ensemble = kwargs.get("ensemble", "auto")

        self.logger.info(
            f"Calibration du modèle avec method='{method}', cv={cv}, ensemble={ensemble}"
        )

        calibrator = CalibratedClassifierCV(
            estimator=model,
            method=method,
            cv=cv,
            ensemble=ensemble
        )

        calibrator.fit(X_calib, y_calib)

        self.logger.info("Calibration terminée avec succès.")
        return calibrator
