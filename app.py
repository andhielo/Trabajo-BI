import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Analítica Salud Mental - Lima Norte",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables de estado para la navegación y persistencia de datos
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Pantalla General"

if 'dataset_crudo' not in st.session_state:
    # Generar datos base alineados exactamente al esquema del CSV
    np.random.seed(42)
    n_samples = 500
    hash_ids = [f"usr_{hash(i) & 0xffffffff:08x}" for i in range(n_samples)]
    st.session_state['dataset_crudo'] = pd.DataFrame({
        'Hash_ID': hash_ids,
        'Universidad': np.random.choice(["UNI", "UCH", "UCV", "UPN"], n_samples),
        'Edad': np.random.randint(16, 36, n_samples),
        'Sexo': np.random.choice(["Masculino", "Femenino"], n_samples),
        'Distrito_Residencia': np.random.choice(["Los Olivos", "San Martín de Porres", "Comas", "Carabayllo", "Independencia"], n_samples),
        'Ciclo_Academico': np.random.randint(1, 11, n_samples),
        'Puntuacion_Ansiedad_GAD7': np.random.randint(0, 22, n_samples),
        'Puntuacion_Depresion_PHQ9': np.random.randint(0, 28, n_samples),
        'Estres_Academico': np.random.randint(1, 11, n_samples),
        'Horas_Sueno_Promedio': np.round(np.random.uniform(4.0, 9.5, n_samples), 1),
        'Apoyo_Social_Activo': np.random.choice(["Sí", "No"], n_samples, p=[0.75, 0.25])
    })

def set_page(page_name):
    st.session_state.current_page = page_name

# ==========================================
# ESTILOS CSS PERSONALIZADOS (TEMA BLANCO)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    hr {
        border-color: #E2E8F0 !important;
    }
    .main-banner {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .main-banner h1 {
        color: #1E3A8A;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        margin-top: 0;
    }
    .main-banner p {
        font-size: 16px;
        color: #475569;
        margin-bottom: 15px;
    }
    .tech-badge {
        background-color: #F1F5F9;
        color: #059669;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #E2E8F0;
    }
    [data-testid="baseButton-secondary"] {
        background-color: #F1F5F9;
        color: #1E3A8A !important;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 10px;
        font-weight: bold;
    }
    [data-testid="baseButton-primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 12px;
        font-weight: bold;
        font-size: 16px;
    }
    .step-header {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .step-title {
        font-size: 18px;
        font-weight: bold;
        color: #0F172A;
        margin-bottom: 5px;
        margin-top: 0px;
    }
    .step-desc {
        font-size: 13px;
        color: #64748B;
        height: 40px;
        margin-bottom: 15px;
    }
    .step-status {
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: #1E3A8A;
    }
    .metric-label {
        font-size: 14px;
        color: #475569;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR (BARRA LATERAL)
# ==========================================
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 10px;"><h1 style="font-size: 50px; margin: 0;">🧠</h1><h2 style="margin: 0; font-size: 20px; font-weight: 900; color: #1E3A8A !important;">SALUD MENTAL</h2><p style="font-size: 12px; color: #64748B !important; margin-top: -5px;">— LIMA NORTE —</p></div>', unsafe_allow_html=True)
    
    if st.button("⊞ Pantalla General", use_container_width=True):
        set_page("Pantalla General")
        
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #64748B !important; margin-bottom: 10px;'>7 PASOS DEL FLUJO BI</p>", unsafe_allow_html=True)
    
    opciones = [
        "① Fuentes de Datos",
        "② Staging Area",
        "③ Proceso ETL",
        "④ Data Warehouse",
        "⑤ Capa de IA Ética",
        "⑥ Capa Semántica & KPIs",
        "⑦ Visualización BI"
    ]
    
    for op in opciones:
        if st.session_state.current_page == op:
            st.markdown(f"<div style='background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 8px 10px; border-radius: 0px 5px 5px 0px; margin-bottom: 5px; cursor: pointer; font-size: 14px; font-weight: bold; color: #1D4ED8 !important;'>{op}</div>", unsafe_allow_html=True)
        else:
            if st.button(op, key=op, use_container_width=True):
                set_page(op)

df_active = st.session_state['dataset_crudo']

# ==========================================
# CONTENIDOS DE LAS PANTALLAS
# ==========================================

# --- PANTALLA GENERAL ---
if st.session_state.current_page == "Pantalla General":
    st.markdown("""
    <div class="main-banner">
        <h1>PLATAFORMA BI INTEGRADA - SALUD MENTAL UNIVERSITARIA</h1>
        <p>Gobernanza cloud end-to-end: captura segura de encuestas, anonimización criptográfica, almacenamiento dimensional y analítica predictiva ética.</p>
        <div class="tech-badge">🟢 GitHub + Supabase PostgreSQL + Streamlit Community Cloud</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #3B82F6;">Paso 1</span><span style="color: #94A3B8;">FUENTES DE DATOS</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Fuentes de Datos</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Captura de cuestionarios e historial académico de Lima Norte.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #0EA5E9;">Carga activa</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 1 →", key="btn1", use_container_width=True): set_page("① Fuentes de Datos"); st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #8B5CF6;">Paso 2</span><span style="color: #94A3B8;">STAGING AREA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Staging Area</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Control de calidad sintáctico y anonimización de identidades.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #8B5CF6;">Seguridad y limpieza</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 2 →", key="btn2", use_container_width=True): set_page("② Staging Area"); st.rerun()
    with col3:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #10B981;">Paso 3</span><span style="color: #94A3B8;">PROCESO ETL</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Proceso ETL</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Generación de indicadores clínicos (GAD y PHQ) normalizados.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #10B981;">Transformación fluida</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 3 →", key="btn3", use_container_width=True): set_page("③ Proceso ETL"); st.rerun()
    with col4:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #F59E0B;">Paso 4</span><span style="color: #94A3B8;">DATA WAREHOUSE</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Data Warehouse</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Persistencia relacional en Supabase con Modelo Snowflake.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #F59E0B;">Esquema estrella/copo</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 4 →", key="btn4", use_container_width=True): set_page("④ Data Warehouse"); st.rerun()

    st.write("")
    col5, col6, col7, _ = st.columns(4)
    with col5:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #3B82F6;">Paso 5</span><span style="color: #94A3B8;">CAPA DE IA ÉTICA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa de IA Ética</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Cálculo de riesgo predictivo con explicabilidad y privacidad.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #3B82F6;">Prevención con sesgo cero</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 5 →", key="btn5", use_container_width=True): set_page("⑤ Capa de IA Ética"); st.rerun()
    with col6:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #EAB308;">Paso 6</span><span style="color: #94A3B8;">CAPA SEMÁNTICA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa Semántica</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">KPIs ejecutivos, promedio de estrés, GAD-7 y PHQ-9.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #EAB308;">Negocio y analítica</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 6 →", key="btn6", use_container_width=True): set_page("⑥ Capa Semántica & KPIs"); st.rerun()
    with col7:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #EC4899;">Paso 7</span><span style="color: #94A3B8;">VISUALIZACIÓN BI</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Visualización BI</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Dashboards y reportes analíticos consolidados.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #EC4899;">Mando directivo</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 7 →", key="btn7", use_container_width=True): set_page("⑦ Visualización BI"); st.rerun()

# --- PASO 1: FUENTES DE DATOS ---
elif st.session_state.current_page == "① Fuentes de Datos":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Fuentes de datos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; margin-bottom: 30px;'>Carga archivos SISAP o datasets de encuestas de salud mental universitaria en Lima Norte.</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        uploaded_file = st.file_uploader("Carga archivo en formato XLSX, XLS, CSV", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df_active = pd.read_csv(uploaded_file)
                else:
                    df_active = pd.read_excel(uploaded_file)
                st.session_state['dataset_crudo'] = df_active
                st.success("✅ Archivo cargado correctamente.")
            except Exception as e:
                st.error(f"Error al procesar: {e}")

    st.markdown(f"<div style='background-color: #EFF6FF; padding: 12px; border-radius: 6px; margin: 15px 0; border-left: 5px solid #2563EB; color: #1E40AF; font-weight: bold;'>Registros leídos: {len(df_active)} | Válidos: {len(df_active)}</div>", unsafe_allow_html=True)
    st.dataframe(df_active.head(10), use_container_width=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ② Staging Area →", type="primary", use_container_width=True):
            set_page("② Staging Area"); st.rerun()

# --- PASO 2: STAGING AREA ---
elif st.session_state.current_page == "② Staging Area":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Staging Area</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Capa intermedia de sanitización de datos. Enfoque ético: Anonimización de datos mediante hashing criptográfico.</p>", unsafe_allow_html=True)

    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(f'<div class="metric-label">Registros fuente</div><div class="metric-value">{len(df_active)}</div>', unsafe_allow_html=True)
    with c_m2:
        st.markdown(f'<div class="metric-label">Registros OK</div><div class="metric-value">{len(df_active)}</div>', unsafe_allow_html=True)
    with c_m3:
        st.markdown('<div class="metric-label">Errores Sanitizados</div><div class="metric-value" style="color: #10B981;">0</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("#### Datos anonimizados listos para ETL:")
    df_stage = df_active.copy()
    if 'Hash_ID' not in df_stage.columns:
        df_stage['Hash_ID'] = [f"sha256_{hash(str(x)) & 0xffffffff:08x}" for x in range(len(df_stage))]
    
    st.dataframe(df_stage.head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ③ Proceso ETL →", type="primary", use_container_width=True):
            set_page("③ Proceso ETL"); st.rerun()

# --- PASO 3: PROCESO ETL ---
elif st.session_state.current_page == "③ Proceso ETL":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Proceso ETL</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Limpieza, mapeo de dimensiones y estructuración de métricas de GAD-7 (Ansiedad) y PHQ-9 (Depresión).</p>", unsafe_allow_html=True)

    with st.spinner("Ejecutando pipeline de limpieza y transformación de datos..."):
        df_etl = df_active.copy()
        # Se utilizan las columnas EXACTAS del archivo CSV
        df_etl['Nivel_Ansiedad'] = pd.cut(df_etl['Puntuacion_Ansiedad_GAD7'], bins=[-1, 4, 9, 14, 21], labels=["Mínimo", "Leve", "Moderado", "Severo"])
        df_etl['Nivel_Depresion'] = pd.cut(df_etl['Puntuacion_Depresion_PHQ9'], bins=[-1, 4, 9, 14, 19, 27], labels=["Mínimo", "Leve", "Moderado", "Moderado-Severo", "Severo"])

    st.success("✅ ¡Transformación completada con éxito!")
    st.dataframe(df_etl[['Hash_ID', 'Universidad', 'Nivel_Ansiedad', 'Nivel_Depresion', 'Horas_Sueno_Promedio', 'Estres_Academico']].head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ④ Data Warehouse →", type="primary", use_container_width=True):
            set_page("④ Data Warehouse"); st.rerun()

# --- PASO 4: DATA WAREHOUSE ---
elif st.session_state.current_page == "④ Data Warehouse":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Data Warehouse en Supabase (Cloud PostgreSQL)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Modelo lógico dimensional de Copo de Nieve (Snowflake Schema) para el repositorio de hechos de Salud Mental.</p>", unsafe_allow_html=True)

    # Gráfico corregido (Se remueven las propiedades incorrectas ec y fc)
    fig = go.Figure()
    fig.add_annotation(
        x=0.5, y=0.5, 
        text="FACT_SALUD_MENTAL<br><br>PK_Evaluacion<br>FK_Estudiante (Hash)<br>FK_Universidad<br>FK_Tiempo<br>Metrica_GAD7<br>Metrica_PHQ9<br>Metrica_HorasSueno",
        showarrow=False, 
        bordercolor="#3B82F6",
        borderwidth=2,
        bgcolor="#EFF6FF",
        font=dict(size=12, color="#1E3A8A")
    )
    fig.add_annotation(
        x=0.1, y=0.5, 
        text="DIM_ESTUDIANTE<br><br>PK_Estudiante<br>Edad<br>Sexo<br>Distrito_Residencia",
        showarrow=False, 
        bordercolor="#64748B",
        borderwidth=1,
        bgcolor="#F8FAFC",
        font=dict(size=11, color="#0F172A")
    )
    fig.add_annotation(
        x=0.9, y=0.5, 
        text="DIM_UNIVERSIDAD<br><br>PK_Universidad<br>Nombre_Sede<br>Abreviatura",
        showarrow=False, 
        bordercolor="#64748B",
        borderwidth=1,
        bgcolor="#F8FAFC",
        font=dict(size=11, color="#0F172A")
    )
    fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), height=250, margin=dict(l=0,r=0,t=0,b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Acciones de Carga y Mantenimiento")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.button("Guardar Data Warehouse en Supabase", use_container_width=True)
    with col_a2:
        st.button("Reconstruir Tablas (Vaciar Supabase)", use_container_width=True)

    st.markdown(f"**Filas analíticas consolidadas:** {len(df_active)}")
    st.dataframe(df_active.head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑤ Capa de IA →", type="primary", use_container_width=True):
            set_page("⑤ Capa de IA Ética"); st.rerun()

# --- PASO 5: CAPA DE IA ÉTICA ---
elif st.session_state.current_page == "⑤ Capa de IA Ética":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Capa de Inteligencia Artificial Ética</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Modelado predictivo de riesgos de ansiedad y depresión severa utilizando algoritmos explicables no sesgados.</p>", unsafe_allow_html=True)

    st.info("💡 **Compromiso Ético:** Para evitar sesgos discriminatorios en procesos universitarios, el modelo no utiliza variables socioeconómicas directas de forma punitiva. Cada predicción emite un código/token de canalización único y anónimo.")

    # Simulación de predicciones
    df_pred = df_active.copy()
    score_riesgo = (df_pred['Puntuacion_Ansiedad_GAD7'] * 0.4 + df_pred['Puntuacion_Depresion_PHQ9'] * 0.4 + df_pred['Estres_Academico'] * 0.2) / 25
    df_pred['Prob_Riesgo'] = np.clip(score_riesgo, 0.05, 0.98).round(3)
    df_pred['Riesgo_Predicho_IA'] = np.where(df_pred['Prob_Riesgo'] > 0.65, "Riesgo Alto", np.where(df_pred['Prob_Riesgo'] > 0.35, "Riesgo Moderado", "Riesgo Bajo"))

    col_ia1, col_ia2 = st.columns(2)
    with col_ia1:
        fig_prob = px.histogram(df_pred, x="Prob_Riesgo", color="Riesgo_Predicho_IA", 
                                title="Distribución de Probabilidades de Riesgo Preventivo",
                                color_discrete_map={"Riesgo Alto": "#EF4444", "Riesgo Moderado": "#F59E0B", "Riesgo Bajo": "#10B981"},
                                labels={"Prob_Riesgo": "Índice de Riesgo (0-1)"})
        fig_prob.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_prob, use_container_width=True)

    with col_ia2:
        fig_scatter = px.scatter(df_pred, x="Horas_Sueno_Promedio", y="Estres_Academico", color="Riesgo_Predicho_IA",
                                 title="Correlación: Sueño vs Estrés Académico",
                                 color_discrete_map={"Riesgo Alto": "#EF4444", "Riesgo Moderado": "#F59E0B", "Riesgo Bajo": "#10B981"})
        fig_scatter.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("### Tabla de Predicciones por ID de Estudiante (Anonimizado)")
    st.dataframe(df_pred[['Hash_ID', 'Universidad', 'Prob_Riesgo', 'Riesgo_Predicho_IA']].head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑥ Capa Semántica & KPIs →", type="primary", use_container_width=True):
            set_page("⑥ Capa Semántica & KPIs"); st.rerun()

# --- PASO 6: CAPA SEMÁNTICA & KPIS ---
elif st.session_state.current_page == "⑥ Capa Semántica & KPIs":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Capa Semántica & KPIs</h2>", unsafe_allow_html=True)

    st.markdown("### Filtros de Análisis")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        u_sel = st.selectbox("Seleccionar Universidad", ["Todas", "UNI", "UCH", "UCV", "UPN"])
    with col_f2:
        d_sel = st.multiselect("Distritos Sede", ["Los Olivos", "San Martín de Porres", "Comas", "Carabayllo", "Independencia"], default=["Los Olivos", "Comas"])

    df_filtered = df_active.copy()
    if u_sel != "Todas":
        df_filtered = df_filtered[df_filtered['Universidad'] == u_sel]
    if d_sel:
        df_filtered = df_filtered[df_filtered['Distrito_Residencia'].isin(d_sel)]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="metric-label">Estrés Promedio General</div><div class="metric-value">{df_filtered["Estres_Academico"].mean():.2f}/10</div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-label">GAD-7 Promedio (Ansiedad)</div><div class="metric-value">{df_filtered["Puntuacion_Ansiedad_GAD7"].mean():.2f}/21</div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-label">PHQ-9 Promedio (Depresión)</div><div class="metric-value">{df_filtered["Puntuacion_Depresion_PHQ9"].mean():.2f}/27</div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="metric-label">Promedio de Sueño</div><div class="metric-value">{df_filtered["Horas_Sueno_Promedio"].mean():.2f} hrs</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### Capa Semántica - Datos Filtrados")
    st.dataframe(df_filtered.head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑦ Visualización BI →", type="primary", use_container_width=True):
            set_page("⑦ Visualización BI"); st.rerun()

# --- PASO 7: VISUALIZACIÓN BI ---
elif st.session_state.current_page == "⑦ Visualización BI":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Visualización BI - Dashboard Directivo</h2>", unsafe_allow_html=True)

    col_bi_f1, col_bi_f2 = st.columns([1, 4])
    with col_bi_f1:
        st.markdown("**Filtros Rápidos**")
        univ_bi = st.selectbox("Universidad", ["Todas", "UNI", "UCH", "UCV", "UPN"], key="univ_bi_key")
        apoyo_bi = st.radio("Soporte Social Activo", ["Todos", "Sí", "No"])

    df_bi = df_active.copy()
    if univ_bi != "Todas":
        df_bi = df_bi[df_bi['Universidad'] == univ_bi]
    if apoyo_bi != "Todos":
        df_bi = df_bi[df_bi['Apoyo_Social_Activo'] == apoyo_bi]

    with col_bi_f2:
        dist_ans = df_bi.groupby('Distrito_Residencia')['Puntuacion_Ansiedad_GAD7'].mean().reset_index().sort_values(by='Puntuacion_Ansiedad_GAD7', ascending=False)
        fig_bar = px.bar(dist_ans, x='Distrito_Residencia', y='Puntuacion_Ansiedad_GAD7', title="Nivel de Ansiedad GAD-7 Promedio por Distrito",
                         color_discrete_sequence=["#3B82F6"])
        fig_bar.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_bar, use_container_width=True)

        col_bi_sub1, col_bi_sub2 = st.columns(2)
        with col_bi_sub1:
            casos_estres = df_bi[df_bi['Estres_Academico'] >= 7]
            fig_pie = px.pie(casos_estres, names="Apoyo_Social_Activo", title="Soporte Social Activo en Estudiantes con Estrés Alto (>=7)",
                             color_discrete_sequence=["#10B981", "#EF4444"])
            fig_pie.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bi_sub2:
            fig_trend = px.density_heatmap(df_bi, x="Puntuacion_Ansiedad_GAD7", y="Puntuacion_Depresion_PHQ9", 
                                           title="Densidad de Co-ocurrencia: Ansiedad vs Depresión",
                                           color_continuous_scale="Viridis")
            fig_trend.update_layout(plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig_trend, use_container_width=True)