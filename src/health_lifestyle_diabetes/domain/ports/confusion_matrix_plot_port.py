# --------------------------------------------------------------
# Domaine : Port (interface) pour l'affichage des CM
# --------------------------------------------------------------

from typing import Any, Optional, Protocol
from health_lifestyle_diabetes.domain.entities.confusion_matrix_config import ConfusionMatrixConfig

class ConfusionMatrixPlotPort(Protocol):
    """
    Interface définissant le contrat de visualisation.
    Implémentée dans l'infrastructure (ex: Matplotlib).
    """

    def plot(
        self,
        model: Any,
        *,
        X_test: Any,
        y_test: Any,
        config: ConfusionMatrixConfig,
        X_valid: Optional[Any] = None,
        y_valid: Optional[Any] = None,
        run_name: Optional[str] = None,
        save: bool = False
    ) -> None:
        """Affiche (et/ou sauvegarde) une ou plusieurs matrices de confusion."""
        ...