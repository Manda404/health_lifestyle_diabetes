from dataclasses import dataclass

@dataclass(frozen=True)
class ConfusionMatrixConfig:
    """
    Configuration immuable (value object) pour l'affichage des matrices de confusion.

    Cette configuration sert à centraliser les paramètres nécessaires
    au rendu visuel, tout en évitant l'utilisation de variables globales
    ou de constantes dispersées dans le code.

    Elle peut être injectée :
    - dans un port (ConfusionMatrixPlotPort),
    - dans un service applicatif,
    - ou directement dans un adapter de visualisation.

    Attributes
    ----------
    normalization : str, default="pred"
        Méthode de normalisation de la matrice.
        Choix disponibles :
        - "pred" : normalisation par colonne (≃ précision ; recommandé en clinique)
        - "row"  : normalisation par ligne (≃ rappel ; prévention des faux négatifs)
        - "diag" : normalisation sur la diagonale (analyse d'erreurs relatives)

    labels : tuple, default=(0, 1)
        Valeurs numériques des classes utilisées pour l'ordre dans la matrice.

    class_labels : tuple, default=("Non-Diabétique", "Diabétique")
        Libellés lisibles associés aux labels.
        Idéal pour l'affichage orienté utilisateur / métier (ex: médecin).
    """

    normalization: str = "pred"   # row | pred | diag
    labels: tuple = (0, 1)
    class_labels: tuple = ("Non-Diabétique", "Diabétique")
    #fig_size: tuple = (8, 6)  # Taille de la figure Matplotlib fig_size = (LARGEUR, HAUTEUR) ex: figsize = (10, 5)  # 10 = largeur (longueur) / 5 = hauteur
    dual_fig_size: tuple = (14, 6)               # (largeur, hauteur)
    single_fig_size: tuple = (7, 6) 
    cmap_test: str = "Blues"                # cmap test
    cmap_valid: str = "Purples"             # cmap validation