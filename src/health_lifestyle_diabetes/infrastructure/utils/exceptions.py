"""
exceptions.py
--------------

Définition d'exceptions personnalisées utilisées dans l'application.
Ces exceptions permettent une gestion propre des erreurs à travers les
différentes couches : domain, application, infrastructure.

Les exceptions sont volontairement simples pour rester compatibles avec
la Clean Architecture (pas de dépendance externe).
"""


# ============================================================
# ===============   Exceptions générales   ====================
# ============================================================

class BaseAppError(Exception):
    """Exception racine pour toutes les erreurs de l'application."""
    pass


class ConfigLoadingError(BaseAppError):
    """Erreur liée au chargement ou au parsing d'un fichier de configuration."""
    pass


class LoggerInitializationError(BaseAppError):
    """Erreur survenue lors de l'initialisation du logger."""
    pass


# ============================================================
# ===============   Exceptions Dataset   ======================
# ============================================================

class DatasetLoadingError(BaseAppError):
    """Erreur lors du chargement d'un dataset (fichier manquant, corrompu, etc.)."""
    pass


class DatasetSavingError(BaseAppError):
    """Erreur lors de la sauvegarde d'un dataset."""
    pass


class DatasetValidationError(BaseAppError):
    """Erreur lorsqu'un dataset ne respecte pas un schéma attendu."""
    pass


# ============================================================
# ===============   Exceptions Modèle ML   ====================
# ============================================================

class ModelLoadingError(BaseAppError):
    """Erreur lors du chargement d'un modèle (fichier manquant, incompatible, etc.)."""
    pass


class ModelSavingError(BaseAppError):
    """Erreur lors de la sauvegarde d'un modèle."""
    pass


class ModelTrainingError(BaseAppError):
    """Erreur survenue pendant l'entraînement du modèle."""
    pass


class ModelPredictionError(BaseAppError):
    """Erreur survenue lors d'une prédiction."""
    pass


# ============================================================
# ===============   Exceptions Domaine (métier) ===============
# ============================================================

class InvalidPatientProfileError(BaseAppError):
    """Erreur métier : les données du patient sont invalides ou incomplètes."""
    pass


class FeatureEngineeringError(BaseAppError):
    """Erreur métier lors de la création de features."""
    pass


class PredictionServiceError(BaseAppError):
    """Erreur métier lors de l'appel au service de prédiction."""
    pass


__all__ = [
    "BaseAppError",
    "ConfigLoadingError",
    "LoggerInitializationError",

    "DatasetLoadingError",
    "DatasetSavingError",
    "DatasetValidationError",

    "ModelLoadingError",
    "ModelSavingError",
    "ModelTrainingError",
    "ModelPredictionError",

    "InvalidPatientProfileError",
    "FeatureEngineeringError",
    "PredictionServiceError",
]
