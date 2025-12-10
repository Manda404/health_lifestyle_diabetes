from typing import Protocol

from pandas import DataFrame


class FeatureEngineeringPort(Protocol):
    """
    Port définissant le contrat que doivent respecter tous les modules
    de feature engineering dans l'application.

    Dans la Clean Architecture :
    - le domaine dépend de ce port,
    - les implémentations concrètes (infrastructure) doivent fournir
      une méthode `transform` conforme à cette interface.

    Cette abstraction permet :
    - de brancher n’importe quel pipeline de transformation,
    - de tester l'application sans dépendre d'une implémentation réelle,
    - de garantir une séparation claire entre logique métier et infrastructure.
    """

    def transform(self, df: DataFrame) -> DataFrame:
        """
        Transforme un DataFrame en appliquant un pipeline de feature engineering.

        Paramètres
        ----------
        df : pd.DataFrame
            Données d'entrée brutes ou partiellement transformées.

        Retour
        ------
        pd.DataFrame
            DataFrame enrichi et nettoyé, prêt pour l’entraînement du modèle.
        """
        ...
