# src/health_lifestyle_diabetes/infrastructure/metrics/sklearn_metrics_adapter.py

from typing import Dict, Sequence

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    cohen_kappa_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)

from health_lifestyle_diabetes.domain.ports.metrics_port import MetricsPort


class SklearnMetricsAdapter(MetricsPort):
    """
    Adaptateur d'Infrastructure implémentant le MetricsPort du Domaine.

    Rôle :
    ------
    Traduit l'appel abstrait de calcul de métriques (demandé par le Domaine)
    en appels concrets à la librairie technique scikit-learn.

    Ceci garantit que la logique d'évaluation du Domaine reste complètement
    découplée de la dépendance à sklearn.
    """

    def compute_metrics(
        self,
        y_true: Sequence[int],
        y_pred: Sequence[int],
        y_proba: Sequence[float],
    ) -> Dict[str, float]:
        """
        Calcule un ensemble standard de métriques de classification pour un rapport complet.

        Cette méthode prend les séquences d'entrée, les convertit en tableaux
        Numpy, puis utilise les fonctions appropriées de sklearn pour calculer
        toutes les métriques requises par le Port.

        Args:
            y_true (Sequence[int]): Les labels réels (vérité terrain), souvent 0 ou 1.
            y_pred (Sequence[int]): Les labels prédits par le modèle après seuillage (thresholding).
            y_proba (Sequence[float]): Les probabilités (scores) prédites par le modèle.

        Returns:
            Dict[str, float]: Un dictionnaire contenant les métriques calculées.

            Exemple de contenu:
            {
                "accuracy": 0.8900,
                "f1": 0.8450,
                "auc_roc": 0.9210,
                "kappa": 0.6105,
                "mcc": 0.7000,
                "recall": 0.7800,
                "precision": 0.9100,
            }

        Raises:
            ValueError/TypeError: Peut lever des exceptions si les séquences
                                  ne sont pas compatibles ou sont vides (issues de sklearn).
        """

        # 1. Conversion des formats (séquences Python vers tableaux Numpy)
        y_true_arr = np.array(y_true)
        y_pred_arr = np.array(y_pred)
        y_proba_arr = np.array(y_proba)

        # 2. Calcul des métriques (Métriques basées sur y_pred)
        accuracy = accuracy_score(y_true_arr, y_pred_arr)
        precision = precision_score(
            y_true_arr, y_pred_arr, zero_division=0
        )  # zero_division pour gérer les cas sans prédictions positives
        recall = recall_score(y_true_arr, y_pred_arr, zero_division=0)
        f1 = f1_score(y_true_arr, y_pred_arr, zero_division=0)
        kappa = cohen_kappa_score(y_true_arr, y_pred_arr)
        mcc = matthews_corrcoef(y_true_arr, y_pred_arr)

        # 3. Calcul des métriques (Métriques basées sur y_proba)
        auc_roc = roc_auc_score(y_true_arr, y_proba_arr)
        auc_pr = average_precision_score(y_true_arr, y_proba_arr)

        # 4. Formatage et Retour (Rapport complet)
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "auc_roc": round(auc_roc, 4),
            "auc_pr": round(auc_pr, 4),
            "kappa": round(kappa, 4),
            "mcc": round(mcc, 4),
        }
