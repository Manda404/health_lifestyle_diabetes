# 📁 **Structure finale du projet avec commentaires**

```
health_lifestyle_diabetes/
│
├── pyproject.toml                 # Configurations du package (Poetry ou autre)
├── README.md                      # Documentation générale du projet
├── .gitignore                     # Gestion des fichiers à ignorer par Git
│
├── configs/                       # Fichiers de configuration (YAML)
│   ├── training.yaml              # Config d'entraînement ML
│   ├── inference.yaml             # Config d'inférence
│   └── logging.yaml               # Config du système de logs
│
├── tests/                         # Tests unitaires + end-to-end (E2E)
│   ├── domain/                    # Tests du domaine (entités, services, ports)
│   ├── application/               # Tests des use cases
│   ├── infrastructure/            # Tests des implémentations techniques
│   └── e2e/                       # Tests bout-à-bout simulant un workflow complet
│
└── src/
    └── health_lifestyle_diabetes/
        │
        ├── domain/                   # 1️⃣ Domaine = logique métier pure
        │   │                         # Aucune dépendance vers Pandas, Sklearn, Plotly, etc.
        │   │
        │   ├── entities/             # Objets métier = modèles du domaine
        │   │   ├── patient_profile.py       # Représentation stricte du profil patient
        │   │   ├── diabetes_prediction.py   # Sortie métier d’une prédiction
        │   │   └── features_schema.py       # Schéma métier des features attendues
        │   │
        │   ├── interfaces/           # Ports = contrats que l’infrastructure doit respecter
        │   │   ├── dataset_repository.py    # Interface générique pour charger/sauver un dataset
        │   │   └── model_repository.py      # Interface pour persister des modèles ML
        │   │
        │   └── services/             # Logique métier pure (sans dépendances externes)
        │       ├── feature_service.py       # Validation, normalisation métier des features
        │       └── prediction_service.py    # Règles métier de prédiction (hors ML)
        │
        ├── application/              # 2️⃣ Application = orchestration des cas d’usage
        │   │                         # Ne contient jamais de logique métier profonde
        │   │                         # Ne dépend que vers "domain" et "infrastructure"
        │   │
        │   ├── use_cases/            # Cas d’usage (actions du système)
        │   │   ├── perform_eda.py           # Cas d’usage : réaliser l’analyse EDA complète
        │   │   ├── train_model.py           # Cas d’usage : orchestrer l’entraînement modèle ML
        │   │   ├── evaluate_model.py        # Cas d’usage : orchestrer les évaluations du modèle
        │   │   ├── predict_patient.py       # Cas d’usage : prédiction sur un patient
        │   │   └── preprocess_dataset.py    # Cas d’usage : prétraitement des données brutes
        │   │
        │   └── dto/                  # DTO = structures d’entrée / sortie pour les use cases
        │       ├── training_config.py       # Paramètres d’entraînement (lr, depth, etc.)
        │       ├── prediction_request.py    # Format d’entrée pour la prédiction
        │       └── prediction_response.py   # Format de réponse pour la prédiction
        │
        ├── infrastructure/           # 3️⃣ Infrastructure = implémentations techniques
        │   │                         # Dépendances externes : Pandas, Sklearn, XGBoost, Plotly…
        │   │                         # ⚠️ Cette couche implémente les ports définis dans domain/interfaces
        │   │
        │   ├── data_sources/         # Sources de données physiques
        │   │   ├── csv_loader.py         # Chargement CSV brut → DataFrame
        │   │   └── local_storage.py      # Sauvegarde locale de fichiers (CSV, pickle…)
        │   │
        │   ├── repositories/         # Implémentations concrètes des ports
        │   │   ├── dataset_repository_impl.py   # Utilise csv_loader/local_storage
        │   │   └── model_repository_impl.py     # Sauvegarde / chargement des modèles ML
        │   │
        │   ├── ml/                   # Tout ce qui concerne le Machine Learning & Data Science
        │   │   │
        │   │   ├── preprocessors/           # Outils de preprocessing ML (encoders, scalers…)
        │   │   │   └── (OneHotEncoder, Scaler, etc.)
        │   │   │
        │   │   ├── eda/                    # 🔍 Exploratory Data Analysis (EDA)
        │   │   │   ├── dataset_summary.py      # Résumé dataset (manquants, cardinalité, types…)
        │   │   │   ├── numeric_analysis.py     # Analyse des variables numériques
        │   │   │   │                                # - distribution du risque
        │   │   │   │                                # - comparaison num vs target
        │   │   │   │                                # - analyse score de risque
        │   │   │   └── target_analysis.py       # Analyse de la variable cible
        │   │   │                                    # - distribution cible
        │   │   │                                    # - fréquences cumulées
        │   │   │
        │   │   ├── models/                  # Modèles ML concrets (XGBoost, CatBoost, LogReg…)
        │   │   │   ├── xgboost_model.py
        │   │   │   ├── catboost_model.py
        │   │   │   └── baseline_logreg.py
        │   │   │
        │   │   ├── pipelines/               # Pipelines ML complets (préprocess + modèle)
        │   │   │   └── diabetes_pipeline.py
        │   │   │
        │   │   └── metrics/                 # Métriques & évaluation des modèles
        │   │       └── evaluate_metrics.py  # AUC, F1, précision, rappel…
        │   │
        │   ├── utils/                       # Outils techniques généraux
        │   │   ├── logger.py                # Système de log unifié basé sur Loguru
        │   │   ├── config_loader.py         # Chargement des fichiers YAML
        │   │   └── exceptions.py            # Exceptions custom (DatasetError, ModelSavingError…)
        │
        ├── presentation/               # 4️⃣ Présentation = interfaces utilisateur
        │   ├── cli/                    # Command-line interface (scripts)
        │   │   ├── train.py            # Permet d’entraîner le modèle en CLI
        │   │   ├── evaluate.py         # Permet d’évaluer un modèle
        │   │   └── predict.py          # Permet de faire une prédiction via CLI
        │   │
        │   ├── api/                    # Application FastAPI (optionnel)
        │   │   └── fastapi_app.py      # Endpoints /predict, /train, etc.
        │   │
        │   └── streamlit/              # UI interactive pour la data science
        │       └── dashboard.py        # Dashboard complet : EDA + prédiction + visualisations
        │
        └── __init__.py
```

---

# 🧠 **Résumé des responsabilités par couche**

### **1️⃣ Domaine : Le cœur du métier**

* Pas de dépendance vers Pandas, Sklearn, XGBoost…
* Définit *ce que le système fait*, pas *comment*.
* Ports = interfaces que l'infrastructure doit implémenter.

### **2️⃣ Application : Orchestration**

* Coordonne les services du domaine + infrastructure.
* Contient les **use cases**.
* Utilise DTO pour échanger les données.

### **3️⃣ Infrastructure : Technologies**

* Code dépendant de libraries externes.
* Implémente les ports du domaine.
* Contient les modèles ML et pipelines.

### **4️⃣ Présentation : Interfaces utilisateur**

* CLI, API, Streamlit.
* Appelle les use cases.

---

## 2️⃣ Structure finale proposée pour *health_lifestyle_diabetes*

### 📁 Racine

```text
health_lifestyle_diabetes/
├── pyproject.toml
├── README.md
├── .gitignore
├── configs/
│   ├── training.yaml
│   ├── inference.yaml
│   ├── preprocessing.yaml
│   ├── logging.yaml
│   └── paths.yaml
├── tests/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── e2e/
└── src/
    └── health_lifestyle_diabetes/
        ├── domain/
        ├── application/
        ├── infrastructure/
        └── presentation/
```
