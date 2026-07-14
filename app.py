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

# Inicializar variables de estado
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Pantalla General"

if 'dataset_crudo' not in st.session_state:
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

# PALETA DE COLORES ESTÉTICA
COLOR_PRIMARY = "#1E3A8A"   
COLOR_SUCCESS = "#059669"   
COLOR_WARNING = "#D97706"   
COLOR_DANGER = "#E11D48"    
COLOR_MUTED = "#64748B"     

# ==========================================
# ESTILOS CSS PERSONALIZADOS 
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F8FAFC; }}

    [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }}
    [data-testid="stSidebar"] * {{ color: #0F172A; }}
    hr {{ border-color: #E2E8F0 !important; }}

    .main-banner {{
        background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }}
    .main-banner h1 {{ color: {COLOR_PRIMARY}; font-size: 32px; font-weight: 800; margin-top: 0; }}
    .main-banner p {{ font-size: 16px; color: #475569; margin-bottom: 15px; }}

    /* TODOS LOS BOTONES: FONDO NEGRO Y LETRAS PLOMAS (GRIS) */
    .stButton>button, 
    [data-testid="baseButton-secondary"], 
    [data-testid="baseButton-primary"] {{
        background-color: #111827 !important; /* Negro/Gris muy oscuro */
        color: #D1D5DB !important; /* Gris plomo */
        border-radius: 8px;
        border: 1px solid #374151 !important;
        padding: 10px 15px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover, 
    [data-testid="baseButton-secondary"]:hover, 
    [data-testid="baseButton-primary"]:hover {{ 
        background-color: #1F2937 !important; 
        color: #F3F4F6 !important; 
    }}
    
    .step-header {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; margin-bottom: 10px; }}
    .step-title {{ font-size: 20px; font-weight: bold; color: #0F172A; margin-bottom: 5px; margin-top: 0px; }}
    .step-desc {{ font-size: 14px; color: {COLOR_MUTED}; height: 40px; margin-bottom: 15px; }}
    
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {{
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 10px;"><h1 style="font-size: 50px; margin: 0;">🧠</h1><h2 style="margin: 0; font-size: 20px; font-weight: 900; color: #1E3A8A !important;">SALUD MENTAL</h2><p style="font-size: 12px; color: #64748B !important; margin-top: -5px;">— LIMA NORTE —</p></div>', unsafe_allow_html=True)
    
    if st.button("⊞ Pantalla General", use_container_width=True): set_page("Pantalla General")
        
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #64748B !important; margin-bottom: 10px;'>7 PASOS DEL FLUJO BI</p>", unsafe_allow_html=True)
    
    opciones = [
        "① Fuentes de Datos", "② Staging Area", "③ Proceso ETL", "④ Data Warehouse",
        "⑤ Capa de IA Ética", "⑥ Capa Semántica & KPIs", "⑦ Visualización BI"
    ]
    
    for op in opciones:
        if st.session_state.current_page == op:
            st.markdown(f"<div style='background-color: #E2E8F0; border-left: 4px solid #1E293B; padding: 8px 10px; border-radius: 0px 5px 5px 0px; margin-bottom: 5px; cursor: pointer; font-size: 14px; font-weight: bold; color: #0F172A !important;'>{op}</div>", unsafe_allow_html=True)
        else:
            if st.button(op, key=op, use_container_width=True): set_page(op)

df_active = st.session_state['dataset_crudo']

# ==========================================
# PANTALLAS
# ==========================================

if st.session_state.current_page == "Pantalla General":
    st.markdown("""
    <div class="main-banner">
        <h1>PLATAFORMA BI INTEGRADA - SALUD MENTAL UNIVERSITARIA</h1>
        <p>Gobernanza cloud end-to-end: captura segura de encuestas, anonimización criptográfica, almacenamiento dimensional y analítica predictiva ética.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_PRIMARY};">Paso 1</span><span style="color: #94A3B8;">FUENTES DE DATOS</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Fuentes de Datos</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Captura de cuestionarios e historial académico de Lima Norte.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 1 →", key="btn1", use_container_width=True): set_page("① Fuentes de Datos"); st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #8B5CF6;">Paso 2</span><span style="color: #94A3B8;">STAGING AREA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Staging Area</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Control de calidad sintáctico y anonimización de identidades.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 2 →", key="btn2", use_container_width=True): set_page("② Staging Area"); st.rerun()
    with col3:
        with st.container(border=True):
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_SUCCESS};">Paso 3</span><span style="color: #94A3B8;">PROCESO ETL</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Proceso ETL</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Generación de indicadores clínicos (GAD y PHQ) normalizados.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 3 →", key="btn3", use_container_width=True): set_page("③ Proceso ETL"); st.rerun()
    with col4:
        with st.container(border=True):
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_WARNING};">Paso 4</span><span style="color: #94A3B8;">DATA WAREHOUSE</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Data Warehouse</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Persistencia relacional en Supabase con Modelo Snowflake.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 4 →", key="btn4", use_container_width=True): set_page("④ Data Warehouse"); st.rerun()

    st.write("")
    col5, col6, col7, _ = st.columns(4)
    with col5:
        with st.container(border=True):
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_DANGER};">Paso 5</span><span style="color: #94A3B8;">CAPA DE IA ÉTICA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa de IA Ética</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Cálculo predictivo de riesgo y protección de privacidad.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 5 →", key="btn5", use_container_width=True): set_page("⑤ Capa de IA Ética"); st.rerun()
    with col6:
        with st.container(border=True):
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_PRIMARY};">Paso 6</span><span style="color: #94A3B8;">CAPA SEMÁNTICA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa Semántica</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">KPIs ejecutivos, promedio de estrés, GAD-7 y PHQ-9.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 6 →", key="btn6", use_container_width=True): set_page("⑥ Capa Semántica & KPIs"); st.rerun()
    with col7:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #EC4899;">Paso 7</span><span style="color: #94A3B8;">VISUALIZACIÓN BI</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Visualización BI</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Dashboards y reportes analíticos consolidados.</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 7 →", key="btn7", use_container_width=True): set_page("⑦ Visualización BI"); st.rerun()

# --- PASO 1 ---
elif st.session_state.current_page == "① Fuentes de Datos":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Fuentes de datos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Carga archivos SISAP o encuestas (XLSX, XLS, CSV).</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        uploaded_file = st.file_uploader(" ", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'): df_active = pd.read_csv(uploaded_file)
            else: df_active = pd.read_excel(uploaded_file)
            st.session_state['dataset_crudo'] = df_active

    st.dataframe(df_active.head(10), use_container_width=True)
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ② Staging Area →", use_container_width=True): set_page("② Staging Area"); st.rerun()

# --- PASO 2 ---
elif st.session_state.current_page == "② Staging Area":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Staging Area</h2>", unsafe_allow_html=True)
    
    df_stage = df_active.copy()
    if 'Hash_ID' not in df_stage.columns: df_stage['Hash_ID'] = [f"sha256_{hash(str(x)) & 0xffffffff:08x}" for x in range(len(df_stage))]
    st.dataframe(df_stage.head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ③ Proceso ETL →", use_container_width=True): set_page("③ Proceso ETL"); st.rerun()

# --- PASO 3 ---
elif st.session_state.current_page == "③ Proceso ETL":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Proceso ETL</h2>", unsafe_allow_html=True)
    
    df_etl = df_active.copy()
    df_etl['Nivel_Ansiedad'] = pd.cut(df_etl['Puntuacion_Ansiedad_GAD7'], bins=[-1, 4, 9, 14, 21], labels=["Mínimo", "Leve", "Moderado", "Severo"])
    df_etl['Nivel_Depresion'] = pd.cut(df_etl['Puntuacion_Depresion_PHQ9'], bins=[-1, 4, 9, 14, 19, 27], labels=["Mínimo", "Leve", "Moderado", "Moderado-Severo", "Severo"])
    st.dataframe(df_etl[['Hash_ID', 'Universidad', 'Nivel_Ansiedad', 'Nivel_Depresion', 'Horas_Sueno_Promedio', 'Estres_Academico']].head(10), use_container_width=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ④ Data Warehouse →", use_container_width=True): set_page("④ Data Warehouse"); st.rerun()

# --- PASO 4 (DATA WAREHOUSE) ---
elif st.session_state.current_page == "④ Data Warehouse":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Data Warehouse en Supabase (Cloud PostgreSQL)</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .dw-container {
            background-color: #162032; 
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .dw-title-bar {
            background-color: #1E293B;
            padding: 10px 15px;
            border-radius: 6px;
            color: #10B981;
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
    <div class="dw-container">
        <div class="dw-title-bar">
            [COPO DE NIEVE] MODELO LOGICO FISICO: SNOWFLAKE SCHEMA (DATA WAREHOUSE) <br>
            <span style="color:#F8FAFC; font-weight:normal;">Cardinalidad: <span style="color:#10B981">1</span> Uno (Lado Principal / PK) &nbsp;|&nbsp; <span style="color:#A855F7">N</span> Muchas (Lado Hechos / FK)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    
    # FACT TABLE 
    fig.add_annotation(
        x=0.5, y=0.5, 
        text="<b>FACT_SALUD_MENTAL</b><br><span style='font-size:9px'>TABLA DE HECHOS (MÉTRICAS)</span><hr style='margin:5px 0; border-color:#3B82F6'>"
             "PK id_evaluacion<br>"
             "FK id_estudiante <span style='color:#A855F7'>N</span><br>"
             "FK id_universidad <span style='color:#A855F7'>N</span><br>"
             "FK id_tiempo <span style='color:#A855F7'>N</span><br><br>"
             "# score_gad7<br># score_phq9<br># horas_sueno",
        showarrow=False, 
        bordercolor="#3B82F6", borderwidth=2, bgcolor="#1E3A8A", font=dict(size=12, color="#FFFFFF"),
        width=200, align="left"
    )
    
    dim_style = dict(showarrow=False, bordercolor="#334155", borderwidth=1, bgcolor="#0F172A", font=dict(size=11, color="#E2E8F0"), align="left", width=160)
    
    # DIMENSIONES
    fig.add_annotation(x=0.1, y=0.5, text="<b>DIM_ESTUDIANTE</b><hr style='margin:5px 0; border-color:#334155'>PK id_estudiante <span style='color:#10B981'>1</span><br># edad<br># sexo<br># distrito", **dim_style)
    fig.add_shape(type="line", x0=0.25, y0=0.5, x1=0.35, y1=0.5, line=dict(color="#10B981", width=2))
    
    fig.add_annotation(x=0.9, y=0.7, text="<b>DIM_UNIVERSIDAD</b><hr style='margin:5px 0; border-color:#334155'>PK id_universidad <span style='color:#10B981'>1</span><br># nombre_sede", **dim_style)
    fig.add_shape(type="line", x0=0.65, y0=0.5, x1=0.75, y1=0.7, line=dict(color="#10B981", width=2))
    
    fig.add_annotation(x=0.9, y=0.3, text="<b>DIM_TIEMPO</b><hr style='margin:5px 0; border-color:#334155'>PK id_tiempo <span style='color:#10B981'>1</span><br># fecha<br># anio_mes", **dim_style)
    fig.add_shape(type="line", x0=0.65, y0=0.5, x1=0.75, y1=0.3, line=dict(color="#A855F7", width=2))

    fig.update_layout(
        xaxis=dict(visible=False, range=[0, 1]), yaxis=dict(visible=False, range=[0, 1]), 
        height=350, margin=dict(l=0,r=0,t=0,b=0), 
        plot_bgcolor="#162032", paper_bgcolor="#162032"
    )
    
    st.markdown("<div style='margin-top:-60px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Subtítulo de Acciones con diseño específico
    st.markdown("<h3 style='color: #FFFFFF; margin-top: 10px; margin-bottom: 20px; background-color: #3B82F6; padding: 10px; border-radius: 5px; width: fit-content;'>Acciones de Carga y Mantenimiento</h3>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1: st.button("Guardar Data Warehouse en Supabase", use_container_width=True)
    with col_a2: st.button("Reconstruir Tablas (Vaciar Supabase)", use_container_width=True)

    st.write("")
    st.dataframe(df_active.head(10), use_container_width=True) # Agregamos la tabla de nuevo
    st.write("")
    
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑤ Capa de IA →", use_container_width=True): set_page("⑤ Capa de IA Ética"); st.rerun()

# --- PASO 5 ---
elif st.session_state.current_page == "⑤ Capa de IA Ética":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Capa de IA Ética</h2>", unsafe_allow_html=True)
    
    df_pred = df_active.copy()
    score_riesgo = (df_pred['Puntuacion_Ansiedad_GAD7'] * 0.4 + df_pred['Puntuacion_Depresion_PHQ9'] * 0.4 + df_pred['Estres_Academico'] * 0.2) / 25
    df_pred['Prob_Riesgo'] = np.clip(score_riesgo, 0.05, 0.98).round(3)
    df_pred['Riesgo_Predicho_IA'] = np.where(df_pred['Prob_Riesgo'] > 0.65, "Riesgo Alto", np.where(df_pred['Prob_Riesgo'] > 0.35, "Riesgo Moderado", "Riesgo Bajo"))

    col_ia1, col_ia2 = st.columns(2)
    with col_ia1:
        fig_prob = px.histogram(df_pred, x="Prob_Riesgo", color="Riesgo_Predicho_IA", title="Distribución Probabilidades Riesgo", color_discrete_map={"Riesgo Alto": COLOR_DANGER, "Riesgo Moderado": COLOR_WARNING, "Riesgo Bajo": COLOR_SUCCESS})
        fig_prob.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#1E293B", size=11))
        st.plotly_chart(fig_prob, use_container_width=True)
    with col_ia2:
        fig_scatter = px.scatter(df_pred, x="Horas_Sueno_Promedio", y="Estres_Academico", color="Riesgo_Predicho_IA", title="Sueño vs Estrés Académico", color_discrete_map={"Riesgo Alto": COLOR_DANGER, "Riesgo Moderado": COLOR_WARNING, "Riesgo Bajo": COLOR_SUCCESS})
        fig_scatter.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#1E293B", size=11))
        st.plotly_chart(fig_scatter, use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑥ Capa Semántica & KPIs →", use_container_width=True): set_page("⑥ Capa Semántica & KPIs"); st.rerun()

# --- PASO 6 ---
elif st.session_state.current_page == "⑥ Capa Semántica & KPIs":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Capa Semántica & KPIs</h2>", unsafe_allow_html=True)
    
    st.dataframe(df_active.head(10), use_container_width=True)

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑦ Visualización BI →", use_container_width=True): set_page("⑦ Visualización BI"); st.rerun()

# --- PASO 7 ---
elif st.session_state.current_page == "⑦ Visualización BI":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown("<h2 style='color: #0F172A;'>Visualización BI - Dashboard Directivo</h2>", unsafe_allow_html=True)
    
    col_bi_f1, col_bi_f2 = st.columns([1, 4])
    with col_bi_f1:
        st.markdown("**Filtros Rápidos**")
        univ_bi = st.selectbox("Universidad", ["Todas", "UNI", "UCH", "UCV", "UPN"])
        apoyo_bi = st.radio("Soporte Social Activo", ["Todos", "Sí", "No"])

    df_bi = df_active.copy()
    if univ_bi != "Todas": df_bi = df_bi[df_bi['Universidad'] == univ_bi]
    if apoyo_bi != "Todos": df_bi = df_bi[df_bi['Apoyo_Social_Activo'] == apoyo_bi]

    with col_bi_f2:
        dist_ans = df_bi.groupby('Distrito_Residencia')['Puntuacion_Ansiedad_GAD7'].mean().reset_index()
        fig_bar = px.bar(dist_ans, x='Distrito_Residencia', y='Puntuacion_Ansiedad_GAD7', title="Ansiedad GAD-7 Promedio por Distrito", color_discrete_sequence=[COLOR_PRIMARY])
        fig_bar.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#1E293B", size=11))
        st.plotly_chart(fig_bar, use_container_width=True)