# src/health_lifestyle_diabetes/domain/ports/feature_engineering_port.py

from __future__ import annotations

from typing import Any, Protocol


class FeatureEngineeringPort(Protocol):
    """
    Décrit ce que le domaine attend du feature engineering.

    Le domaine ne sait pas si l'implémentation utilise Pandas, Spark,
    des arrays Numpy, etc. Il sait seulement que l'entrée et la sortie
    sont des "tables" abstraites.
    """

    def transform(self, raw_table: Any) -> Any:
        """
        Applique le pipeline complet de feature engineering
        sur une table de données brutes.

        Parameters
        ----------
        raw_table : Any
            Données brutes (ex: DataFrame, RDD, etc.)

        Returns
        -------
        Any
            Données transformées, prêtes pour le modèle.
        """
        ...
