# app.py - INTERFACE MODERNE SANS "ACCUEIL"
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="FraudShield - Détection Intelligente",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PERSONNALISÉ MODERNE
st.markdown("""
<style>
    /* Styles généraux */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        font-size: 3.5rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #f8f9fa;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Cartes modernes */
    .modern-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .mission-card {
        background: linear-gradient(135deg, #1a237e, #000051);
        color: white;
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    
    /* Boutons modernes */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Navigation */
    .nav-container {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    /* Texte mission */
    .mission-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .mission-subtitle {
        font-size: 1.8rem;
        font-weight: 300;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .mission-text {
        font-size: 1.2rem;
        line-height: 1.6;
        opacity: 0.8;
        max-width: 800px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# HEADER HÉROÏQUE
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<h1 class="main-header">🛡️ FraudShield</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Détection Intelligente de Fraudes Financières</p>', unsafe_allow_html=True)

# NAVIGATION MODERNE
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("📊 Tableau de Bord", use_container_width=True):
        st.session_state.page = "dashboard"

with nav_col2:
    if st.button("🔍 Analyser", use_container_width=True):
        st.session_state.page = "analyze"

with nav_col3:
    if st.button("📈 Statistiques", use_container_width=True):
        st.session_state.page = "stats"

st.markdown('</div>', unsafe_allow_html=True)

# SECTION NOTRE MISSION - CENTRÉE ET MODERNE
st.markdown("""
<div class="mission-card">
    <div class="mission-title">Notre Mission</div>
    <div class="mission-subtitle">Protection Financière Intelligente</div>
    <div class="mission-text">
        Nous nous engageons à protéger chaque transaction financière grâce à l'intelligence artificielle de pointe, 
        en détectant et prévenant les fraudes en temps réel pour assurer la sécurité de votre business.
    </div>
</div>
""", unsafe_allow_html=True)

# CONTENU PRINCIPAL
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

if st.session_state.page == "dashboard":
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("## 📊 **Tableau de Bord en Temps Réel**")
    
    # Métriques en temps réel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Transactions Aujourd'hui", "1,247", "+5.2%")
    
    with col2:
        st.metric("Fraudes Détectées", "8", "-2.1%")
    
    with col3:
        st.metric("Taux de Détection", "99.1%", "+0.3%")
    
    with col4:
        st.metric("Temps Moyen", "47ms", "-3ms")
    
    # Graphiques du tableau de bord
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📅 Activité des 7 derniers jours")
        daily_data = pd.DataFrame({
            'Jour': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            'Transactions': [1150, 1240, 1180, 1320, 1247, 980, 760],
            'Alertes': [12, 8, 15, 9, 8, 5, 3]
        })
        
        fig_daily = px.line(daily_data, x='Jour', y=['Transactions', 'Alertes'],
                           title='Activité Quotidienne')
        st.plotly_chart(fig_daily, use_container_width=True)
    
    with col_chart2:
        st.subheader("🎯 Répartition des Risques")
        risk_data = pd.DataFrame({
            'Niveau': ['Faible', 'Moyen', 'Élevé', 'Critique'],
            'Pourcentage': [65, 25, 8, 2]
        })
        
        fig_risk = px.pie(risk_data, values='Pourcentage', names='Niveau',
                         title='Distribution des Niveaux de Risque')
        st.plotly_chart(fig_risk, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "analyze":
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("## 🔍 **Analyse de Transaction**")
    
    # Formulaire moderne
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💳 Informations Transaction")
            montant = st.number_input("Montant (€)", min_value=0.0, value=150.0, step=10.0)
            categorie = st.selectbox("Catégorie", ["Retail", "E-commerce", "Services", "Voyage", "International"])
            heure = st.slider("Heure de transaction", 0, 23, 14)
            methode_paiement = st.selectbox("Méthode de paiement", ["Carte", "Virement", "Mobile", "En ligne"])
        
        with col2:
            st.subheader("👤 Profil Client")
            age = st.number_input("Âge", min_value=18, max_value=100, value=35)
            localisation = st.selectbox("Localisation", ["France", "UE", "International", "Zone à risque"])
            historique = st.selectbox("Historique Client", ["Nouveau", "Occasionnel", "Régulier", "VIP"])
            device = st.selectbox("Appareil", ["Mobile connu", "Nouveau mobile", "Ordinateur", "Inconnu"])
        
        soumettre = st.form_submit_button("🚀 Analyser la Transaction", use_container_width=True)
        
        if soumettre:
            with st.spinner("🔍 Analyse en cours..."):
                # Simulation d'analyse IA
                import random
                risque_score = random.randint(1, 100)
                
                if risque_score > 70:
                    st.error("### ⚠️ Transaction à Risque Élevé")
                    col_risk1, col_risk2 = st.columns(2)
                    with col_risk1:
                        st.metric("Score de Risque", f"{risque_score}%", delta="Élevé", delta_color="inverse")
                    with col_risk2:
                        st.metric("Recommandation", "Bloquer", delta="Action requise")
                    
                    st.warning("**Facteurs de risque détectés:** Montant élevé, Localisation suspecte, Nouvel appareil")
                    
                elif risque_score > 30:
                    st.warning("### 🔄 Transaction à Risque Moyen")
                    col_risk1, col_risk2 = st.columns(2)
                    with col_risk1:
                        st.metric("Score de Risque", f"{risque_score}%", delta="Moyen")
                    with col_risk2:
                        st.metric("Recommandation", "Vérifier", delta="Surveillance")
                    
                    st.info("**Recommandation:** Vérification d'identité recommandée")
                    
                else:
                    st.success("### ✅ Transaction Sécurisée")
                    col_risk1, col_risk2 = st.columns(2)
                    with col_risk1:
                        st.metric("Score de Risque", f"{risque_score}%", delta="Faible")
                    with col_risk2:
                        st.metric("Recommandation", "Approuver", delta="Sécurisée")
                    
                    st.info("**Statut:** Transaction conforme aux habitudes du client")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "stats":
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("## 📈 **Statistiques et Analytics**")
    
    # Graphiques statistiques
    col_stat1, col_stat2 = st.columns(2)
    
    with col_stat1:
        st.subheader("📅 Activité Mensuelle")
        monthly_data = pd.DataFrame({
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
            'Transactions': [11200, 12350, 13100, 14600, 15247, 16800],
            'Fraudes': [45, 38, 42, 28, 32, 25]
        })
        
        fig_monthly = px.line(monthly_data, x='Mois', y=['Transactions', 'Fraudes'],
                             title='Évolution Mensuelle')
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col_stat2:
        st.subheader("🎯 Types de Fraudes")
        fraud_types = pd.DataFrame({
            'Type': ['Carte Clonée', 'Phishing', 'International', 'Identité Volée', 'Autre'],
            'Count': [125, 89, 67, 42, 28]
        })
        
        fig_pie = px.pie(fraud_types, values='Count', names='Type',
                        title='Répartition des Types de Fraude')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Métriques supplémentaires
    st.subheader("📊 Performance du Système")
    col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
    
    with col_perf1:
        st.metric("Précision", "99.2%", "+0.4%")
    
    with col_perf2:
        st.metric("Rappel", "96.8%", "+0.7%")
    
    with col_perf3:
        st.metric("Taux Faux Positifs", "0.8%", "-0.2%")
    
    with col_perf4:
        st.metric("Satisfaction Client", "98.5%", "+1.2%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER PROFESSIONNEL
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🛡️ FraudShield**")
    st.markdown("Sécurité financière intelligente")

with footer_col2:
    st.markdown("**📞 Support**")
    st.markdown("contact@fraudshield.com")

with footer_col3:
    st.markdown("**🔒 Sécurité**")
    st.markdown("Certifié ISO 27001")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666; font-size: 0.9rem;'>© 2024 FraudShield - Intelligence Artificielle pour la Sécurité Financière</div>", 
            unsafe_allow_html=True)
