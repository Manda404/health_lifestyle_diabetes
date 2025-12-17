from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ConfusionMatrixResult:
    """
    Représentation métier d'une matrice de confusion.

    Cette entité est indépendante de toute librairie technique
    (sklearn, numpy, pandas, matplotlib).
    """

    labels: List[int]
    class_names: List[str]

    matrix: List[List[int]]
    normalized_matrix: List[List[float]]