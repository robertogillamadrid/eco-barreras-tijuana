# dashboard/app.py

import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_engine
from sqlalchemy import text

st.set_page_config(
    page_title="Eco-Barreras Tijuana",
    page_icon="🌊",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    engine = get_engine()
    with engine.connect() as conn:
        canonos = pd.read_sql("SELECT * FROM canon_tijuana", conn)
        entidades = pd.read_sql("SELECT * FROM entidad_federativa", conn)
        municipios = pd.read_sql("""
            SELECT m.nombre AS municipio, e.nombre AS entidad
            FROM municipio m
            JOIN entidad_federativa e ON m.id_entidad = e.id_entidad
        """, conn)
        programas = pd.read_sql("""
            SELECT e.nombre AS entidad, COUNT(*) AS total_programas
            FROM programa_municipal p
            JOIN municipio m ON p.id_municipio = m.id_municipio
            JOIN entidad_federativa e ON m.id_entidad = e.id_entidad
            GROUP BY e.nombre ORDER BY total_programas DESC
        """, conn)
        tipos = pd.read_sql("SELECT * FROM tipo_residuo", conn)
        recoleccion = pd.read_sql("""
            SELECT r.toneladas_dia, r.metodo_recoleccion,
                   r.cobertura_pct, r.anio, m.nombre AS municipio
            FROM recoleccion_residuos r
            JOIN municipio m ON r.id_municipio = m.id_municipio
        """, conn)
    return canonos, entidades, municipios, programas, tipos, recoleccion

canonos, entidades, municipios, programas, tipos, recoleccion = cargar_datos()

# ── SIDEBAR ────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/recycle.png", width=80)
st.sidebar.title("Eco-Barreras Inteligentes")
st.sidebar.markdown("**Tijuana, Baja California**")
st.sidebar.markdown("---")
dashboard = st.sidebar.radio("Selecciona Dashboard:", [
    "🗺️ Dashboard 1: Cañones Críticos",
    "♻️ Dashboard 2: Tipos de Residuos",
    "📊 Dashboard 3: Programas Municipales"
])

# ══════════════════════════════════════════════
# DASHBOARD 1 — CAÑONES CRÍTICOS
# ══════════════════════════════════════════════
if dashboard == "🗺️ Dashboard 1: Cañones Críticos":
    st.title("🗺️ Cañones Críticos de Tijuana")
    st.markdown("**Pregunta:** ¿Cuáles son los cañones con mayor acumulación de residuos?")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    alta = len(canonos[canonos["nivel_prioridad"] == "Alta"])
    media = len(canonos[canonos["nivel_prioridad"] == "Media"])
    col1.metric("Total Cañones", len(canonos))
    col2.metric("🔴 Prioridad Alta", alta)
    col3.metric("🟡 Prioridad Media", media)

    st.markdown("### Mapa de ubicación")
    mapa_df = canonos[["latitud", "longitud", "nombre"]].copy()
    mapa_df.columns = ["lat", "lon", "nombre"]
    st.map(mapa_df)

    st.markdown("### Detalle de cañones")
    colores = {"Alta": "🔴", "Media": "🟡", "Baja": "🟢"}
    canonos["Prioridad"] = canonos["nivel_prioridad"].map(colores) + " " + canonos["nivel_prioridad"]
    st.dataframe(
        canonos[["nombre", "Prioridad", "descripcion"]].rename(columns={
            "nombre": "Canon", "descripcion": "Descripcion"
        }),
        use_container_width=True
    )

# ══════════════════════════════════════════════
# DASHBOARD 2 — TIPOS DE RESIDUOS
# ══════════════════════════════════════════════
elif dashboard == "♻️ Dashboard 2: Tipos de Residuos":
    st.title("♻️ Tipos de Residuos en Cañones")
    st.markdown("**Pregunta:** ¿Que tipos de residuos predominan en los canones?")
    st.markdown("---")

    # Datos reales de recoleccion
    col1, col2, col3 = st.columns(3)
    col1.metric("Total registros", len(recoleccion))
    col2.metric("Cobertura promedio", f"{recoleccion['cobertura_pct'].mean():.1f}%")
    col3.metric("Toneladas promedio/dia", f"{recoleccion['toneladas_dia'].mean():.2f}")

    st.markdown("### Residuos por tipo de recoleccion")
    df_tipo = recoleccion.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
    df_tipo.columns = ["Tipo de Residuo", "Toneladas Total"]
    df_tipo = df_tipo.sort_values("Toneladas Total", ascending=False)
    st.bar_chart(df_tipo.set_index("Tipo de Residuo"))

    st.markdown("### Toneladas recolectadas por año")
    df_anio = recoleccion.groupby("anio")["toneladas_dia"].sum().reset_index()
    df_anio.columns = ["Año", "Toneladas Total"]
    st.line_chart(df_anio.set_index("Año"))

    st.markdown("### Detalle completo")
    st.dataframe(
        recoleccion.sort_values("toneladas_dia", ascending=False).head(50),
        use_container_width=True
    )

# ══════════════════════════════════════════════
# DASHBOARD 3 — PROGRAMAS MUNICIPALES
# ══════════════════════════════════════════════
elif dashboard == "📊 Dashboard 3: Programas Municipales":
    st.title("📊 Programas Municipales de Gestion")
    st.markdown("**Pregunta:** ¿Cuantos residuos genera Tijuana vs otros municipios de Baja California?")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Estados con programas", len(programas))
    col2.metric("Total municipios BD", len(municipios))
    col3.metric("Municipios BC", len(municipios[municipios["entidad"] == "Baja California"]))

    st.markdown("### Programas por entidad federativa")
    st.bar_chart(programas.set_index("entidad")["total_programas"])

    st.markdown("### Cobertura de recoleccion por año en Tijuana")
    df_cob = recoleccion.groupby("anio")["cobertura_pct"].mean().reset_index()
    df_cob.columns = ["Año", "Cobertura Promedio (%)"]
    st.line_chart(df_cob.set_index("Año"))

    st.markdown("### Municipios de Baja California registrados")
    bc = municipios[municipios["entidad"] == "Baja California"]
    st.dataframe(bc.reset_index(drop=True), use_container_width=True)

    st.markdown("### Todos los municipios")
    st.dataframe(municipios, use_container_width=True)