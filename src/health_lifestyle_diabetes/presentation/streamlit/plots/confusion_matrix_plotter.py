import matplotlib.pyplot as plt

from health_lifestyle_diabetes.domain.entities.confusion_matrix_result import (
    ConfusionMatrixResult,
)


class ConfusionMatrixPlotter:
    """
    Affichage matplotlib des matrices de confusion.

    - plot(...) crée sa propre figure (usage rapide).
    - plot_on_ax(...) dessine sur un axe existant (subplots).
    """

    @staticmethod
    def plot_on_ax(
        ax,
        result: ConfusionMatrixResult,
        *,
        title: str,
        cmap: str = "Blues",
        show_colorbar: bool = True,
    ):
        """
        Dessine une matrice de confusion sur un axe matplotlib existant.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axe sur lequel dessiner.
        result : ConfusionMatrixResult
            Résultat métier (brut + normalisé).
        title : str
            Titre du subplot.
        cmap : str
            Colormap matplotlib.
        show_colorbar : bool
            Afficher la colorbar pour ce subplot.
        """
        cm = result.matrix
        cmn = result.normalized_matrix

        im = ax.imshow(cmn, cmap=cmap)

        ax.set_title(title)
        ax.set_xlabel("Prédit")
        ax.set_ylabel("Réel")

        ax.set_xticks(range(len(result.labels)))
        ax.set_yticks(range(len(result.labels)))
        ax.set_xticklabels(result.class_names)
        ax.set_yticklabels(result.class_names)

        for i in range(len(result.labels)):
            for j in range(len(result.labels)):
                ax.text(
                    j,
                    i,
                    f"{cm[i][j]}\n({cmn[i][j]:.1f}%)",
                    ha="center",
                    va="center",
                )

        if show_colorbar:
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        return im

    @staticmethod
    def plot(
        result: ConfusionMatrixResult,
        *,
        title: str,
        cmap: str = "Blues",
    ):
        """
        Version simple : crée sa propre figure.
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        ConfusionMatrixPlotter.plot_on_ax(ax, result, title=title, cmap=cmap)
        plt.tight_layout()
        plt.show()
