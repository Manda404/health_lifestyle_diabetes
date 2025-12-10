# 🎓 **COURS : L’ÉVALUATION DES MODÈLES DE CLASSIFICATION EN DATA SCIENCE**

## *La vérité sur les métriques dans le monde réel (datasets déséquilibrés)*

---

# 🧩 **INTRODUCTION : Pourquoi l’évaluation n’est pas une étape facultative**

Créer un modèle qui s’entraîne n’est **pas** suffisant.
Créer un modèle qui généralise **n’est toujours pas** suffisant.
Créer un modèle qui est performant **n’est encore pas suffisant**.

La seule vraie question en entreprise est :

> **Ton modèle prend-il de BONNES décisions dans le contexte métier ?**

Et cela dépend **entièrement** de l’évaluation.

L'évaluation te permet de :

* comprendre **où le modèle réussit**
* comprendre **où il échoue**
* savoir s'il est **robuste**
* savoir s'il est **digne d'être mis en production**
* savoir **le risque** associé à ses erreurs

Ce cours te donne **la boîte à outils complète**.

---

# 🧨 **PARTIE 1 — Les erreurs capitales que font les débutants**

### ❌ 1. Se fier à l’Accuracy

Dans un dataset déséquilibré :

* si 95% des gens ne sont pas malades,
* un modèle qui prédit toujours "pas malade"
* obtient **95% accuracy**

➡️ et pourtant il est **inutilisable**.

### ❌ 2. Regarder uniquement F1 ou Precision

Une métrique seule **ne raconte pas l’histoire complète**.

### ❌ 3. Ne pas analyser la calibration

Ton modèle peut être "bon" mais **inutilisable pour prendre des décisions** si ses probabilités ne sont pas fiables.

### ❌ 4. Ne pas analyser les FP et FN

Tu dois comprendre **la nature des erreurs**, pas seulement leur nombre.

---

# 📊 **PARTIE 2 — Les métriques indispensables en classification déséquilibrée**

On les regroupe en **4 familles**, chacune indispensable.

---

# 🅰️ FAMILLE 1 — MÉTRIQUES BASIQUES (mais obligatoires)

Objectif : vérifier la performance élémentaire du modèle.

## 1️⃣ Accuracy (⚠ à utiliser avec prudence)

### Pourquoi ?

Donne une première idée de la performance **globale**.

### Pourquoi elle est dangereuse ?

Dans les datasets déséquilibrés, elle devient **illusoire**.

👉 Toujours regarder **balanced accuracy** plutôt que accuracy.

---

## 2️⃣ Precision

[
Precision = \frac{TP}{TP + FP}
]

### Pourquoi elle est cruciale ?

* mesure combien de prédictions positives sont correctes
* utile si les faux positifs coûtent cher (fausse alerte médicale, fraude…)

### Quand l'utiliser ?

* si ton problème nécessite de **réduire les fausses alertes**

---

## 3️⃣ Recall (Sensitivity, TPR)

[
Recall = \frac{TP}{TP + FN}
]

### Pourquoi elle est cruciale ?

* mesure la capacité du modèle à **attraper la classe positive**
* indispensable en santé, assurance, fraude

### Quand l'utiliser ?

* si rater un positif est **grave**
  → diabète, cancer, fraude, défaut bancaire…

---

## 4️⃣ F1-score

[
F1 = 2 * \frac{Precision * Recall}{Precision + Recall}
]

### Pourquoi indispensable ?

* équilibre entre precision & recall
* bon choix lorsque tu veux optimiser **les deux** en même temps

### Attention :

* F1-score masque la réalité si les classes sont très déséquilibrées.

---

# 🅱️ FAMILLE 2 — MÉTRIQUES ADAPTÉES AUX DATASETS DÉSÉQUILIBRÉS

## 5️⃣ Balanced Accuracy

[
BA = \frac{Recall + Specificity}{2}
]

### Pourquoi indispensable ?

* corrige le biais de l’accuracy
* chaque classe compte **comme si elle était équilibrée**

### Quand l’utiliser ?

TOUJOURS lorsque ton dataset est déséquilibré.

---

## 6️⃣ Specificity (TNR)

[
Specificity = \frac{TN}{TN + FP}
]

### Pourquoi utile ?

* mesure la capacité à reconnaître les négatifs
* important pour éviter les faux positifs

---

## 7️⃣ FPR (False Positive Rate)

[
FPR = \frac{FP}{FP + TN}
]

### Pourquoi indispensable ?

* mesure la proportion de négatifs mal classés
* critique pour comprendre comment se comporte ton modèle lorsque la classe majoritaire prédomine

---

## 8️⃣ FNR (False Negative Rate)

[
FNR = \frac{FN}{FN + TP}
]

### Pourquoi indispensable ?

* un modèle peut être "excellent" mais rater énormément la classe minoritaire
* FNR est critique → les FN sont **les erreurs les plus dangereuses**

### Exemple :

Rater un diabétique → conséquence grave.

---

# 🅾️ FAMILLE 3 — MÉTRIQUES AVANCÉES POUR DATASETS DÉSÉQUILIBRÉS

## 9️⃣ MCC — **Matthews Correlation Coefficient**

[
MCC = \frac{TP · TN - FP · FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}
]

### Pourquoi c’est la métrique préférée des experts ?

* tient compte **de toutes les cellules** de la matrice de confusion
* robuste aux distributions déséquilibrées
* impossible à manipuler
* score global **stable**, contrairement à F1, Accuracy…

### Interprétation :

* 1 → parfait
* 0 → hasard
* < 0 → pire que hasard

➡️ MCC est **la métrique la plus fiable en classification binaire**.

---

## 🔟 Cohen's Kappa

[
\kappa = \frac{P_o - P_e}{1 - P_e}
]

### Pourquoi pertinent ?

* mesure l’accord modèle ↔ réalité **en tenant compte du hasard**
* excellent pour évaluer un modèle dans des milieux où les classes minoritaires importent

### Pourquoi moins utilisé que MCC ?

* un peu instable quand la prévalence change
* MCC donne souvent une mesure plus fidèle

➡️ Mais Kappa reste **essentiel pour un audit complet**.

---

# 🅿️ FAMILLE 4 — MÉTRIQUES BASÉES SUR LES PROBABILITÉS

## 1️⃣1️⃣ AUC-ROC

### Pourquoi utile ?

* mesure la capacité du modèle à séparer les classes **à tous les seuils**
* très utilisé en compétition & recherche

### Limite :

* peut être **trompeuse** en cas de dataset très déséquilibré

---

## 1️⃣2️⃣ AUC Precision-Recall

### Pourquoi cruciale en dataset déséquilibré ?

* la PR-AUC se concentre uniquement sur la classe positive
* beaucoup plus informative que ROC-AUC dans ton contexte

➡️ **Une des métriques les plus importantes dans ton cas.**

---

## 1️⃣3️⃣ Brier Score

[
BS = \frac{1}{N}\sum (y_i - p_i)^2
]

### Pourquoi indispensable ?

* mesure la **calibration** des probabilités
* essentiel en assurance, santé, scoring de risque

### Exemple :

Un modèle peut être bon en classification, mais **donner des probabilités inutilisables**.

---

## 1️⃣4️⃣ Calibration Curve (et ECE si avancé)

### Pourquoi indispensable ?

* vérifie si le modèle est **fiable quand il donne une probabilité**
* si il prédit 0.7 → doit être vrai 70% du temps

---

# 🎯 **PARTIE 3 — Quelle métrique utiliser et quand ? (TABLEAU PRATIQUE)**

| Scénario                          | Métrique(s) clé                |
| --------------------------------- | ------------------------------ |
| Dataset déséquilibré              | MCC, Balanced Accuracy, PR-AUC |
| Rater un positif est grave        | Recall, FNR                    |
| Faux positifs coûteux             | Precision, FPR                 |
| Analyse globale robuste           | MCC, ROC-AUC                   |
| Décisions basées sur probabilités | Brier Score, Calibration curve |
| Comparaison entre modèles         | ROC-AUC + PR-AUC + MCC         |

---

# 🧠 **PARTIE 4 — La stratégie d’évaluation d’un Data Scientist confirmé**

Un expert ne regarde pas "une métrique".
Il regarde un **ensemble de métriques**, et surtout **leur cohérence entre elles**.

### ✔ 1. Toujours regarder MCC

MCC est le premier indicateur de robustesse.

### ✔ 2. Ensuite regarder Recall, Precision, FNR, FPR

→ comprendre la nature des erreurs.

### ✔ 3. Ensuite PR-AUC

→ qualité de détection de la classe minoritaire.

### ✔ 4. Ensuite Brier Score + calibration

→ qualité des probabilités.

### ✔ 5. Ensuite les plots de probas

→ comprendre comment le modèle pense.

**C’est ça, l’évaluation professionnelle.**

---

# 🏁 **CONCLUSION DU COURS : Les métriques que tu dois ABSOLUMENT maîtriser**

### 🔥 Les indispensables (à regarder systématiquement)

* **MCC**
* **PR-AUC**
* **Recall**
* **Precision**
* **F1**
* **Balanced Accuracy**
* **FNR / FPR**
* **Brier Score**
* **Calibration Curve**

### 🔥 Les secondaires mais très utiles

* **ROC-AUC**
* **Specificity**
* **Kappa**

### 🔥 Les pièges

* Accuracy seule
* F1 seul
* ROC-AUC seul
* regarder aucune métrique de calibration

---