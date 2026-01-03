from typing import Protocol, Dict, Optional, Sequence


class MetricsPlotterPort(Protocol):
    """
    Port abstrait pour la visualisation des métriques d'évaluation.

    Le domaine exprime le besoin d'afficher des métriques,
    sans connaître la technologie utilisée (matplotlib, plotly, etc.).
    """

    def plot_metrics(
        self,
        metrics: Dict[str, float],
        *,
        title: str,
        selected_metrics: Optional[Sequence[str]] = None,
        as_percentage: bool = True,
    ) -> None:
        """
        Affiche des métriques sous forme graphique.

        Règles fonctionnelles :
        -----------------------
        - selected_metrics = None → métriques par défaut
        - certaines métriques absentes → ignorées avec notification
        - aucune métrique valide → fallback métriques par défaut

        Parameters
        ----------
        metrics : dict[str, float]
            Dictionnaire des métriques disponibles.
        title : str
            Titre de la visualisation.
        selected_metrics : sequence[str] | None
            Liste ordonnée des métriques à afficher
            (list, tuple, etc.).
        as_percentage : bool
            Affiche les scores en pourcentage si True.
        """
        ...