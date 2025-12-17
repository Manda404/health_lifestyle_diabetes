
---

# ⚕️ Health & Lifestyle Diabetes Prediction

**Un projet Machine Learning pédagogique basé sur la Clean Architecture et les bonnes pratiques MLOps**

---

## 📌 Présentation du projet

Ce projet est un **système de Machine Learning dédié à la prédiction du diabète**, construit avec une forte orientation **Clean Architecture appliquée aux projets de Data Science**.

L’objectif de ce dépôt **n’est pas** de proposer un simple projet de modélisation ou un notebook expérimental, mais de montrer **comment concevoir, structurer et organiser un projet de Machine Learning de manière professionnelle**, en respectant des principes d’architecture logicielle utilisés en entreprise.

Le projet s’appuie sur un jeu de données **santé & mode de vie**, mais la **véritable valeur ajoutée** réside dans la **structure du code**, la **séparation des responsabilités**, et la **vision MLOps** adoptée tout au long du projet.

---

## 🎯 Objectifs pédagogiques

Les objectifs principaux de ce projet sont les suivants :

* ✅ Appliquer les **principes de la Clean Architecture** à un projet de Data Science
* ✅ Montrer comment structurer un projet ML de manière claire et maintenable
* ✅ Séparer proprement :

  * la logique métier
  * la logique Machine Learning
  * les aspects techniques et d’infrastructure
* ✅ Illustrer un **workflow de Machine Learning Engineer** proche des standards industriels
* ✅ Mettre en œuvre les **bonnes pratiques MLOps** (CI/CD, tracking, configuration, API)

D’un point de vue modélisation, le projet traite :

* la **classification binaire** (diabète / non-diabète)
* la **classification multi-classes** (stades du diabète)
* l’**estimation de risque** à partir d’indicateurs de santé et de mode de vie

---

## 🏗️ Approche architecturale

Ce projet est structuré selon les principes de la **Clean Architecture**, adaptés aux **projets de Data Science et de Machine Learning**.

L’idée centrale est de **séparer clairement ce que fait le système** de **la manière dont il est implémenté**, afin de construire un code :

* plus lisible
* plus testable
* plus évolutif
* plus proche des exigences de la production

### Pourquoi appliquer la Clean Architecture en Data Science ?

Dans de nombreux projets ML, on observe rapidement les problèmes suivants :

* les notebooks deviennent difficiles à maintenir
* le chargement des données, le preprocessing, les modèles et les API sont mélangés
* changer de modèle ou de source de données casse une grande partie du code

La Clean Architecture permet d’éviter ces écueils en imposant :

* une **séparation forte des responsabilités**
* une **inversion des dépendances**
* une distinction claire entre :

  * le cœur métier
  * les cas d’usage
  * l’infrastructure technique
  * les interfaces d’exposition

---

### 🧱 Vue d’ensemble de la Clean Architecture

👉 **C’est ici que tu peux insérer l’image de la Clean Architecture** :

```md
![Schéma de la Clean Architecture](note/clean-architecture.png)
```

> Ce schéma illustre comment les principes de la Clean Architecture sont appliqués pour structurer un système de Machine Learning.

---

### 🧠 Architecture logique (simplifiée)

```
presentation  →  application  →  domain
        ↑                ↑
        └──── infrastructure ─┘
```

Chaque couche a un rôle bien défini :

* **Domain**
  Contient les concepts métier et les interfaces.
  Cette couche ne dépend d’aucune technologie (pas de pandas, pas de modèles ML).

* **Application**
  Définit les cas d’usage : entraînement, évaluation, prédiction.
  Elle orchestre le workflow sans connaître les détails techniques.

* **Infrastructure**
  Contient les implémentations concrètes :

  * chargement des données
  * preprocessing
  * modèles de Machine Learning
  * tracking des expériences
  * outils techniques

* **Presentation**
  Expose le système via :

  * une API (FastAPI)
  * une CLI
  * un dashboard

Toutes les dépendances **pointent vers l’intérieur**, garantissant la stabilité du cœur du système.

---

## 📁 Structure du projet (simplifiée)

```
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

Cette organisation permet de conserver un projet :

* clair
* testable
* modulaire
* prêt pour des usages industriels

---

## 🤖 Machine Learning & pratiques MLOps

Ce projet illustre comment le Machine Learning **s’intègre naturellement dans une architecture propre**.

### 🔹 Modèles de Machine Learning

Les modèles utilisés sont principalement des **modèles de boosting**, particulièrement adaptés aux données tabulaires :

* Gradient Boosting
* XGBoost
* CatBoost

Ces modèles sont entièrement encapsulés dans la couche *infrastructure*, ce qui les rend **facilement interchangeables** sans impacter le reste du système.

---

### 🔹 Suivi des expérimentations

* **MLflow** est utilisé pour :

  * le suivi des expériences
  * l’enregistrement des métriques
  * la gestion des versions de modèles

Cela permet d’illustrer concrètement les notions de **traçabilité** et de **reproductibilité**.

---

### 🔹 Configuration orientée métier

* Les paramètres sont définis via des fichiers **YAML**
* Aucun hyperparamètre n’est codé en dur
* Les expérimentations sont reproductibles et contrôlées

---

### 🔹 CI/CD et qualité du code

* Des pipelines **GitHub Actions** sont mis en place pour :

  * exécuter les tests
  * vérifier la qualité du code
  * valider la structure du projet

Cela montre comment appliquer des pratiques DevOps à des projets de Data Science.

---

### 🔹 Inférence via API

* **FastAPI** est utilisé pour exposer les prédictions
* L’API est totalement découplée de la logique ML
* Cette approche illustre les bonnes pratiques de déploiement de modèles en production

---

## 🧪 Technologies utilisées

### Stack principale

* **Python**
* **Poetry** (gestion des dépendances et du packaging)

### Data Science & Machine Learning

* Pandas
* NumPy
* Scikit-learn
* XGBoost
* CatBoost

### MLOps & ingénierie

* MLflow
* FastAPI
* GitHub Actions (CI/CD)
* Configuration YAML
* Logging structuré et gestion des erreurs

---

## 🎓 Objectif pédagogique du projet

Ce dépôt a avant tout une **vocation pédagogique**.

Il vise à montrer :

* comment appliquer la **Clean Architecture à la Data Science**
* comment dépasser une approche uniquement basée sur des notebooks
* comment structurer un projet ML pour le long terme
* comment raisonner en **Machine Learning Engineer**, et non uniquement en data scientist expérimental

Ce projet n’est pas pensé comme un package prêt à l’emploi, mais comme une **référence de bonnes pratiques**.

---

## 👤 Auteur

**Rostand Surel**
📧 [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)

---

## ⭐ Note finale

Ce projet reflète ma vision des projets de Machine Learning :

* une architecture claire et robuste
* une séparation stricte des responsabilités
* des workflows reproductibles
* une approche orientée production

Il constitue une **base pédagogique** pour comprendre comment concevoir des projets de Data Science modernes et maintenables en appliquant la Clean Architecture.

---