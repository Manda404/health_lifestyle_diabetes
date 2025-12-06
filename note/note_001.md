# 🧠 ⭐ Qu’est-ce que la Clean Architecture ?

La **Clean Architecture** est une manière d’organiser ton code pour obtenir :

* un projet **maintenable**
* **facile à faire évoluer**
* **testable**
* **robuste**
* où les changements à l’extérieur (modèle ML, format CSV, API, Framework...) **n’impactent pas ton cœur métier**

En résumé :

> **Séparer ce qui est stable (le métier) de ce qui change souvent (la technologie).**

---

# 🏛️ Le principe fondamental : les cercles concentriques

Voici le schéma de base de la Clean Architecture :

```
         +-------------------------------+
         |         Presentation          |
         +-------------------------------+
                   ↓         ↑
         +-------------------------------+
         |         Application           |
         +-------------------------------+
                   ↓         ↑
         +-------------------------------+
         |            Domain             |
         +-------------------------------+
                   ↑
         +-------------------------------+
         |        Infrastructure         |
         +-------------------------------+
```

## Le **sens des dépendances est sacré :**

➡️ **Tout pointe vers le Domain.**
➡️ Le Domain ne dépend **d’aucune autre couche**.
➡️ L'infrastructure dépend du Domain, mais jamais l'inverse.

C’est la clé pour avoir un projet propre, solide et déployable partout.

---

# 🔍 Les 4 couches et leurs rôles

## 🟣 1. DOMAIN (le cœur métier)

**La partie la plus importante.**

Ce qu’on y met :

* Les **entités métier** (PatientProfile, DiabetesStage…)
* Les **interfaces** (DatasetRepository, ModelRepository…)
* Les **règles métier** pures
* AUCUNE technologie :
  ❌ pas de pandas
  ❌ pas de sklearn
  ❌ pas de fastapi
  ❌ pas de streamlit
  ❌ pas de fichiers CSV

C’est la couche **stable** : elle change rarement.

👉 Exemple orienté Data Science :
Le concept d’un *Patient*, d’un *DiabetesTarget*, d’une *feature vector*, ne dépend pas du format CSV ou du modèle XGBoost.

---

## 🔵 2. APPLICATION (Use Cases)

Ici on définit **ce que le système doit faire**.

Exemples :

* `preprocess_dataset.py`
* `train_model.py`
* `evaluate_model.py`
* `predict_patient.py`

Cette couche utilise **le domaine** mais ne connaît **pas l’infrastructure**.

Elle ne dit pas *comment* les données sont chargées, seulement *qu'elle doit être chargée*.

Exemple :

```python
df = dataset_repository.load_raw()
```

🎯 Le Use Case dit **quoi faire**, pas **comment le faire**.

---

## 🟢 3. INFRASTRUCTURE (le technique)

C’est ici qu’on met :

* Pandas
* Scikit-Learn
* XGBoost / CatBoost
* FastAPI
* Pickle
* CSV I/O
* Preprocessors
* Pipelines ML

Cette couche **implémente les interfaces du Domain**.

Exemple (infrastructure) :

```python
class CSVLoader(DatasetRepository):
    def load_raw(self):
        return pd.read_csv("data/input/diabetes.csv")
```

Le Use Case ne voit jamais Pandas.
Il voit juste `DatasetRepository`.

---

## 🔴 4. PRESENTATION (interfaces utilisateur)

On met ici :

* CLI : `train.py`, `predict.py`
* API FastAPI
* Dashboard Streamlit
* Notebooks (optionnel)

Ces scripts **appellent les Use Cases**, jamais les modèles ML directement.

Exemple (CLI) :

```python
use_case = TrainModelUseCase(dataset_repo, model_repo, preprocessing_service)
result = use_case.execute()
```

➡️ Le CLI ne contient **aucune logique métier**, juste *l’orchestration IO*.

---

# 🎯 Pourquoi la Clean Architecture est ESSENTIELLE pour la Data Science ?

## **1. Tu peux changer le modèle ML quand tu veux**

Aujourd’hui XGBoost, demain CatBoost, après-demain LightGBM :
➡️ Aucun fichier hors infrastructure ne change.

## **2. Tu peux remplacer le CSV par une base SQL**

➡️ Il suffit de changer l'implémentation du repository.

## **3. Tu peux déployer en API, CLI ou Streamlit**

➡️ Sans toucher au cœur métier.

## **4. Tu peux écrire des tests unitaires sans ML**

➡️ Le Domain et les Use Cases sont 100% testables.

## **5. C’est indispensable pour l’industrie**

AXA, Safran, Airbus, BNP, MAIF, Google utilisent ces principes pour :

* pipelines ML
* modèles en production
* projets long terme

---

# 🔥 Exemple ultra concret de Clean Architecture dans TON projet

Imaginons ton **Use Case** veut entraîner un modèle :

```python
class TrainModelUseCase:

    def __init__(self, dataset_repo, model_repo, preprocessing_service):
        self.dataset_repo = dataset_repo
        self.model_repo = model_repo
        self.preprocessing_service = preprocessing_service

    def execute(self, config):
        df = self.dataset_repo.load_raw()
        X_train, X_test, y_train, y_test = self.preprocessing_service.split_train_test(df)

        model = DiabetesPipeline(config)
        model.train(X_train, y_train)

        metrics = model.evaluate(X_test, y_test)
        self.model_repo.save_model(model, "diabetes-model.pkl")

        return metrics
```

Ce Use Case :

* ne connaît pas Pandas
* ne connaît pas XGBoost
* ne connaît pas CSV
* ne connaît pas pickle
* ne connaît pas l’API
* ne connaît pas Streamlit

Il est **purement métier**, **stable**, **testable**, **professionnel**.

---

# 🧩 Vision magique de Clean Architecture

> **L'extérieur peut changer autant qu'il veut, l’intérieur reste propre.**

En Data Science :

* tu changes de dataset → pas de problème
* tu ajoutes de nouvelles features → tout reste cohérent
* tu remplaces le modèle → l’architecture tient
* tu changes de framework → rien ne casse

C’est exactement ce qu’on attend d’un **projet ML prêt pour la production**.

---

# 🎓 Résumé pédagogique

| Couche             | Ce qu’elle contient                        | Ce qu’elle ne doit pas contenir |
| ------------------ | ------------------------------------------ | ------------------------------- |
| **Domain**         | Entités, interfaces, règles métier         | Pandas, sklearn, ML             |
| **Application**    | Use Cases                                  | Implémentations techniques      |
| **Infrastructure** | Modèles ML, Pandas, SQLite, CSV, pipelines | Règles métier                   |
| **Presentation**   | API, CLI, dashboard                        | Logique métier, ML direct       |

➡️ **Les dépendances vont TOUJOURS vers le Domain.**

---

# 🚀 Prêt pour la suite ?

Je peux maintenant t’aider avec :

### 🔹 une **visualisation graphique** de la Clean Architecture

### 🔹 un **exemple complet de A à Z**

### 🔹 l'implémentation progressive **de chaque couche**

### 🔹 un **diagramme UML** de ton projet

### 🔹 la **mise en place des premiers fichiers réels**

Souhaites-tu maintenant :

**A. Une version illustrée très visuelle ?**
**B. Une explication encore plus simplifiée ?**
**C. Un exemple complet appliqué à TON architecture ?**
**D. Qu’on commence à coder la première couche (Domain) ?**
