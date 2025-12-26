from typing import Any, Protocol, Sequence


class CalibrationPort(Protocol):
    """
    Port pour calibrer un modèle de classification.
    """

    def calibrate(
        self,
        model: Any,
        X_calib: Sequence,
        y_calib: Sequence,
        **kwargs
    ) -> Any:
        """
        Retourne un modèle calibré prêt à prédire.
        """
        ...
