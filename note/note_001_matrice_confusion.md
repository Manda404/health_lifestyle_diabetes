📘 COURS : Normalisation d’une Matrice de Confusion

🎯 Objectif

Comprendre comment interpréter correctement une matrice de confusion suivant le type de normalisation choisi, et quel KPI chaque méthode met en lumière.

⸻

1️⃣ Rappel : Matrice de Confusion

Une matrice de confusion est un tableau qui résume les performances d’un modèle de classification.

	Prédits = Chat	Prédits = Chien	Prédits = Lapin
Vrais Chats	TP	FP (Chat → Chien)	FP
Vrais Chiens	FN (Chien → Chat)	TP	FP
Vrais Lapins	FN	FN	TP

👉 La diagonale représente les bonnes prédictions (True Positive).
👉 Hors diagonale = erreurs de classification (confusions).

⸻

2️⃣ Pourquoi normaliser ?

Sans normalisation → risques d’erreurs d’interprétation 🚨

Si une classe a beaucoup plus d’exemples, elle dominera la matrice.

Exemple :
	•	Classe A : 10 000 exemples
	•	Classe B : 30 exemples

➡️ Sans normalisation, les erreurs de B seront invisibles 😨
➡️ La normalisation permet de ramener les classes à la même échelle.

⸻

3️⃣ Les 4 normalisations standard (scikit-learn)

📌 1. Aucune normalisation
	•	Valeurs brutes
	•	On observe les volumes réels
	•	Utile pour détecter les déséquilibres de classes

⸻

📌 2. Normalisation par ligne (row)

Division par : total des vrais exemples (ligne)

CM_{norm}(i,j) = \frac{CM(i,j)}{\sum_j CM(i,j)}

➡️ Chaque ligne = 100% des vrais X

Cette normalisation calcule en fait le Recall / Sensibilité par classe.

Interprétation

Parmi tous les vrais X, combien sont bien ou mal prédits ?

⸻

📌 3. Normalisation par colonne (pred)

Division par : total des prédictions de la classe (colonne)

CM_{norm}(i,j) = \frac{CM(i,j)}{\sum_i CM(i,j)}

➡️ Chaque colonne = 100% des prédictions Y

Cette normalisation mesure la Précision par classe.

Interprétation

Quand le modèle prédit Y, est-il fiable ?

⸻

📌 4. Normalisation globale (all)

Division par : total des observations

Tout devient des pourcentages globaux.

Interprétation

Quelle proportion du dataset total se trouve dans chaque case ?

✔️ Simple, bonne vue d’ensemble
❌ Peut masquer les erreurs de petites classes

⸻

4️⃣ ⭐ Méthode BONUS (non standard)

✨ Normalisation diagonale (ta demande)

Cette méthode divise chaque ligne par la valeur diagonale de la classe (TP).

CM_{norm}(i,j) = \frac{CM(i,j)}{CM(i,i)}

📌 Objectif : comprendre l’importance des erreurs par rapport aux réussites

Interprétation

Pour 1 bonne prédiction, combien d’erreurs ?
Quel type de confusion est le plus dangereux ?

⸻

5️⃣ 🧠 Lien avec les métriques classiques

Normalisation	KPI équivalent
Ligne (row)	Recall
Colonne (pred)	Précision
Globale (all)	Accuracy (vue mélangée)
Aucune	Comptage brut
Diagonale	Poids des erreurs / Succès (non standard)


⸻

6️⃣ 📊 Tableau comparatif demandé

Méthode de normalisation	Division par	KPI mesuré	Interprétation	Quand l’utiliser
Aucune (valeurs brutes)	rien	—	volume réel des erreurs / succès	Diagnostiquer le déséquilibre de classes, comprendre les quantités
Ligne (row) ✔️ ta méthode actuelle	total de la classe réelle (somme ligne)	Recall / Sensibilité	Parmi tous les vrais X, combien bien/mal prédits ?	Dataset déséquilibré, évaluer qualité par classe
Colonne (pred)	total des prédictions de la colonne	Précision	Quand je prédis Y, suis-je fiable ?	Éviter les faux positifs, décisions sensibles (médecine, assurance fraude, sécurité)
Globale (all)	total global	% du dataset	Vue d’ensemble de la performance	Communication simple, rapport exécutif / board
Diagonale 🔥 non standard	vrai positif (élément diagonal)	Erreur relative au succès	Par rapport au bon classement, combien d’erreurs ?	Comprendre les confusions principales, tuning, diagnostic fin


⸻

7️⃣ 🏁 Résumé à retenir absolument

Si tu veux évaluer…	Alors utilise…
La qualité par classe	Normalisation ligne
La fiabilité des prédictions	Normalisation colonne
La performance globale	Normalisation globale
Le volume réel	Aucune
Les erreurs critiques par rapport aux succès	Diagonale


⸻

🎉 Conclusion finale

La normalisation d’une matrice de confusion change l’angle d’analyse :

📌 On ne change pas les données, on change la façon de les lire.

👉 C’est un outil stratégique pour comprendre un modèle,
👉 surtout dans des contextes professionnels à fort enjeu (banque, assurance, santé, fraude, industrie).

⸻