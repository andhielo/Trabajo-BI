"""
PLATAFORMA INTEGRAL DE ANALÍTICA UNIVERSITARIA
BI, Big Data e IA Ética para la mejora de la Salud Mental en Universitarios de Lima Norte
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# ============================================================
# CONFIGURACIÓN GENERAL Y CONSTANTES
# ============================================================
st.set_page_config(
    page_title="BI Salud Mental Lima Norte",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rutas relativas para compatibilidad local y de nube
DB_PATH = "warehouse.db"
RAW_CSV_DEFAULT = "encuestas_salud_mental_lima_norte.csv"

PASOS = [
    "Pantalla General",
    "1. Fuentes de Datos",
    "2. Staging Area",
    "3. Proceso ETL",
    "4. Data Warehouse",
    "5. Capa de IA Ética",
    "6. Capa Semántica & KPIs",
    "7. Visualización BI",
]

# ============================================================
# INICIALIZACIÓN DEL ESTADO (Session State)
# ============================================================
def init_session_state():
    variables = [
        "df_raw", "df_staging", "df_errores", "df_clean", 
        "modelo_entrenado", "metricas_modelo", "df_pred"
    ]
    for var in variables:
        if var not in st.session_state:
            st.session_state[var] = None

# ============================================================
# ESTILOS CSS
# ============================================================
def aplicar_estilos():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 5px solid #2ecc71;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO (Cacheadas)
# ============================================================
@st.cache_data
def cargar_datos_demo(ruta):
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    else:
        st.error(f"Archivo no encontrado: {ruta}.")
        return None

# ============================================================
# VISTAS DE CADA PASO
# ============================================================
def mostrar_pantalla_general():
    st.markdown("""
    <div class="main-header">
        <h1 style="margin-bottom: 0;">Plataforma Integral de Analítica Universitaria</h1>
        <h3 style="font-weight: 300; margin-top: 10px; color: #e0e0e0;">BI, Big Data e IA Ética para la mejora de la Salud Mental en Lima Norte</h3>
        <p style="margin-top: 20px;">Pipeline de datos End-to-End: Captura ➔ Staging ➔ ETL ➔ DW ➔ Machine Learning ➔ BI Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Arquitectura del Sistema")
    st.info("El objetivo es **detectar patrones de riesgo psicoemocional** de forma ética y anónima para apoyar la toma de decisiones en Bienestar Universitario.")

def mostrar_fuentes_datos():
    st.subheader("1. Fuentes de Datos")
    st.write("Carga el archivo de encuestas de bienestar universitario.")

    archivo = st.file_uploader("Sube tu archivo (CSV o Excel)", type=["csv", "xlsx"])
    usar_demo = st.checkbox("Usar dataset de ejemplo", value=(archivo is None))

    df = None
    if archivo is not None:
        df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    elif usar_demo:
        df = cargar_datos_demo(RAW_CSV_DEFAULT)

    if df is not None:
        st.session_state.df_raw = df
        st.success(f"✅ Datos cargados: {df.shape[0]} registros y {df.shape[1]} columnas.")
        st.dataframe(df.head(), use_container_width=True)

def mostrar_staging():
    st.subheader("2. Staging Area (Calidad de Datos)")
    
    if st.session_state.df_raw is None:
        st.warning("⚠️ Carga los datos en el Paso 1 primero.")
        return

    df = st.session_state.df_raw.copy()
    
    edad_num = pd.to_numeric(df.get("edad", pd.Series()), errors="coerce")
    sueno_num = pd.to_numeric(df.get("horas_sueno_promedio", pd.Series()), errors="coerce")
    
    mask_edad = ~edad_num.between(15, 60)
    mask_sueno = ~sueno_num.between(0, 16) & sueno_num.notna()
    mask_dup = df.duplicated(subset=["id_encuesta"], keep=False) if "id_encuesta" in df else pd.Series(False, index=df.index)

    mask_error = mask_edad.fillna(False) | mask_sueno.fillna(False) | mask_dup
    
    st.session_state.df_staging = df[~mask_error]
    st.session_state.df_errores = df[mask_error]

    cols = st.columns(4)
    cols[0].metric("Total Registros", len(df))
    cols[1].metric("Duplicados", mask_dup.sum())
    cols[2].metric("Errores Edad", mask_edad.sum())
    cols[3].metric("Registros Válidos", len(st.session_state.df_staging))

    if len(st.session_state.df_errores) > 0:
        st.error(f"Se aislaron {len(st.session_state.df_errores)} registros con inconsistencias.")
        st.dataframe(st.session_state.df_errores.head(), use_container_width=True)

def mostrar_etl():
    st.subheader("3. Proceso ETL")
    
    if st.session_state.df_staging is None:
        st.warning("⚠️ Ejecuta el Paso 2 primero.")
        return

    df = st.session_state.df_staging.copy()

    with st.spinner("Procesando transformaciones..."):
        if "universidad" in df:
            df["universidad"] = df["universidad"].str.strip().str.title()
        if "fecha_encuesta" in df:
            df["fecha_encuesta"] = pd.to_datetime(df["fecha_encuesta"], errors="coerce")
        if "id_encuesta" in df:
            df = df.drop_duplicates(subset=["id_encuesta"])

        req_cols = ["nivel_estres", "nivel_ansiedad", "nivel_animo", "apoyo_social"]
        if all(c in df.columns for c in req_cols):
            df["indice_riesgo"] = (
                df["nivel_estres"] * 0.35 + 
                df["nivel_ansiedad"] * 0.35 + 
                (10 - df["nivel_animo"]) * 0.20 + 
                (10 - df["apoyo_social"]) * 0.10
            ).round(2)

            df["nivel_riesgo"] = pd.cut(
                df["indice_riesgo"], 
                bins=[-1, 4.5, 7, 10], 
                labels=["Bajo", "Medio", "Alto"]
            )

        st.session_state.df_clean = df

    st.success("✅ Transformaciones completadas con éxito.")
    st.dataframe(df.head(), use_container_width=True)

def mostrar_data_warehouse():
    st.subheader("4. Data Warehouse (SQLite)")
    
    if st.session_state.df_clean is None:
        st.warning("⚠️ Ejecuta el ETL primero.")
        return

    df = st.session_state.df_clean
    
    st.markdown("""
    <div class="kpi-card">
    <b>Modelo Estrella Lógico:</b> <code>FACT_SALUD_MENTAL</code> rodeada por <code>DIM_ESTUDIANTE</code> y <code>DIM_TIEMPO</code>.
    </div><br>
    """, unsafe_allow_html=True)

    if st.button("💾 Generar y Guardar DW en SQLite", type="primary"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df.to_sql("fact_salud_mental", conn, if_exists="replace", index=False)
            st.success(f"✅ Data Warehouse generado correctamente en {DB_PATH}")
        except Exception as e:
            st.error(f"Error al guardar: {e}")

def mostrar_ia():
    st.subheader("5. Capa de IA Ética")
    
    if st.session_state.df_clean is None or "nivel_riesgo" not in st.session_state.df_clean:
        st.warning("⚠️ Requiere datos limpios con el cálculo de riesgo (Paso 3).")
        return

    df = st.session_state.df_clean.dropna(subset=["nivel_riesgo"])
    
    features = ["horas_sueno_promedio", "apoyo_social", "promedio_academico", "edad"]
    features = [f for f in features if f in df.columns]

    if st.button("🧠 Entrenar Modelo Random Forest", type="primary"):
        X = df[features].fillna(0)
        y = df["nivel_riesgo"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        clf = RandomForestClassifier(random_state=42, class_weight="balanced")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        st.session_state.modelo_entrenado = clf
        st.session_state.metricas_modelo = {"acc": accuracy_score(y_test, y_pred)}
        
        st.success(f"✅ Modelo entrenado. Exactitud: {accuracy_score(y_test, y_pred):.2%}")
        
        # Uso de gráficos nativos de Streamlit para la importancia de variables
        st.markdown("##### Importancia de Variables (Transparencia)")
        imp_df = pd.DataFrame({"Importancia": clf.feature_importances_}, index=features).sort_values("Importancia", ascending=False)
        st.bar_chart(imp_df)

def mostrar_kpis():
    st.subheader("6. Capa Semántica y KPIs")
    
    if st.session_state.df_clean is None:
        st.warning("⚠️ Ejecuta el ETL primero.")
        return

    df = st.session_state.df_clean
    
    try:
        pct_alto = (df["nivel_riesgo"] == "Alto").mean() * 100
        sueno_ok = (pd.to_numeric(df.get("horas_sueno_promedio", 0), errors="coerce") >= 7).mean() * 100
        
        c1, c2 = st.columns(2)
        c1.metric("🔴 % Estudiantes en Riesgo Alto", f"{pct_alto:.1f}%")
        c2.metric("💤 % Sueño Saludable (≥7h)", f"{sueno_ok:.1f}%")
    except Exception as e:
        st.error("No se pudieron calcular los KPIs con los datos actuales.")

def mostrar_bi():
    st.subheader("7. Dashboard Ejecutivo BI")
    
    if st.session_state.df_clean is None:
        st.warning("⚠️ Ejecuta el ETL primero.")
        return

    df = st.session_state.df_clean

    if "nivel_riesgo" in df.columns:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### Distribución de Riesgo Psicoemocional")
            # Gráfico nativo de Streamlit reemplazando el pie chart
            riesgo_counts = df["nivel_riesgo"].value_counts()
            st.bar_chart(riesgo_counts)
            
        with c2:
            if "universidad" in df.columns:
                st.markdown("##### Riesgo por Universidad")
                # Preparamos los datos cruzados para que Streamlit los grafique nativamente
                univ_riesgo = pd.crosstab(df["universidad"], df["nivel_riesgo"])
                st.bar_chart(univ_riesgo)

# ============================================================
# FUNCIÓN PRINCIPAL (MAIN)
# ============================================================
def main():
    init_session_state()
    aplicar_estilos()

    with st.sidebar:
        st.markdown("## 🧠 Panel de Control")
        st.caption("Flujo de trabajo BI")
        st.markdown("---")
        paso_actual = st.radio("Navegación", PASOS)
        st.markdown("---")
        st.caption("Desarrollado con Streamlit (Sin dependencias externas de visualización)")

    # Enrutador
    if paso_actual == PASOS[0]:
        mostrar_pantalla_general()
    elif paso_actual == PASOS[1]:
        mostrar_fuentes_datos()
    elif paso_actual == PASOS[2]:
        mostrar_staging()
    elif paso_actual == PASOS[3]:
        mostrar_etl()
    elif paso_actual == PASOS[4]:
        mostrar_data_warehouse()
    elif paso_actual == PASOS[5]:
        mostrar_ia()
    elif paso_actual == PASOS[6]:
        mostrar_kpis()
    elif paso_actual == PASOS[7]:
        mostrar_bi()

if __name__ == "__main__":
    main()