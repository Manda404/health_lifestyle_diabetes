"""
Service métier de validation des enregistrements par rapport au FeatureSchema.

Rôle :
------
- vérifier qu'une ligne de données contient toutes les colonnes attendues,
- valider les types Python (int, float, str…),
- produire des messages d'erreurs clairs en cas de problème.

Ce service ne connaît pas les DataFrame : il travaille avec des dict.
"""

from dataclasses import dataclass
from typing import Any, Dict, Type

from health_lifestyle_diabetes.infrastructure.utils.exceptions import (
    FeatureValidationError,
)

from ..entities.features_schema import FEATURE_SCHEMA


@dataclass
class FeatureValidationService:
    """
    Service métier de validation des enregistrements par rapport au FeatureSchema.

    Ce service garantit que les données d'entrée (e.g., une requête de prédiction)
    possèdent toutes les colonnes requises et que le typage Python de chaque valeur
    est compatible avec les attentes du modèle ML.

    Attributs:
        schema (Dict[str, Type]): Dictionnaire des types attendus, extrait de FEATURE_SCHEMA.
                                   Exemple: {"age": int, "bmi": float}.
    """

    # Récupère le dictionnaire des types attendus : {"colonne": type_attendu}
    schema: Dict[str, Type] = FEATURE_SCHEMA.expected_types

    def validate(self, record: Dict[str, Any]) -> None:
        """
        Valide un enregistrement (ligne de données) pour vérifier la présence
        des colonnes et la compatibilité des types.

        Le service ne vérifie que la structure et le typage Python ; il ne vérifie
        pas les bornes min/max ni les valeurs métier spécifiques.

        Args:
            record (Dict[str, Any]): Dictionnaire représentant une ligne de données
                                     à valider (e.g., les données du DTO).

        Raises:
            FeatureValidationError: Si une colonne attendue est manquante dans l'enregistrement.
            FeatureValidationError: Si le type Python d'une valeur est incompatible avec le type attendu.
        """
        for col, expected_type in self.schema.items():
            # 1. Vérification de la PRÉSENCE de la colonne
            if col not in record:
                raise FeatureValidationError(f"Colonne manquante : {col}")

            value = record[col]

            # 2. Vérification du TYPAGE
            if not isinstance(value, expected_type):
                raise FeatureValidationError(
                    f"Colonne '{col}' doit être de type {expected_type.__name__}, "
                    f"reçu : {type(value).__name__}"
                )
