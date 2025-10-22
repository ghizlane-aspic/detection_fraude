import sys
import os

# ✅ CORRECTION : Ajouter le chemin racine du projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import streamlit as st
import time

try:
    from backend_connector import fraud_detector
    HAS_FRAUD_DETECTOR = True
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
    HAS_FRAUD_DETECTOR = False
    
    # Création d'un simulateur de secours
    class MockFraudDetector:
        def __init__(self):
            self.is_loaded = False
            self.model_name = "Simulation"
        
        def predict(self, data):
            return {
                'success': True,
                'is_fraud': False,
                'fraud_probability': 0.1,
                'risk_score': 15,
                'model_used': 'Simulation',
                'risk_factors': []
            }
    
    fraud_detector = MockFraudDetector()

# Le reste de votre code Streamlit reste identique...
# [Votre CSS et interface utilisateur existants]

# CSS UNIFIÉ AVEC ANIMATIONS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: none;
        transition: all 0.4s ease;
        animation: slideInUp 0.8s ease-out;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .form-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .result-fraud {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.5);
        animation: shake 0.5s ease, glowRed 2s infinite;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    @keyframes glowRed {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 107, 107, 0.8); }
    }
    
    .result-safe {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 15px 35px rgba(67, 233, 123, 0.5);
        animation: bounce 1s ease, glowGreen 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glowGreen {
        0%, 100% { box-shadow: 0 0 20px rgba(67, 233, 123, 0.5); }
        50% { box-shadow: 0 0 40px rgba(67, 233, 123, 0.8); }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .risk-factor {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
        animation: slideInRight 0.5s ease-out;
        box-shadow: 0 8px 20px rgba(250, 112, 154, 0.4);
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
    }
    
    .input-group {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .input-group:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(5px);
    }
    
    .spinner {
        animation: rotate 1s linear infinite;
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .model-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== BOUTON RETOUR ====================
col_back, col_title, col_empty = st.columns([1, 2, 1])
with col_back:
    if st.button("← Retour", use_container_width=True):
        st.switch_page("app.py")

# ==================== TITRE ====================
st.markdown('<h1 class="page-title">🔍 Analyse de Transactions</h1>', unsafe_allow_html=True)

# ==================== DESCRIPTION ====================
model_status = "✅ Actif" if (HAS_FRAUD_DETECTOR and fraud_detector.is_loaded) else "🔄 Simulation"
model_name = fraud_detector.model_name if HAS_FRAUD_DETECTOR else "Simulation"

st.markdown(f"""
<div class="card">
    <h2 style="color: #2c3e50; text-align: center; margin-bottom: 1rem;">Analysez vos transactions en temps réel</h2>
    <p style="color: #7f8c8d; text-align: center; font-size: 1.1rem; line-height: 1.6;">
        Notre Intelligence Artificielle analyse instantanément chaque transaction pour détecter 
        les fraudes potentielles. Remplissez le formulaire ci-dessous et obtenez un résultat en moins de 2 secondes !
    </p>
    
  
</div>
""", unsafe_allow_html=True)

# ==================== FORMULAIRE ====================
with st.form("transaction_form"):
    st.markdown("""
    <div class="form-section">
        <h2 style="color: white; text-align: center; margin: 0;">📋 Formulaire d'Analyse</h2>
        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0;">
            Remplissez les informations de la transaction à analyser
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SECTION 1 : INFORMATIONS CLIENT ==========
    st.markdown("### 👤 Informations Client")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        age = st.slider(
            "🎂 Âge du client",
            min_value=18,
            max_value=100,
            value=35,
            help="Âge du titulaire de la carte"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        gender = st.selectbox(
            "🚻 Genre",
            ["Homme", "Femme"],
            help="Genre du client"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        job = st.selectbox(
            "💼 Profession",
            ["Employé", "Cadre", "Commerçant", "Retraité", "Étudiant", "Autre"],
            help="Profession du client"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== SECTION 2 : DÉTAILS TRANSACTION ==========
    st.markdown("### 💳 Détails de la Transaction")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        amount = st.number_input(
            "💰 Montant (€)",
            min_value=0.0,
            max_value=10000.0,
            value=150.0,
            step=1.0,
            help="Montant de la transaction en euros"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        category = st.selectbox(
            "🛒 Catégorie d'achat",
            [
                "Supermarché",
                "Restaurant", 
                "Essence",
                "Shopping/Vêtements",
                "Pharmacie",
                "Transport",
                "Loisirs",
                "En ligne",
                "Voyage",
                "Autre"
            ],
            help="Type de commerce"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        merchant = st.text_input(
            "🏪 Commerçant",
            value="Carrefour",
            help="Nom du commerçant"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== SECTION 3 : LOCALISATION ==========
    st.markdown("### 📍 Localisation")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        city = st.text_input(
            "🏙️ Ville",
            value="Tanger",
            help="Ville où la transaction a lieu"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        distance = st.slider(
            "🚗 Distance du domicile (km)",
            min_value=0.0,
            max_value=1000.0,
            value=15.0,
            step=5.0,
            help="Distance entre le domicile et le lieu de transaction"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== SECTION 4 : MOMENT ==========
    st.markdown("### 🕐 Moment de la Transaction")
    
    col9, col10 = st.columns(2)
    
    with col9:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        trans_hour = st.slider(
            "⏰ Heure de la journée",
            min_value=0,
            max_value=23,
            value=14,
            help="Heure à laquelle la transaction a été effectuée"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col10:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        is_weekend = st.checkbox(
            "🎉 Week-end",
            value=False,
            help="Transaction effectuée le week-end"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== BOUTON D'ANALYSE ==========
    st.markdown("---")
    submitted = st.form_submit_button(
        "🚀 LANCER L'ANALYSE IA",
        type="primary",
        use_container_width=True
    )

# ==================== TRAITEMENT ET RÉSULTATS ====================
if submitted:
    # Animation de chargement
    with st.spinner(""):
        st.markdown('<div class="spinner">🔄</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; font-size: 1.2rem; color: white; margin: 1rem 0;">Notre IA analyse la transaction...</div>', unsafe_allow_html=True)
        
        # Simulation du temps d'analyse
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
    
    # ========== UTILISATION DU MODÈLE IA ==========
    input_data = {
        'amount': amount,
        'merchant': merchant,
        'category': category,
        'gender': gender,
        'age': age,
        'job': job,
        'city': city,
        'distance': distance,
        'trans_hour': trans_hour,
        'is_weekend': is_weekend
    }
    
    # Appel au modèle (réel ou simulation)
    result = fraud_detector.predict(input_data)
    
    # Variables pour l'affichage
    use_simulation = not HAS_FRAUD_DETECTOR or not result.get('success', False)
    
    # Gestion des erreurs
    if not result.get('success', False):
        if not use_simulation:
            st.error(f"❌ {result.get('error', 'Erreur inconnue du modèle')}")
            st.info("💡 Utilisation du mode simulation en attendant...")
        use_simulation = True
    
    # ========== MODE SIMULATION (fallback) ==========
    if use_simulation:
        risk_score = 0
        risk_factors = []
        
        # Facteur 1 : Montant
        if amount > 2000:
            risk_score += 35
            risk_factors.append("💰 Montant très élevé (>2000€)")
        elif amount > 1000:
            risk_score += 20
            risk_factors.append("💸 Montant élevé (1000-2000€)")
        elif amount > 500:
            risk_score += 10
            risk_factors.append("📈 Montant supérieur à la moyenne")
        
        # Facteur 2 : Heure
        if trans_hour < 6:
            risk_score += 25
            risk_factors.append("🌙 Transaction très tôt (avant 6h)")
        elif trans_hour > 22:
            risk_score += 20
            risk_factors.append("🌜 Transaction tardive (après 22h)")
        
        # Facteur 3 : Distance
        if distance > 500:
            risk_score += 30
            risk_factors.append("✈️ Très loin du domicile (>500km)")
        elif distance > 100:
            risk_score += 20
            risk_factors.append("🚗 Loin du domicile (100-500km)")
        elif distance > 50:
            risk_score += 10
            risk_factors.append("📍 Distance modérée")
        
        # Facteur 4 : Catégorie
        if category in ["En ligne", "Voyage"]:
            risk_score += 15
            risk_factors.append(f"🎯 Catégorie {category} (risque élevé)")
        elif category in ["Loisirs", "Shopping/Vêtements"]:
            risk_score += 8
            risk_factors.append(f"🛍️ Catégorie {category} (risque modéré)")
        
        # Facteur 5 : Combinaisons
        if is_weekend and (trans_hour < 6 or trans_hour > 22):
            risk_score += 15
            risk_factors.append("🎭 Week-end + heures inhabituelles")
        
        if amount > 500 and distance > 50:
            risk_score += 12
            risk_factors.append("⚡ Montant élevé + distance")
        
        # Calcul final simulation
        probability = min(risk_score / 100, 0.99)
        is_fraud = probability > 0.5
        model_used = "Simulation"
        
    else:
        # Utiliser les vrais résultats du modèle
        is_fraud = result['is_fraud']
        probability = result['fraud_probability']
        risk_score = result['risk_score']
        model_used = result['model_used']
        risk_factors = result.get('risk_factors', [])
        
        # Afficher info modèle utilisé
        st.success(f"✅ Analyse réalisée avec le modèle **{model_used}**")

    # ========== AFFICHAGE DES RÉSULTATS ==========
    st.markdown("---")
    st.markdown("## 📊 Résultats de l'Analyse")
    
    # Récapitulatif
    with st.expander("📋 Récapitulatif de la transaction", expanded=True):
        recap_col1, recap_col2, recap_col3 = st.columns(3)
        
        with recap_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #2c3e50; margin: 0;">👤 Client</h4>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Âge : {age} ans</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Genre : {gender}</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Profession : {job}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with recap_col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #2c3e50; margin: 0;">💳 Transaction</h4>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Montant : {amount:.2f}€</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Catégorie : {category}</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Commerçant : {merchant}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with recap_col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #2c3e50; margin: 0;">📍 Contexte</h4>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Ville : {city}</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Distance : {distance} km</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Heure : {trans_hour}h</p>
                <p style="color: #7f8c8d; margin: 0.5rem 0;">• Week-end : {'Oui' if is_weekend else 'Non'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("###")
    
    # Résultat principal
    if is_fraud:
        # ========== FRAUDE DÉTECTÉE ==========
        st.markdown("""
        <div class="result-fraud">
            <h2 style="text-align: center; margin: 0; font-size: 2.5rem;">🚨 ALERTE FRAUDE</h2>
            <h3 style="text-align: center; margin: 0.5rem 0; color: rgba(255,255,255,0.9);">
                Transaction suspecte détectée
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        # Métriques
        prob_percent = probability * 100
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #ff6b6b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #ff6b6b;">{prob_percent:.1f}%</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Probabilité</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric2:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #ff6b6b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #ff6b6b;">{risk_score}/100</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Score de risque</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric3:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #ff6b6b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #ff6b6b;">{len(risk_factors)}</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Facteurs risques</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        # Facteurs de risque
        if risk_factors:
            st.markdown("#### 🔍 Facteurs de Risque Identifiés")
            for factor in risk_factors:
                st.markdown(f'<div class="risk-factor">{factor}</div>', unsafe_allow_html=True)
        
        st.markdown("###")
        
        # Recommandations
        st.markdown("#### 🛡️ Actions Recommandées")
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("""
            <div class="card">
                <h4 style="color: #2c3e50; margin-top: 0;">⚡ Actions Immédiates</h4>
                <ul style="color: #7f8c8d;">
                    <li>🛑 Bloquer temporairement la transaction</li>
                    <li>📞 Contacter le client immédiatement</li>
                    <li>🔐 Demander authentification supplémentaire</li>
                    <li>🔒 Geler temporairement la carte</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rec_col2:
            st.markdown("""
            <div class="card">
                <h4 style="color: #2c3e50; margin-top: 0;">🔍 Investigation</h4>
                <ul style="color: #7f8c8d;">
                    <li>📊 Vérifier l'historique récent</li>
                    <li>🔎 Analyser transactions similaires</li>
                    <li>👮 Signaler aux autorités si nécessaire</li>
                    <li>📈 Mettre à jour les patterns de fraude</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # ========== TRANSACTION LÉGITIME ==========
        st.markdown("""
        <div class="result-safe">
            <h2 style="text-align: center; margin: 0; font-size: 2.5rem;">✅ TRANSACTION SÉCURISÉE</h2>
            <h3 style="text-align: center; margin: 0.5rem 0; color: rgba(255,255,255,0.9);">
                Aucun risque de fraude détecté
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        # Métriques
        prob_percent = probability * 100
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #43e97b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #43e97b;">{prob_percent:.1f}%</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Probabilité</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric2:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #43e97b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #43e97b;">{risk_score}/100</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Score de risque</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_metric3:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #43e97b;">
                <h2 style="margin: 0; font-size: 2.5rem; color: #43e97b;">FAIBLE</h2>
                <p style="margin: 0.5rem 0; color: #7f8c8d;">Niveau de risque</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        # Message de confirmation (CORRIGÉ : <u1> → <ul>)
        st.markdown("""
        <div class="card">
            <h3 style="color: #2c3e50; margin-top: 0;">✅ Analyse Positive</h3>
            <p style="color: #7f8c8d; font-size: 1.1rem; line-height: 1.6;">
                Notre système IA n'a détecté aucun pattern suspect dans cette transaction. 
                Tous les paramètres analysés correspondent à un comportement d'achat normal.
                Actions Recommandées :
            </p>
            
<ul style="color: #7f8c8d; line-height: 1.8;">
    <li>✓ <b>Approuver</b> la transaction automatiquement</li>
    <li>✓ <b>Aucune vérification</b> supplémentaire requise</li>
    <li>✓ <b>Continuer</b> la surveillance normale</li>
    <li>✓ <b>Mettre à jour</b> les patterns comportementaux</li>
</ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Facteurs mineurs si présents
        if risk_factors:
            st.markdown("###")
            with st.expander("⚠️ Points d'attention mineurs"):
                for factor in risk_factors:
                    st.markdown(f"""
                    <div style="background: rgba(255, 193, 7, 0.1); 
                                padding: 1rem; border-radius: 8px; 
                                margin: 0.5rem 0; border-left: 4px solid #ffc107;">
                        <p style="margin: 0; color: #7f8c8d;">{factor}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption("Ces éléments ne sont pas suffisamment critiques pour bloquer la transaction.")

# ==================== BOUTON NOUVELLE ANALYSE ====================
if submitted:
    st.markdown("---")
    col_new1, col_new2, col_new3 = st.columns([1, 2, 1])
    with col_new2:
        if st.button("🔄 Nouvelle Analyse", use_container_width=True):
            st.rerun()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.8);">
    <p style="font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">
        🔍 Système de Détection de Fraudes en Temps Réel
    </p>
    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">
        Analyse IA • Décision instantanée • Protection maximale
    </p>
</div>
""", unsafe_allow_html=True)
