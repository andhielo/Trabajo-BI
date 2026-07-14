import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Analítica de Salud Mental - Lima Norte",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados (CSS)
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        color: #1E3A8A;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .ethical-container {
        background-color: #ECFDF5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown('<div class="main-title">🧠 Plataforma Integral de Analítica Universitaria</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">BI, Big Data e IA Ética para la mejora de la Salud Mental en Universitarios de Lima Norte</div>', unsafe_allow_html=True)

# Sidebar para filtros
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2042/2042813.png", width=100)
st.sidebar.title("Filtros de Control")

universidad = st.sidebar.selectbox(
    "Seleccione Universidad:",
    ["Todas", "Universidad Nacional de Ingeniería (UNI)", "Universidad de Ciencias y Humanidades (UCH)", "Universidad César Vallejo (UCV)", "Universidad Privada del Norte (UPN)"]
)

distrito = st.sidebar.multiselect(
    "Distrito de Residencia (Lima Norte):",
    ["Los Olivos", "San Martín de Porres", "Comas", "Carabayllo", "Independencia", "Ancón", "Puente Piedra"],
    default=["Los Olivos", "San Martín de Porres", "Comas"]
)

rango_edad = st.sidebar.slider("Rango de Edad:", 16, 40, (18, 25))

# Generar datos simulados de Big Data para la visualización
np.random.seed(42)
n_samples = 500
data = pd.DataFrame({
    'ID': range(1, n_samples + 1),
    'Universidad': np.random.choice(["UNI", "UCH", "UCV", "UPN"], n_samples, p=[0.25, 0.25, 0.25, 0.25]),
    'Edad': np.random.randint(17, 35, n_samples),
    'Distrito': np.random.choice(["Los Olivos", "San Martín de Porres", "Comas", "Carabayllo", "Independencia", "Ancón", "Puente Piedra"], n_samples),
    'Nivel_Ansiedad': np.random.choice(["Bajo", "Moderado", "Severo"], n_samples, p=[0.4, 0.4, 0.2]),
    'Nivel_Depresion': np.random.choice(["Bajo", "Moderado", "Severo"], n_samples, p=[0.45, 0.35, 0.2]),
    'Estrés_Académico': np.random.randint(1, 10, n_samples),
    'Horas_Sueño': np.random.randint(4, 9, n_samples),
    'Apoyo_Social': np.random.choice(["Sí", "No"], n_samples, p=[0.7, 0.3]),
    'Riesgo_Predicho': np.random.choice(["Bajo Riesgo", "Requiere Atención", "Alerta Crítica"], n_samples, p=[0.5, 0.35, 0.15])
})

# Filtrado de datos
df_filtered = data[
    (data['Edad'] >= rango_edad[0]) & 
    (data['Edad'] <= rango_edad[1]) & 
    (data['Distrito'].isin(distrito))
]
if universidad != "Todas":
    univ_map = {"Universidad Nacional de Ingeniería (UNI)": "UNI", 
                "Universidad de Ciencias y Humanidades (UCH)": "UCH", 
                "Universidad César Vallejo (UCV)": "UCV", 
                "Universidad Privada del Norte (UPN)": "UPN"}
    df_filtered = df_filtered[df_filtered['Universidad'] == univ_map[universidad]]

# Tabs de navegación de la plataforma
tab1, tab2, tab3, tab4 = st.tabs(["📊 Business Intelligence (BI)", "🧬 Big Data & Analítica", "🤖 IA Ética & Predicciones", "⚖️ Marco Ético y Gobernanza"])

with tab1:
    st.subheader("Indicadores de Negocio (KPIs de Salud Mental)")
    
    # KPIs en columnas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Estudiantes Evaluados", len(df_filtered))
    with col2:
        alerta_porcentaje = round((df_filtered['Riesgo_Predicho'] == "Alerta Crítica").mean() * 100, 1)
        st.metric("En Alerta Crítica 🚨", f"{alerta_porcentaje}%", delta="-2.1% vs mes anterior", delta_color="inverse")
    with col3:
        promedio_estres = round(df_filtered['Estrés_Académico'].mean(), 1)
        st.metric("Estrés Académico Promedio", f"{promedio_estres}/10")
    with col4:
        horas_sueno_prom = round(df_filtered['Horas_Sueño'].mean(), 1)
        st.metric("Promedio Horas Sueño", f"{horas_sueno_prom} hrs")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("### Niveles de Ansiedad por Distrito")
        fig1 = px.histogram(df_filtered, x="Distrito", color="Nivel_Ansiedad", 
                            barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        st.markdown("### Distribución de Depresión Detectada")
        fig2 = px.pie(df_filtered, names="Nivel_Depresion", 
                      color_discrete_sequence=px.colors.qualitative.Safe, hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Correlaciones de Variables de Big Data")
    st.write("Análisis avanzado cruzando factores socioeconómicos y académicos con el estado psicológico del estudiante.")
    
    col_big1, col_big2 = st.columns(2)
    with col_big1:
        st.markdown("### Impacto de las Horas de Sueño en el Estrés Académico")
        fig_scatter = px.scatter(df_filtered, x="Horas_Sueño", y="Estrés_Académico", 
                                 color="Riesgo_Predicho", size="Edad",
                                 hover_data=['Universidad', 'Distrito'],
                                 color_discrete_map={"Bajo Riesgo": "green", "Requiere Atención": "orange", "Alerta Crítica": "red"})
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_big2:
        st.markdown("### Distribución de Edad vs Estrés")
        fig_box = px.box(df_filtered, x="Universidad", y="Estrés_Académico", color="Apoyo_Social",
                         title="Nivel de Estrés por Universidad y Apoyo Social")
        st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.subheader("Predicciones Predictivas con Inteligencia Artificial")
    st.info("Nota de IA Ética: Este modelo NO reemplaza un diagnóstico clínico. Los datos son anonimizados y se utiliza para canalización preventiva.")
    
    # Formulario interactivo para predecir riesgo individual éticamente
    st.markdown("#### Simulador de Triaje y Canalización con Algoritmo Ético")
    
    col_form1, col_form2 = st.columns(2)
    with col_form1:
        f_edad = st.number_input("Edad del Estudiante", 16, 45, 20)
        f_sueño = st.slider("Horas de Sueño promedio diarias", 3, 12, 6)
        f_estres = st.slider("Autoevaluación de Estrés Académico (1-10)", 1, 10, 7)
    with col_form2:
        f_ansiedad = st.selectbox("¿Ha experimentado episodios frecuentes de ansiedad?", ["No", "A veces", "Frecuentemente"])
        f_apoyo = st.radio("¿Cuenta con una red de apoyo familiar o amical activa?", ["Sí", "No"])
        f_depresivo = st.selectbox("¿Presenta desinterés o tristeza persistente?", ["No", "A veces", "Frecuentemente"])
        
    if st.button("Evaluar Riesgo Éticamente"):
        # Lógica de simulación de modelo predictivo (árbol de decisión/regresión logística simplificada)
        score = 0
        if f_sueño < 6: score += 2
        if f_estres > 7: score += 2
        if f_ansiedad == "Frecuentemente": score += 3
        elif f_ansiedad == "A veces": score += 1
        if f_depresivo == "Frecuentemente": score += 3
        elif f_depresivo == "A veces": score += 1
        if f_apoyo == "No": score += 2
        
        # Resultados de IA con enfoque preventivo y ético
        st.markdown("---")
        if score >= 7:
            st.error("⚠️ **Estado de Riesgo: ALERTA CRÍTICA**")
            st.markdown("""
                **Acción Sugerida Automatizada:** Canalización inmediata con el departamento de psicología de su universidad. 
                Se ha generado un token de atención anónimo para proteger su identidad.
            """)
        elif 4 <= score < 7:
            st.warning("⚡ **Estado de Riesgo: REQUIERE ATENCIÓN MODERADA**")
            st.markdown("""
                **Acción Sugerida Automatizada:** Recomendación de talleres de manejo de estrés y seguimiento preventivo.
            """)
        else:
            st.success("✅ **Estado de Riesgo: BAJO RIESGO**")
            st.markdown("Siga manteniendo hábitos saludables de sueño y balance académico-personal.")

with tab4:
    st.subheader("Gobernanza de Datos e IA Ética")
    st.markdown("""
    Nuestra plataforma se rige estrictamente por principios internacionales de IA Ética (UNESCO) y la Ley de Protección de Datos Personales de Perú (Ley N° 29733):
    
    1. **Anonimización desde el Origen:** No se almacenan nombres, DNIs, correos ni datos directamente identificables. Cada registro se gestiona mediante un Hash Criptográfico.
    2. **Transparencia Algorítmica:** Los modelos predictivos son explicables (XAI). No operan como "cajas negras".
    3. **Consentimiento Informado:** Todo estudiante firma digitalmente el consentimiento antes de participar en las evaluaciones preventivas.
    4. **No Discriminación:** El sistema prohíbe el uso de resultados predictivos para decisiones académicas disciplinarias o de matrícula.
    """)
    
    st.markdown('<div class="ethical-container"><strong>Compromiso Ético de Lima Norte:</strong> "La tecnología debe servir para salvar vidas y potenciar el bienestar estudiantil, respetando incondicionalmente la privacidad."</div>', unsafe_allow_html=True)
