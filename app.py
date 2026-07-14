import streamlit as st

# Configuración de la página debe ir siempre primero
st.set_page_config(
    page_title="Analítica Salud Mental - Lima Norte",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables de estado para la navegación
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Pantalla General"

def set_page(page_name):
    st.session_state.current_page = page_name

# ==========================================
# ESTILOS CSS PERSONALIZADOS (TEMA BLANCO)
# ==========================================
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Estilos generales del Sidebar para que sea BLANCO */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    
    /* Línea separadora del sidebar */
    hr {
        border-color: #E2E8F0 !important;
    }

    /* Banner Principal (Fondo Blanco) */
    .main-banner {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .main-banner h1 {
        color: #1E3A8A; /* Azul oscuro para el título principal */
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
        color: #059669; /* Verde oscuro */
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #E2E8F0;
    }

    /* Estilos para los botones de las tarjetas */
    .stButton>button {
        background-color: #F1F5F9;
        color: #1E3A8A !important;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #E2E8F0;
        border-color: #CBD5E1;
    }
    
    /* Títulos de los pasos */
    .step-header {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .step-title {
        font-size: 20px;
        font-weight: bold;
        color: #0F172A;
        margin-bottom: 5px;
        margin-top: 0px;
    }
    .step-desc {
        font-size: 14px;
        color: #64748B;
        height: 40px;
        margin-bottom: 15px;
    }
    .step-status {
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* Tarjetas (Contenedores) */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR (BARRA LATERAL)
# ==========================================
with st.sidebar:
    # Logo / Título
    st.markdown('<div style="text-align: center; margin-bottom: 10px;"><h1 style="font-size: 50px; margin: 0;">🧠</h1><h2 style="margin: 0; font-size: 20px; font-weight: 900; color: #1E3A8A !important;">SALUD MENTAL</h2><p style="font-size: 12px; color: #64748B !important; margin-top: -5px;">— LIMA NORTE —</p></div>', unsafe_allow_html=True)
    
    # Botón Pantalla General
    if st.button("⊞ Pantalla General", use_container_width=True):
        set_page("Pantalla General")
        
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 11px; font-weight: bold; color: #64748B !important; margin-bottom: 10px;'>7 PASOS DEL FLUJO BI</p>", unsafe_allow_html=True)
    
    # Menú de navegación lateral
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

# ==========================================
# CONTENIDO PRINCIPAL
# ==========================================
if st.session_state.current_page == "Pantalla General":
    
    # Banner Principal
    st.markdown("""
    <div class="main-banner">
        <h1>PLATAFORMA BI INTEGRADA - SALUD MENTAL UNIVERSITARIA</h1>
        <p>Arquitectura cloud end-to-end: captura segura, anonimización, ETL, warehouse, analítica predictiva ética y visualización de bienestar.</p>
        <div class="tech-badge">🟢 GitHub + Supabase PostgreSQL + Streamlit Community Cloud</div>
    </div>
    """, unsafe_allow_html=True)

    # Grid de 7 Pasos (2 filas: 4 columnas en la primera, 3 columnas en la segunda)
    col1, col2, col3, col4 = st.columns(4)
    
    # Paso 1
    with col1:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #3B82F6;">Paso 1</span><span style="color: #94A3B8;">FUENTES DE DATOS</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Fuentes de Datos</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Captura de tests psicológicos (GAD-7, PHQ-9) y encuestas.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #0EA5E9;">Registros crudos</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 1 →", key="btn1", use_container_width=True):
                set_page("① Fuentes de Datos")
                st.rerun()

    # Paso 2
    with col2:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #8B5CF6;">Paso 2</span><span style="color: #94A3B8;">STAGING AREA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Staging Area</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Validación, control de calidad y anonimización de datos (Hash).</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #8B5CF6;">Privacidad asegurada</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 2 →", key="btn2", use_container_width=True):
                set_page("② Staging Area")
                st.rerun()

    # Paso 3
    with col3:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #10B981;">Paso 3</span><span style="color: #94A3B8;">PROCESO ETL</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Proceso ETL</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Limpieza y transformación de métricas de estrés y sueño.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #10B981;">Transformación base</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 3 →", key="btn3", use_container_width=True):
                set_page("③ Proceso ETL")
                st.rerun()

    # Paso 4
    with col4:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #F59E0B;">Paso 4</span><span style="color: #94A3B8;">DATA WAREHOUSE</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Data Warehouse</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Carga segura en repositorio central Supabase PostgreSQL.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #F59E0B;">Modelo analítico listo</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 4 →", key="btn4", use_container_width=True):
                set_page("④ Data Warehouse")
                st.rerun()

    # Segunda fila
    st.write("") # Espaciador
    col5, col6, col7, col8 = st.columns(4) 
    
    # Paso 5
    with col5:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #3B82F6;">Paso 5</span><span style="color: #94A3B8;">CAPA DE IA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa de IA</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Predicción ética de riesgo y tokens de canalización psicológica.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #3B82F6;">Algoritmo preventivo</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 5 →", key="btn5", use_container_width=True):
                set_page("⑤ Capa de IA Ética")
                st.rerun()

    # Paso 6
    with col6:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #EAB308;">Paso 6</span><span style="color: #94A3B8;">CAPA SEMÁNTICA</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Capa Semántica</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Indicadores ejecutivos de ansiedad, depresión y estrés.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #EAB308;">Métricas de bienestar</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 6 →", key="btn6", use_container_width=True):
                set_page("⑥ Capa Semántica & KPIs")
                st.rerun()

    # Paso 7
    with col7:
        with st.container(border=True):
            st.markdown('<div class="step-header"><span style="color: #EC4899;">Paso 7</span><span style="color: #94A3B8;">VISUALIZACIÓN BI</span></div>', unsafe_allow_html=True)
            st.markdown('<p class="step-title">Visualización BI</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-desc">Dashboard final de monitorización e insights interactivos.</p>', unsafe_allow_html=True)
            st.markdown('<p class="step-status" style="color: #EC4899;">Panel directivo</p>', unsafe_allow_html=True)
            if st.button("Explorar Paso 7 →", key="btn7", use_container_width=True):
                set_page("⑦ Visualización BI")
                st.rerun()

else:
    # Plantilla para cuando el usuario hace clic en alguno de los 7 pasos
    st.button("← Volver a la Pantalla General", on_click=set_page, args=("Pantalla General",))
    st.markdown(f"<h2 style='color: #1E3A8A;'>{st.session_state.current_page}</h2>", unsafe_allow_html=True)
    st.info("Aquí puedes integrar el contenido específico, gráficos de Plotly o tablas de Pandas para este paso de tu arquitectura.")