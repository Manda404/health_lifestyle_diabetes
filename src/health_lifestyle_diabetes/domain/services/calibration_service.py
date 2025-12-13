"""
Service métier pour préparer les points d'une courbe de calibration.

Rôle :
------
- découper les probabilités en "bins" (classes de probas),
- calculer :
    * probabilité moyenne prédite par bin,
    * fréquence réelle observée de la classe positive par bin,
- produire des données prêtes à être tracées (côté infrastructure).

Ce service ne trace rien, il ne fait que du calcul pur.
"""

from typing import List, Sequence, Tuple


class CalibrationService:
    """
    Prépare les points de la courbe de calibration.
    """

    def __init__(self, n_bins: int = 10):
        """
        Paramètres
        ----------
        n_bins : int
            Nombre de bins utilisés pour la calibration.
        """
        self.n_bins = n_bins

    def compute_calibration_points(
        self,
        y_true: Sequence[int],
        y_proba: Sequence[float],
    ) -> Tuple[List[float], List[float]]:
        """
        Calcule les points de calibration (x, y).

        x = probabilité moyenne prédite par bin
        y = fréquence réelle observée de la classe positive par bin

        Paramètres
        ----------
        y_true : séquence d'int
            Labels réels (0 ou 1).
        y_proba : séquence de float
            Probabilités prédites (entre 0 et 1).

        Retour
        ------
        (mean_predicted, fraction_positive) : (List[float], List[float])
        """
        if len(y_true) != len(y_proba):
            raise ValueError("y_true et y_proba doivent avoir la même longueur.")

        # Tri par probabilité croissante
        pairs = sorted(zip(y_proba, y_true), key=lambda x: x[0])
        n = len(pairs)
        if n == 0:
            return [], []

        bin_size = max(1, n // self.n_bins)

        mean_predicted: List[float] = []
        fraction_positive: List[float] = []

        for i in range(0, n, bin_size):
            chunk = pairs[i : i + bin_size]
            if not chunk:
                continue

            probs_chunk = [p for p, _ in chunk]
            labels_chunk = [t for _, t in chunk]

            mean_p = sum(probs_chunk) / len(probs_chunk)
            frac_pos = sum(labels_chunk) / len(labels_chunk)

            mean_predicted.append(mean_p)
            fraction_positive.append(frac_pos)

        return mean_predicted, fraction_positive
