"""
DecisionThresholdPolicy
-----------------------

Politique métier définissant le seuil de décision pour la classification.

Rôle :
------
- encapsuler le seuil comme règle métier stable,
- éviter la propagation de valeurs magiques (0.5, 0.7, etc.),
- centraliser la logique de décision clinique ou métier.

Exemples de politiques :
------------------------
- Prévention : seuil bas → minimiser les faux négatifs
- Diagnostic : seuil élevé → minimiser les faux positifs
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionThresholdPolicy:
    """
    Politique métier de seuil de décision.

    Cette classe représente une règle métier stable,
    indépendante du modèle et des outils techniques.
    """

    threshold: float

    def __post_init__(self):
        if not 0.0 < self.threshold < 1.0:
            raise ValueError(
                "Le seuil de décision doit être compris strictement entre 0 et 1."
            )

    # ------------------------------------------------------------------
    @classmethod
    def prevention_policy(cls) -> "DecisionThresholdPolicy":
        """
        Politique orientée prévention.

        Objectif :
        - réduire les faux négatifs,
        - détecter le plus tôt possible les patients à risque.
        """
        return cls(threshold=0.30)

    @classmethod
    def diagnostic_policy(cls) -> "DecisionThresholdPolicy":
        """
        Politique orientée diagnostic clinique.

        Objectif :
        - réduire les faux positifs,
        - augmenter la confiance dans la décision.
        """
        return cls(threshold=0.70)

    @classmethod
    def balanced_policy(cls) -> "DecisionThresholdPolicy":
        """
        Politique équilibrée (par défaut).

        Compromis entre précision et rappel.
        """
        return cls(threshold=0.50)