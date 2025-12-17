from typing import Protocol, Sequence, Tuple, List


class ConfusionMatrixPort(Protocol):
    """
    Port abstrait pour le calcul d'une matrice de confusion.

    Le domaine définit le CONTRAT,
    l'infrastructure fournit l'implémentation concrète (ex: sklearn).
    """

    def compute(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        labels: Sequence[int],
    ) -> Tuple[List[List[int]], List[List[float]]]:
        """
        Calcule la matrice de confusion brute et normalisée.

        Returns
        -------
        cm : list[list[int]]
            Matrice brute (TN, FP / FN, TP).
        cmn : list[list[float]]
            Matrice normalisée ligne par ligne (%).
        """
        ...
