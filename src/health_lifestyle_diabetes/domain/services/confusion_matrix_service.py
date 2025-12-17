from typing import Sequence

from health_lifestyle_diabetes.domain.entities.confusion_matrix_result import (
    ConfusionMatrixResult,
)
from health_lifestyle_diabetes.domain.ports.confusion_matrix_port import (
    ConfusionMatrixPort,
)


class ConfusionMatrixService:
    """
    Service métier responsable de la construction
    d'une matrice de confusion interprétable.

    Responsabilités :
    -----------------
    - déléguer le calcul technique au port,
    - encapsuler le résultat dans une entité métier,
    - rester totalement indépendant de sklearn / pandas.
    """

    def __init__(self, adapter: ConfusionMatrixPort):
        self.adapter = adapter

    def build(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        labels: Sequence[int],
        class_names: Sequence[str],
    ) -> ConfusionMatrixResult:
        """
        Construit un objet métier ConfusionMatrixResult.
        """

        cm, cmn = self.adapter.compute(y_true, y_pred, labels)

        return ConfusionMatrixResult(
            labels=list(labels),
            class_names=list(class_names),
            matrix=cm,
            normalized_matrix=cmn,
        )
