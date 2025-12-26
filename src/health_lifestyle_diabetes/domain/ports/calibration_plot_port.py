from typing import Optional, Protocol, Sequence

from health_lifestyle_diabetes.domain.ports.logger_port import LoggerPort


class CalibrationPlotPort(Protocol):
    """
    Port applicatif : génération de plots de calibration probabiliste.
    Ce port est utilisé par l'application, pas le domaine.
    """

    logger: LoggerPort  # chaque adapter devra en recevoir un

    def plot_calibration(
        self,
        y_true: Sequence[int],
        y_proba_before: Sequence[float],
        y_proba_after: Sequence[float],
        bins: int = 10,
        model_name: Optional[str] = None,
        save: bool = False,
    ) -> None:
        """
        Produit les plots 'avant vs après calibration'.

        Parameters
        ----------
        y_true : labels réels (0/1)
        y_proba_before : probas du modèle avant calibration
        y_proba_after : probas du modèle calibré
        bins : nombre de bins pour la calibration_curve
        model_name : nom optionnel du modèle (pour le titre du plot)
        save : indique si on sauvegarde le plot ou non
        """
        ...
