import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Analítica Salud Mental - Lima Norte",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PALETA DE COLORES ESTÉTICA (tema único, usado en CSS y en gráficos)
# ==========================================
COLOR_PRIMARY = "#1E3A8A"    # Azul institucional
COLOR_ACCENT = "#3B82F6"     # Azul claro (acentos / hover)
COLOR_SUCCESS = "#059669"    # Verde - riesgo bajo / positivo
COLOR_WARNING = "#D97706"    # Ámbar - riesgo moderado
COLOR_DANGER = "#E11D48"     # Rojo - riesgo crítico
COLOR_MUTED = "#64748B"      # Gris azulado - texto secundario
COLOR_BG = "#F1F5F9"         # Fondo general
COLOR_CARD = "#FFFFFF"       # Fondo de tarjetas
COLOR_BORDER = "#E2E8F0"     # Bordes
COLOR_TEXT = "#0F172A"       # Texto principal

RISK_COLORS = {"Riesgo Alto": COLOR_DANGER, "Riesgo Moderado": COLOR_WARNING, "Riesgo Bajo": COLOR_SUCCESS}

# Columnas requeridas del dataset (esquema esperado por todo el flujo BI)
COLUMNAS_REQUERIDAS = [
    'Universidad', 'Edad', 'Sexo', 'Distrito_Residencia', 'Ciclo_Academico',
    'Puntuacion_Ansiedad_GAD7', 'Puntuacion_Depresion_PHQ9', 'Estres_Academico',
    'Horas_Sueno_Promedio', 'Apoyo_Social_Activo'
]

# ==========================================
# ESTADO DE SESIÓN
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Pantalla General"

# La app arranca SIN datos. El usuario debe cargarlos en el Paso 1
# (o usar el botón de dataset de ejemplo, que es una acción explícita).
if 'dataset_crudo' not in st.session_state:
    st.session_state['dataset_crudo'] = None

if 'upload_error' not in st.session_state:
    st.session_state['upload_error'] = None


def set_page(page_name):
    st.session_state.current_page = page_name


# ==========================================
# FUNCIONES AUXILIARES (compartidas por todos los pasos → misma fuente de verdad)
# ==========================================
def generar_dataset_ejemplo(n_samples=500):
    """Genera un dataset sintético SOLO cuando el usuario lo solicita explícitamente."""
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        'Universidad': rng.choice(["UNI", "UCH", "UCV", "UPN"], n_samples),
        'Edad': rng.integers(16, 36, n_samples),
        'Sexo': rng.choice(["Masculino", "Femenino"], n_samples),
        'Distrito_Residencia': rng.choice(
            ["Los Olivos", "San Martín de Porres", "Comas", "Carabayllo", "Independencia"], n_samples),
        'Ciclo_Academico': rng.integers(1, 11, n_samples),
        'Puntuacion_Ansiedad_GAD7': rng.integers(0, 22, n_samples),
        'Puntuacion_Depresion_PHQ9': rng.integers(0, 28, n_samples),
        'Estres_Academico': rng.integers(1, 11, n_samples),
        'Horas_Sueno_Promedio': np.round(rng.uniform(4.0, 9.5, n_samples), 1),
        'Apoyo_Social_Activo': rng.choice(["Sí", "No"], n_samples, p=[0.75, 0.25])
    })
    return anonimizar(df)


def anonimizar(df):
    """Genera un Hash_ID estable e irreversible (SHA-256) por fila, si no existe."""
    df = df.copy()
    if 'Hash_ID' not in df.columns:
        df.insert(0, 'Hash_ID', [
            hashlib.sha256(f"{i}-{row.to_json()}".encode()).hexdigest()[:16]
            for i, row in df.iterrows()
        ])
    return df


def validar_dataset(df):
    """Verifica que existan las columnas mínimas para que el flujo BI funcione."""
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    return (len(faltantes) == 0, faltantes)


def calcular_niveles_clinicos(df):
    """Añade niveles clínicos (ETL) de forma consistente en todo el flujo."""
    df = df.copy()
    df['Nivel_Ansiedad'] = pd.cut(
        df['Puntuacion_Ansiedad_GAD7'], bins=[-1, 4, 9, 14, 21],
        labels=["Mínimo", "Leve", "Moderado", "Severo"])
    df['Nivel_Depresion'] = pd.cut(
        df['Puntuacion_Depresion_PHQ9'], bins=[-1, 4, 9, 14, 19, 27],
        labels=["Mínimo", "Leve", "Moderado", "Moderado-Severo", "Severo"])
    return df


def calcular_riesgo_ia(df):
    """Capa de IA Ética: score y clasificación de riesgo, reutilizado en Pasos 5, 6 y 7."""
    df = df.copy()
    score = (df['Puntuacion_Ansiedad_GAD7'] * 0.4 +
             df['Puntuacion_Depresion_PHQ9'] * 0.4 +
             df['Estres_Academico'] * 2.0) / 25
    df['Prob_Riesgo'] = np.clip(score, 0.05, 0.98).round(3)
    df['Riesgo_Predicho_IA'] = np.where(
        df['Prob_Riesgo'] > 0.65, "Riesgo Alto",
        np.where(df['Prob_Riesgo'] > 0.35, "Riesgo Moderado", "Riesgo Bajo"))
    return df


def preparar_dataset_completo(df):
    """Pipeline único: anonimizar → niveles clínicos → riesgo IA. Todo el flujo usa esto."""
    df = anonimizar(df)
    df = calcular_niveles_clinicos(df)
    df = calcular_riesgo_ia(df)
    return df


def aplicar_tema_grafico(fig, title=None):
    """Aplica un tema visual consistente a TODOS los gráficos Plotly de la app."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=COLOR_TEXT, family="Arial, sans-serif")) if title else None,
        plot_bgcolor=COLOR_CARD,
        paper_bgcolor=COLOR_CARD,
        font=dict(color=COLOR_TEXT, size=12, family="Arial, sans-serif"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        xaxis=dict(gridcolor=COLOR_BORDER, zerolinecolor=COLOR_BORDER),
        yaxis=dict(gridcolor=COLOR_BORDER, zerolinecolor=COLOR_BORDER),
    )
    return fig


def sin_datos(mensaje="Todavía no hay datos cargados."):
    """Estado vacío consistente en cualquier paso del flujo."""
    st.markdown(f"""
    <div style="background:{COLOR_CARD}; border:1px dashed {COLOR_BORDER}; border-radius:12px;
                padding:40px; text-align:center; margin-top:10px;">
        <div style="font-size:40px; margin-bottom:10px;">📭</div>
        <p style="color:{COLOR_TEXT}; font-weight:700; font-size:16px; margin-bottom:6px;">{mensaje}</p>
        <p style="color:{COLOR_MUTED}; font-size:13px;">Ve al Paso ① Fuentes de Datos para cargar un archivo o usar el dataset de ejemplo.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ir a ① Fuentes de Datos", key=f"goto_upload_{mensaje[:10]}"):
        set_page("① Fuentes de Datos")
        st.rerun()


def metric_card(col, label, value, color, suffix="", icon="●"):
    with col:
        st.markdown(f"""
        <div style="background:{COLOR_CARD}; border:1px solid {COLOR_BORDER}; border-top:4px solid {color};
                    border-radius:10px; padding:18px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.03); height:110px;">
            <div style="color:{COLOR_MUTED}; font-size:12px; font-weight:700; letter-spacing:.3px; text-transform:uppercase;">{icon} {label}</div>
            <div style="color:{COLOR_TEXT}; font-size:28px; font-weight:800; margin-top:8px;">{value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# ESTILOS CSS PERSONALIZADOS (tema unificado)
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; }}

    [data-testid="stSidebar"] {{
        background-color: {COLOR_CARD} !important;
        border-right: 1px solid {COLOR_BORDER};
    }}
    [data-testid="stSidebar"] * {{ color: {COLOR_TEXT}; }}
    hr {{ border-color: {COLOR_BORDER} !important; }}

    .main-banner {{
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #16255E 100%);
        border-radius: 14px;
        padding: 34px 36px; margin-bottom: 26px; box-shadow: 0 8px 20px rgba(30,58,138,0.18);
    }}
    .main-banner h1 {{ color: #FFFFFF; font-size: 30px; font-weight: 800; margin-top: 0; }}
    .main-banner p {{ font-size: 15px; color: #CBD5E1; margin-bottom: 0; max-width: 780px; }}

    .status-pill {{
        display:inline-block; padding: 5px 14px; border-radius: 999px; font-size: 12px; font-weight: 700;
        margin-top: 14px;
    }}

    /* BOTONES: acento azul institucional, texto blanco */
    .stButton>button,
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"] {{
        background-color: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid {COLOR_PRIMARY} !important;
        padding: 10px 15px;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    .stButton>button:hover,
    [data-testid="baseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover {{
        background-color: {COLOR_ACCENT} !important;
        border-color: {COLOR_ACCENT} !important;
        color: #FFFFFF !important;
    }}

    .step-header {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: bold; margin-bottom: 10px; }}
    .step-title {{ font-size: 20px; font-weight: bold; color: {COLOR_TEXT}; margin-bottom: 5px; margin-top: 0px; }}
    .step-desc {{ font-size: 14px; color: {COLOR_MUTED}; height: 40px; margin-bottom: 15px; }}

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {{
        background-color: {COLOR_CARD};
        box-shadow: 0 4px 10px rgba(15,23,42,0.04);
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
    }}

    [data-testid="stMetricValue"] {{ color: {COLOR_PRIMARY}; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(
        f'<div style="text-align: center; margin-bottom: 10px;">'
        f'<h1 style="font-size: 50px; margin: 0;">🧠</h1>'
        f'<h2 style="margin: 0; font-size: 20px; font-weight: 900; color: {COLOR_PRIMARY} !important;">SALUD MENTAL</h2>'
        f'<p style="font-size: 12px; color: {COLOR_MUTED} !important; margin-top: -5px;">— LIMA NORTE —</p></div>',
        unsafe_allow_html=True
    )

    if st.button("⊞ Pantalla General", use_container_width=True):
        set_page("Pantalla General")

    # Indicador de estado de datos, visible en todo momento
    _df_state = st.session_state['dataset_crudo']
    if _df_state is None or len(_df_state) == 0:
        st.markdown(
            f"<div style='background:#FEF3F2; border:1px solid #FECDD3; color:{COLOR_DANGER}; "
            f"font-size:12px; font-weight:700; padding:8px 10px; border-radius:8px; text-align:center; margin:8px 0;'>"
            f"⚠️ Sin datos cargados</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='background:#ECFDF5; border:1px solid #A7F3D0; color:{COLOR_SUCCESS}; "
            f"font-size:12px; font-weight:700; padding:8px 10px; border-radius:8px; text-align:center; margin:8px 0;'>"
            f"✅ {len(_df_state)} registros cargados</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 11px; font-weight: bold; color: {COLOR_MUTED} !important; margin-bottom: 10px;'>7 PASOS DEL FLUJO BI</p>", unsafe_allow_html=True)

    opciones = [
        "① Fuentes de Datos", "② Staging Area", "③ Proceso ETL", "④ Data Warehouse",
        "⑤ Capa de IA Ética", "⑥ Capa Semántica & KPIs", "⑦ Visualización BI"
    ]

    for op in opciones:
        if st.session_state.current_page == op:
            st.markdown(
                f"<div style='background-color: #DBEAFE; border-left: 4px solid {COLOR_PRIMARY}; padding: 8px 10px; "
                f"border-radius: 0px 5px 5px 0px; margin-bottom: 5px; font-size: 14px; font-weight: bold; "
                f"color: {COLOR_PRIMARY} !important;'>{op}</div>", unsafe_allow_html=True)
        else:
            if st.button(op, key=op, use_container_width=True):
                set_page(op)

# Fuente única de verdad para todo el flujo
df_raw = st.session_state['dataset_crudo']
hay_datos = df_raw is not None and len(df_raw) > 0

# ==========================================
# PANTALLAS
# ==========================================

if st.session_state.current_page == "Pantalla General":
    estado_html = (
        f'<span class="status-pill" style="background:#ECFDF5; color:{COLOR_SUCCESS};">✅ {len(df_raw)} registros activos</span>'
        if hay_datos else
        f'<span class="status-pill" style="background:#FEF3F2; color:{COLOR_DANGER};">⚠️ Sin datos cargados — comienza en el Paso ①</span>'
    )
    st.markdown(f"""
    <div class="main-banner">
        <h1>PLATAFORMA BI INTEGRADA - SALUD MENTAL UNIVERSITARIA</h1>
        <p>Gobernanza cloud end-to-end: captura segura de encuestas, anonimización criptográfica, almacenamiento dimensional y analítica predictiva ética.</p>
        {estado_html}
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
            st.markdown(f'<div class="step-header"><span style="color: {COLOR_ACCENT};">Paso 2</span><span style="color: #94A3B8;">STAGING AREA</span></div>', unsafe_allow_html=True)
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

# --- PASO 1: FUENTES DE DATOS ---
elif st.session_state.current_page == "① Fuentes de Datos":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Fuentes de datos</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLOR_MUTED};'>Carga archivos SISAP o encuestas (XLSX, XLS, CSV). Columnas esperadas: "
                f"<code>{', '.join(COLUMNAS_REQUERIDAS)}</code></p>", unsafe_allow_html=True)

    with st.container(border=True):
        col_up, col_demo = st.columns([3, 1])
        with col_up:
            uploaded_file = st.file_uploader("Sube tu archivo", type=["csv", "xlsx", "xls"], label_visibility="collapsed")
        with col_demo:
            if st.button("📊 Usar dataset de ejemplo", use_container_width=True):
                st.session_state['dataset_crudo'] = generar_dataset_ejemplo()
                st.session_state['upload_error'] = None
                st.rerun()

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    nuevo_df = pd.read_csv(uploaded_file)
                else:
                    nuevo_df = pd.read_excel(uploaded_file)

                es_valido, faltantes = validar_dataset(nuevo_df)
                if not es_valido:
                    st.session_state['upload_error'] = (
                        f"El archivo no tiene las columnas requeridas. Faltan: {', '.join(faltantes)}"
                    )
                else:
                    st.session_state['dataset_crudo'] = nuevo_df
                    st.session_state['upload_error'] = None
                    st.success(f"✅ Archivo cargado correctamente: {len(nuevo_df)} registros.")
            except Exception as e:
                st.session_state['upload_error'] = f"No se pudo leer el archivo: {e}"

        if st.session_state.get('upload_error'):
            st.error(st.session_state['upload_error'])

    if hay_datos:
        st.markdown(f"<p style='color:{COLOR_MUTED}; font-size:13px; margin-top:16px;'>Vista previa (primeras 10 filas):</p>", unsafe_allow_html=True)
        st.dataframe(df_raw.head(10), use_container_width=True)
        col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
        with col_c2:
            if st.button("Siguiente Paso: ② Staging Area →", use_container_width=True): set_page("② Staging Area"); st.rerun()
    else:
        sin_datos("Aún no has cargado ningún archivo.")

# --- PASO 2: STAGING AREA ---
elif st.session_state.current_page == "② Staging Area":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Staging Area</h2>", unsafe_allow_html=True)

    if not hay_datos:
        sin_datos()
    else:
        df_stage = anonimizar(df_raw)
        n_duplicados = df_stage.duplicated(subset=[c for c in COLUMNAS_REQUERIDAS if c in df_stage.columns]).sum()
        n_nulos = df_stage[COLUMNAS_REQUERIDAS].isna().sum().sum() if validar_dataset(df_stage)[0] else 0

        m1, m2, m3, m4 = st.columns(4)
        metric_card(m1, "Registros totales", len(df_stage), COLOR_PRIMARY)
        metric_card(m2, "Duplicados detectados", int(n_duplicados), COLOR_WARNING)
        metric_card(m3, "Valores nulos", int(n_nulos), COLOR_DANGER if n_nulos > 0 else COLOR_SUCCESS)
        metric_card(m4, "IDs anonimizados", len(df_stage), COLOR_SUCCESS, icon="🔒")

        st.write("")
        st.markdown(f"<p style='color:{COLOR_MUTED}; font-size:13px;'>Los identificadores se convirtieron a hash SHA-256 truncado — no reversible a la identidad original.</p>", unsafe_allow_html=True)
        st.dataframe(df_stage.head(10), use_container_width=True)

        col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
        with col_c2:
            if st.button("Siguiente Paso: ③ Proceso ETL →", use_container_width=True): set_page("③ Proceso ETL"); st.rerun()

# --- PASO 3: PROCESO ETL ---
elif st.session_state.current_page == "③ Proceso ETL":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Proceso ETL</h2>", unsafe_allow_html=True)

    if not hay_datos:
        sin_datos()
    else:
        df_etl = calcular_niveles_clinicos(anonimizar(df_raw))
        st.dataframe(
            df_etl[['Hash_ID', 'Universidad', 'Nivel_Ansiedad', 'Nivel_Depresion', 'Horas_Sueno_Promedio', 'Estres_Academico']].head(10),
            use_container_width=True
        )

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            conteo_ans = df_etl['Nivel_Ansiedad'].value_counts().reindex(["Mínimo", "Leve", "Moderado", "Severo"]).fillna(0)
            fig_ans = px.bar(x=conteo_ans.index, y=conteo_ans.values, labels={'x': 'Nivel de Ansiedad', 'y': 'Estudiantes'},
                              color=conteo_ans.index,
                              color_discrete_map={"Mínimo": COLOR_SUCCESS, "Leve": COLOR_ACCENT, "Moderado": COLOR_WARNING, "Severo": COLOR_DANGER})
            fig_ans.update_layout(showlegend=False)
            st.plotly_chart(aplicar_tema_grafico(fig_ans, "Distribución — Nivel de Ansiedad (GAD-7)"), use_container_width=True)
        with col_g2:
            conteo_dep = df_etl['Nivel_Depresion'].value_counts().reindex(["Mínimo", "Leve", "Moderado", "Moderado-Severo", "Severo"]).fillna(0)
            fig_dep = px.bar(x=conteo_dep.index, y=conteo_dep.values, labels={'x': 'Nivel de Depresión', 'y': 'Estudiantes'},
                              color=conteo_dep.index,
                              color_discrete_map={"Mínimo": COLOR_SUCCESS, "Leve": COLOR_ACCENT, "Moderado": COLOR_WARNING, "Moderado-Severo": "#FB923C", "Severo": COLOR_DANGER})
            fig_dep.update_layout(showlegend=False)
            st.plotly_chart(aplicar_tema_grafico(fig_dep, "Distribución — Nivel de Depresión (PHQ-9)"), use_container_width=True)

        col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
        with col_c2:
            if st.button("Siguiente Paso: ④ Data Warehouse →", use_container_width=True): set_page("④ Data Warehouse"); st.rerun()

# --- PASO 4 (DATA WAREHOUSE) ---
elif st.session_state.current_page == "④ Data Warehouse":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Data Warehouse en Supabase (Cloud PostgreSQL)</h2>", unsafe_allow_html=True)

    st.markdown(f"""
    <style>
        .dw-container {{
            background-color: #0F1A2E;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .dw-title-bar {{
            background-color: #16213B;
            padding: 10px 15px;
            border-radius: 6px;
            color: {COLOR_SUCCESS};
            font-size: 11px;
            font-weight: bold;
            margin-bottom: 20px;
        }}
    </style>
    <div class="dw-container">
        <div class="dw-title-bar">
            [COPO DE NIEVE] MODELO LÓGICO FÍSICO: SNOWFLAKE SCHEMA (DATA WAREHOUSE) <br>
            <span style="color:#F8FAFC; font-weight:normal;">Cardinalidad: <span style="color:{COLOR_SUCCESS}">1</span> Uno (Lado Principal / PK) &nbsp;|&nbsp; <span style="color:#A855F7">N</span> Muchas (Lado Hechos / FK)</span>
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
        bordercolor=COLOR_ACCENT, borderwidth=2, bgcolor=COLOR_PRIMARY, font=dict(size=12, color="#FFFFFF"),
        width=200, align="left"
    )

    dim_style = dict(showarrow=False, bordercolor="#334155", borderwidth=1, bgcolor="#0F172A", font=dict(size=11, color="#E2E8F0"), align="left", width=160)

    fig.add_annotation(x=0.1, y=0.5, text=f"<b>DIM_ESTUDIANTE</b><hr style='margin:5px 0; border-color:#334155'>PK id_estudiante <span style='color:{COLOR_SUCCESS}'>1</span><br># edad<br># sexo<br># distrito", **dim_style)
    fig.add_shape(type="line", x0=0.25, y0=0.5, x1=0.35, y1=0.5, line=dict(color=COLOR_SUCCESS, width=2))

    fig.add_annotation(x=0.9, y=0.7, text=f"<b>DIM_UNIVERSIDAD</b><hr style='margin:5px 0; border-color:#334155'>PK id_universidad <span style='color:{COLOR_SUCCESS}'>1</span><br># nombre_sede", **dim_style)
    fig.add_shape(type="line", x0=0.65, y0=0.5, x1=0.75, y1=0.7, line=dict(color=COLOR_SUCCESS, width=2))

    fig.add_annotation(x=0.9, y=0.3, text=f"<b>DIM_TIEMPO</b><hr style='margin:5px 0; border-color:#334155'>PK id_tiempo <span style='color:{COLOR_SUCCESS}'>1</span><br># fecha<br># anio_mes", **dim_style)
    fig.add_shape(type="line", x0=0.65, y0=0.5, x1=0.75, y1=0.3, line=dict(color="#A855F7", width=2))

    fig.update_layout(
        xaxis=dict(visible=False, range=[0, 1]), yaxis=dict(visible=False, range=[0, 1]),
        height=350, margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#0F1A2E", paper_bgcolor="#0F1A2E"
    )

    st.markdown("<div style='margin-top:-60px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: #FFFFFF; margin-top: 10px; margin-bottom: 20px; background-color: {COLOR_PRIMARY}; padding: 10px; border-radius: 5px; width: fit-content;'>Acciones de Carga y Mantenimiento</h3>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1: st.button("Guardar Data Warehouse en Supabase", use_container_width=True, disabled=not hay_datos)
    with col_a2: st.button("Reconstruir Tablas (Vaciar Supabase)", use_container_width=True, disabled=not hay_datos)

    st.write("")
    if hay_datos:
        st.dataframe(df_raw.head(10), use_container_width=True)
    else:
        sin_datos()
    st.write("")

    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("Siguiente Paso: ⑤ Capa de IA →", use_container_width=True): set_page("⑤ Capa de IA Ética"); st.rerun()

# --- PASO 5: CAPA DE IA ÉTICA ---
elif st.session_state.current_page == "⑤ Capa de IA Ética":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Capa de IA Ética</h2>", unsafe_allow_html=True)

    if not hay_datos:
        sin_datos()
    else:
        df_pred = calcular_riesgo_ia(df_raw)

        col_ia1, col_ia2 = st.columns(2)
        with col_ia1:
            fig_prob = px.histogram(df_pred, x="Prob_Riesgo", color="Riesgo_Predicho_IA",
                                     color_discrete_map=RISK_COLORS)
            st.plotly_chart(aplicar_tema_grafico(fig_prob, "Distribución de Probabilidades de Riesgo"), use_container_width=True)
        with col_ia2:
            fig_scatter = px.scatter(df_pred, x="Horas_Sueno_Promedio", y="Estres_Academico",
                                      color="Riesgo_Predicho_IA", color_discrete_map=RISK_COLORS)
            st.plotly_chart(aplicar_tema_grafico(fig_scatter, "Sueño vs Estrés Académico"), use_container_width=True)

        st.markdown(f"<p style='color:{COLOR_MUTED}; font-size:13px;'>Modelo explicable: el riesgo pondera ansiedad (40%), depresión (40%) y estrés académico (20%). "
                    f"El token de canalización permite que un psicólogo atienda casos críticos sin conocer la identidad del estudiante.</p>", unsafe_allow_html=True)

        col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
        with col_c2:
            if st.button("Siguiente Paso: ⑥ Capa Semántica & KPIs →", use_container_width=True): set_page("⑥ Capa Semántica & KPIs"); st.rerun()

# --- PASO 6: CAPA SEMÁNTICA & KPIS ---
elif st.session_state.current_page == "⑥ Capa Semántica & KPIs":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Capa Semántica & KPIs</h2>", unsafe_allow_html=True)

    if not hay_datos:
        sin_datos()
    else:
        df_kpi = preparar_dataset_completo(df_raw)

        pct_riesgo_critico = (df_kpi['Riesgo_Predicho_IA'] == 'Riesgo Alto').mean() * 100
        pct_apoyo = (df_kpi['Apoyo_Social_Activo'].astype(str).str.strip().str.lower().isin(['sí', 'si', 'true', '1'])).mean() * 100

        st.markdown(f"<p style='color:{COLOR_MUTED}; font-size:12px; font-weight:700; text-transform:uppercase; margin-bottom:8px;'>KPIs Ejecutivos</p>", unsafe_allow_html=True)
        r1c1, r1c2, r1c3, r1c4 = st.columns(4)
        metric_card(r1c1, "Estudiantes evaluados", len(df_kpi), COLOR_PRIMARY, icon="👥")
        metric_card(r1c2, "GAD-7 promedio", round(df_kpi['Puntuacion_Ansiedad_GAD7'].mean(), 1), COLOR_ACCENT, icon="📈")
        metric_card(r1c3, "PHQ-9 promedio", round(df_kpi['Puntuacion_Depresion_PHQ9'].mean(), 1), COLOR_WARNING, icon="📉")
        metric_card(r1c4, "Estrés académico prom.", round(df_kpi['Estres_Academico'].mean(), 1), COLOR_DANGER, icon="🔥")

        st.write("")
        r2c1, r2c2, r2c3, r2c4 = st.columns(4)
        metric_card(r2c1, "Horas de sueño prom.", round(df_kpi['Horas_Sueno_Promedio'].mean(), 1), COLOR_SUCCESS, suffix=" h", icon="😴")
        metric_card(r2c2, "Con apoyo social activo", round(pct_apoyo, 1), COLOR_SUCCESS, suffix="%", icon="🤝")
        metric_card(r2c3, "En riesgo crítico (IA)", round(pct_riesgo_critico, 1), COLOR_DANGER, suffix="%", icon="🚨")
        metric_card(r2c4, "Universidades activas", df_kpi['Universidad'].nunique(), COLOR_PRIMARY, icon="🏫")

        st.write("")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            kpi_univ = df_kpi.groupby('Universidad', as_index=False)[['Puntuacion_Ansiedad_GAD7', 'Puntuacion_Depresion_PHQ9']].mean()
            fig_kpi_univ = px.bar(kpi_univ, x='Universidad', y=['Puntuacion_Ansiedad_GAD7', 'Puntuacion_Depresion_PHQ9'],
                                   barmode='group', labels={'value': 'Puntuación promedio', 'variable': 'Indicador'},
                                   color_discrete_sequence=[COLOR_PRIMARY, COLOR_DANGER])
            st.plotly_chart(aplicar_tema_grafico(fig_kpi_univ, "GAD-7 y PHQ-9 promedio por Universidad"), use_container_width=True)
        with col_g2:
            riesgo_counts = df_kpi['Riesgo_Predicho_IA'].value_counts().reset_index()
            riesgo_counts.columns = ['Riesgo', 'Estudiantes']
            fig_riesgo = px.pie(riesgo_counts, names='Riesgo', values='Estudiantes', hole=0.55,
                                 color='Riesgo', color_discrete_map=RISK_COLORS)
            st.plotly_chart(aplicar_tema_grafico(fig_riesgo, "Distribución de Niveles de Riesgo (IA)"), use_container_width=True)

        st.write("")
        with st.expander("Ver tabla semántica (10 primeras filas)"):
            st.dataframe(df_kpi.head(10), use_container_width=True)

        col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
        with col_c2:
            if st.button("Siguiente Paso: ⑦ Visualización BI →", use_container_width=True): set_page("⑦ Visualización BI"); st.rerun()

# --- PASO 7: VISUALIZACIÓN BI ---
elif st.session_state.current_page == "⑦ Visualización BI":
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: {COLOR_TEXT};'>Visualización BI - Dashboard Directivo</h2>", unsafe_allow_html=True)

    if not hay_datos:
        sin_datos()
    else:
        df_full = preparar_dataset_completo(df_raw)

        col_bi_f1, col_bi_f2 = st.columns([1, 4])
        with col_bi_f1:
            with st.container(border=True):
                st.markdown("**Filtros Rápidos**")
                univ_opciones = ["Todas"] + sorted(df_full['Universidad'].dropna().unique().tolist())
                univ_bi = st.selectbox("Universidad", univ_opciones)
                apoyo_bi = st.radio("Soporte Social Activo", ["Todos", "Sí", "No"])
                riesgo_bi = st.multiselect("Nivel de Riesgo (IA)", ["Riesgo Bajo", "Riesgo Moderado", "Riesgo Alto"],
                                            default=["Riesgo Bajo", "Riesgo Moderado", "Riesgo Alto"])

        df_bi = df_full.copy()
        if univ_bi != "Todas": df_bi = df_bi[df_bi['Universidad'] == univ_bi]
        if apoyo_bi != "Todos": df_bi = df_bi[df_bi['Apoyo_Social_Activo'] == apoyo_bi]
        if riesgo_bi: df_bi = df_bi[df_bi['Riesgo_Predicho_IA'].isin(riesgo_bi)]

        with col_bi_f2:
            if len(df_bi) == 0:
                st.warning("No hay registros que coincidan con los filtros seleccionados.")
            else:
                m1, m2, m3 = st.columns(3)
                metric_card(m1, "Registros filtrados", len(df_bi), COLOR_PRIMARY)
                metric_card(m2, "GAD-7 promedio", round(df_bi['Puntuacion_Ansiedad_GAD7'].mean(), 1), COLOR_ACCENT)
                metric_card(m3, "% Riesgo alto", round((df_bi['Riesgo_Predicho_IA'] == 'Riesgo Alto').mean() * 100, 1), COLOR_DANGER, suffix="%")

        if len(df_bi) > 0:
            st.write("")
            col_a, col_b = st.columns(2)
            with col_a:
                dist_ans = df_bi.groupby('Distrito_Residencia', as_index=False)['Puntuacion_Ansiedad_GAD7'].mean()
                dist_ans = dist_ans.sort_values('Puntuacion_Ansiedad_GAD7', ascending=False)
                fig_bar = px.bar(dist_ans, x='Distrito_Residencia', y='Puntuacion_Ansiedad_GAD7',
                                  color_discrete_sequence=[COLOR_PRIMARY])
                st.plotly_chart(aplicar_tema_grafico(fig_bar, "Ansiedad GAD-7 Promedio por Distrito"), use_container_width=True)
            with col_b:
                fig_box = px.box(df_bi, x='Universidad', y='Puntuacion_Depresion_PHQ9', color='Universidad',
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                fig_box.update_layout(showlegend=False)
                st.plotly_chart(aplicar_tema_grafico(fig_box, "Distribución de PHQ-9 por Universidad"), use_container_width=True)

            col_c, col_d = st.columns(2)
            with col_c:
                fig_sleep = px.scatter(df_bi, x='Horas_Sueno_Promedio', y='Estres_Academico',
                                        color='Riesgo_Predicho_IA', color_discrete_map=RISK_COLORS)
                st.plotly_chart(aplicar_tema_grafico(fig_sleep, "Sueño vs Estrés Académico"), use_container_width=True)
            with col_d:
                riesgo_counts = df_bi['Riesgo_Predicho_IA'].value_counts().reset_index()
                riesgo_counts.columns = ['Riesgo', 'Estudiantes']
                fig_pie = px.pie(riesgo_counts, names='Riesgo', values='Estudiantes', hole=0.55,
                                  color='Riesgo', color_discrete_map=RISK_COLORS)
                st.plotly_chart(aplicar_tema_grafico(fig_pie, "Composición de Riesgo (filtrado)"), use_container_width=True)

            st.write("")
            with st.expander("Ver datos filtrados"):
                st.dataframe(df_bi.head(50), use_container_width=True)