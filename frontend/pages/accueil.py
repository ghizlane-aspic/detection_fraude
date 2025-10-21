# app.py - INTERFACE ULTRA MODERNE (VERSION CORRIGÉE)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS ULTRA MODERNE
st.markdown("""
<style>
    /* Reset et styles généraux */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* Header néon */
    .neon-header {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(79, 172, 254, 0.5); }
        to { text-shadow: 0 0 30px rgba(79, 172, 254, 0.8), 0 0 40px rgba(79, 172, 254, 0.6); }
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #a8b2d1;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* Cartes en verre */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Bouton cyber */
    .cyber-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        border: none;
        padding: 1.2rem 3rem;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .cyber-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .cyber-button:hover::before {
        left: 100%;
    }
    
    .cyber-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
    }
    
    /* Métriques modernes */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        transform: translateY(-3px);
    }
    
    /* Typographie moderne */
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
    }
    
    .feature-text {
        color: #a8b2d1;
        line-height: 1.7;
        font-size: 1.1rem;
    }
    
    /* Icônes animées */
    .icon-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# HEADER CYBERPUNK
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="neon-header">🛡️ FRAUDSHIELD AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">INTELLIGENCE ARTIFICIELLE • DÉTECTION EN TEMPS RÉEL • SÉCURITÉ AVANCÉE</p>', unsafe_allow_html=True)

# BOUTON PRINCIPAL CYBER
st.markdown("""
<div style='text-align: center; margin: 3rem 0;'>
    <h2 style='color: #a8b2d1; font-weight: 300; margin-bottom: 1.5rem;'>PRÊT À DÉCLENCHER L'ANALYSE ?</h2>
</div>
""", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button(" DÉMARRER LA DÉTECTION IA", use_container_width=True, key="main_cta"):
        st.switch_page("pages/prediction.py")

# SECTION MÉTRIQUES EN TEMPS RÉEL
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title"> DASHBOARD LIVE</h2>', unsafe_allow_html=True)

# Métriques animées
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown("""
    <div class="metric-card">
        <div style='font-size: 2.5rem; font-weight: 800; color: #00f2fe;'>1.2K</div>
        <div style='color: #a8b2d1;'>TRANSACTIONS</div>
        <div style='color: #4ade80; font-size: 0.9rem;'>↗ +5.2%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    st.markdown("""
    <div class="metric-card">
        <div style='font-size: 2.5rem; font-weight: 800; color: #ff6b6b;'>12</div>
        <div style='color: #a8b2d1;'>ALERTES</div>
        <div style='color: #f87171; font-size: 0.9rem;'>↘ -2.1%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown("""
    <div class="metric-card">
        <div style='font-size: 2.5rem; font-weight: 800; color: #4facfe;'>99.3%</div>
        <div style='color: #a8b2d1;'>PRÉCISION</div>
        <div style='color: #4ade80; font-size: 0.9rem;'>↗ +0.4%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col4:
    st.markdown("""
    <div class="metric-card">
        <div style='font-size: 2.5rem; font-weight: 800; color: #a78bfa;'>47ms</div>
        <div style='color: #a8b2d1;'>TEMPS MOYEN</div>
        <div style='color: #4ade80; font-size: 0.9rem;'>↘ -3ms</div>
    </div>
    """, unsafe_allow_html=True)

# Graphiques modernes
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Graphique radial moderne
    categories = ['Transactions', 'Alertes', 'Précision', 'Vitesse']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[95, 85, 99, 92],
        theta=categories,
        fill='toself',
        fillcolor='rgba(79, 172, 254, 0.3)',
        line=dict(color='#4facfe', width=3),
        name='Performance'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with chart_col2:
    # Graphique de distribution
    risk_data = pd.DataFrame({
        'Niveau': ['Faible', 'Moyen', 'Élevé', 'Critique'],
        'Pourcentage': [68, 22, 8, 2],
        'Couleur': ['#4ade80', '#fbbf24', '#f87171', '#dc2626']
    })
    
    fig_bar = px.bar(risk_data, x='Niveau', y='Pourcentage', 
                     color='Niveau', color_discrete_map=dict(zip(risk_data['Niveau'], risk_data['Couleur'])),
                     title='DISTRIBUTION DES RISQUES')
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# SECTION FONCTIONNALITÉS AVANCÉES
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">⚡ TECHNOLOGIES AVANCÉES</h2>', unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;' class="icon-pulse">🧠</div>
        <h3 style='color: #00f2fe; margin-bottom: 1rem;'>IA PROFONDE</h3>
        <p class="feature-text">Réseaux de neurones avancés pour une détection pattern-based avec 99.3% de précision</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;' class="icon-pulse">⚡</div>
        <h3 style='color: #4facfe; margin-bottom: 1rem;'>TEMPS RÉEL</h3>
        <p class="feature-text">Analyse en 47ms avec streaming data processing et alertes instantanées</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;' class="icon-pulse">🔒</div>
        <h3 style='color: #a78bfa; margin-bottom: 1rem;'>CRYPTO SÉCURISÉ</h3>
        <p class="feature-text">Chiffrement end-to-end et blockchain pour une traçabilité inviolable</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# CALL TO ACTION FINAL
st.markdown("""
<div style='text-align: center; margin: 4rem 0;'>
    <h2 style='color: #a8b2d1; font-weight: 300; margin-bottom: 2rem;'>NE LAISSEZ PLUS AUCUNE FRAUDE VOUS ÉCHAPPER</h2>
</div>
""", unsafe_allow_html=True)

col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
with col_cta2:
    if st.button("🔓 ACCÉDER AU SYSTÈME DE DÉTECTION", use_container_width=True, key="final_cta"):
        st.switch_page("pages/prediction.py")

# FOOTER CYBER
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **🛡️ FRAUDSHIELD AI**  
    *Sécurité nouvelle génération*
    """)

with footer_col2:
    st.markdown("""
    **📡 SUPPORT 24/7**  
    `security@fraudshield.ai`
    """)

with footer_col3:
    st.markdown("""
    **🔐 CERTIFICATIONS**  
    ISO 27001 • GDPR • SOC2
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #a8b2d1; font-size: 0.8rem; letter-spacing: 1px;'>
    © 2024 FRAUDSHIELD AI • SYSTÈME DE DÉTECTION INTELLIGENTE • V2.4.1
</div>
""", unsafe_allow_html=True)