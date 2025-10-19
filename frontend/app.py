# app.py - FICHIER PRINCIPAL AVEC NAVIGATION
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Détection de Fraudes",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🔍 Détecteur de Fraudes Bancaires</h1>', 
            unsafe_allow_html=True)

# Sidebar avec navigation
with st.sidebar:
    st.title("Navigation")
    st.markdown("---")
    
    # Menu de navigation
    page = st.radio(
        "Choisir une page :",
        ["🏠 Accueil", "📝 Prédire une transaction"]
    )
    
    st.markdown("---")
    st.info("""
    **Projet IA 2024-2025**
    Système de détection de fraudes
    utilisant le Machine Learning
    """)

# Navigation entre pages
if page == "🏠 Accueil":
    st.switch_page("pages/Accueil.py")
elif page == "📝 Prédire une transaction":
    st.switch_page("pages/Prediction.py")