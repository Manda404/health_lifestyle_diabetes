from typing import Sequence

from health_lifestyle_diabetes.domain.services.confusion_matrix_service import (
    ConfusionMatrixService,
)
from health_lifestyle_diabetes.domain.entities.confusion_matrix_result import (
    ConfusionMatrixResult,
)


class EvaluateModelUseCase:
    """
    Use case responsable de l'évaluation d'un modèle de classification.

    Il orchestre :
    - les prédictions du modèle,
    - la construction des métriques métier,
    - sans dépendre de sklearn ni matplotlib.
    """

    def __init__(self, confusion_service: ConfusionMatrixService):
        self.confusion_service = confusion_service

    def execute(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
    ) -> ConfusionMatrixResult:
        """
        Lance l'évaluation du modèle.

        Returns
        -------
        ConfusionMatrixResult
            Résultat métier prêt pour affichage ou reporting.
        """

        return self.confusion_service.build(
            y_true=y_true,
            y_pred=y_pred,
            labels=[0, 1],
            class_names=["Non diabétique", "Diabétique"],
        )
