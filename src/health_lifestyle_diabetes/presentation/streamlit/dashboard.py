import streamlit as st
#from loguru import logger
import pandas as pd

#from health_lifestyle_diabetes.application.use_cases.predict_patient import PredictPatientUseCase
#from health_lifestyle_diabetes.infrastructure.repositories.model_repository_impl import ModelRepositoryImpl
#from health_lifestyle_diabetes.infrastructure.repositories.dataset_repository_impl import DatasetRepositoryImpl
#from health_lifestyle_diabetes.application.dto.prediction_request import PredictionRequestDTO


# Initialisation repositories
#model_repo = ModelRepositoryImpl()
#dataset_repo = DatasetRepositoryImpl()


# ---------------------------
#       UI CONFIG
# ---------------------------
st.set_page_config(
    page_title="Health Lifestyle Diabetes Dashboard",
    layout="wide"
)


# ---------------------------
#       SIDEBAR MENU
# ---------------------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Accueil", "🔍 EDA", "🤖 Prédiction", "📈 Monitoring"]
)


# ---------------------------
#       ACCUEIL
# ---------------------------
if menu == "🏠 Accueil":
    st.title("Dashboard — Prédiction de Diabète")
    st.write("""
        Bienvenue dans l'application Streamlit du projet Health Lifestyle Diabetes.
        - Visualisez les données (EDA)
        - Faites une prédiction individuelle
        - Surveillez les performances du modèle
    """)


# ---------------------------
#       EDA
# ---------------------------
elif menu == "🔍 EDA":
    st.title("Exploratory Data Analysis")
    
    #df = dataset_repo.load_dataset()

    #st.subheader("Aperçu du dataset")
    #st.dataframe(df.head())

    #st.subheader("Statistiques descriptives")
    #st.dataframe(df.describe())

    #st.subheader("Distribution de la cible")
    #st.bar_chart(df["diagnosed_diabetes"].value_counts())


# ---------------------------
#     PRÉDICTION PATIENT
# ---------------------------
elif menu == "🤖 Prédiction":

    st.title("Prédiction individuelle")

    age = st.slider("Âge", 18, 90, 45)
    bmi = st.number_input("IMC (BMI)", 10.0, 60.0, 25.0)
    glucose = st.number_input("Glucose", 50.0, 250.0, 110.0)
    physical_activity = st.slider("Activité physique (0–1)", 0.0, 1.0, 0.3)
    """
    if st.button("Prédire"):
        dto = PredictionRequestDTO(
            age=age,
            bmi=bmi,
            glucose=glucose,
            physical_activity=physical_activity
        )

        use_case = PredictPatientUseCase(model_repo=model_repo)
        result = use_case.execute(dto)

        st.success(f"Probabilité de diabète : {result.proba:.2f}")
        st.info(f"Classe prédite : {result.label}")
    """

# ---------------------------
#     MONITORING
# ---------------------------
elif menu == "📈 Monitoring":
    st.title("Performances du modèle")
    st.write("🚧 Fonction en cours : intégration des métriques, confusion matrix, historique du training…")
