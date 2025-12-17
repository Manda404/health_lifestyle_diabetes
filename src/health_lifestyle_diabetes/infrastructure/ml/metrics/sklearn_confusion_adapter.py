from typing import Sequence, Tuple, List

from sklearn.metrics import confusion_matrix

from health_lifestyle_diabetes.domain.ports.confusion_matrix_port import (
    ConfusionMatrixPort,
)


class SklearnConfusionMatrixAdapter(ConfusionMatrixPort):
    """
    Implémentation sklearn du port ConfusionMatrixPort.

    Cette classe :
    - dépend de sklearn (donc INFRA),
    - ne contient AUCUNE logique métier,
    - peut être remplacée sans impacter le domaine.
    """

    def compute(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        labels: Sequence[int],
    ) -> Tuple[List[List[int]], List[List[float]]]:

        cm = confusion_matrix(y_true, y_pred, labels=labels)

        # Normalisation ligne par ligne
        row_sums = cm.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        cmn = cm / row_sums * 100.0

        return cm.tolist(), cmn.tolist()
