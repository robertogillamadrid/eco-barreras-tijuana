# dashboard/app.py
#streamlit run residuos/dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_engine
from sqlalchemy import text

st.set_page_config(
    page_title="Eco-Barreras Tijuana",
    page_icon="🌊",
    layout="wide"
)

# ── CSS personalizado ──────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1F4E79, #2E75B6);
        padding: 20px; border-radius: 12px; color: white;
        text-align: center; margin: 5px;
    }
    .kpi-value { font-size: 2rem; font-weight: bold; }
    .kpi-label { font-size: 0.9rem; opacity: 0.85; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    engine = get_engine()
    with engine.connect() as conn:
        canonos = pd.read_sql("SELECT * FROM canon_tijuana", conn)
        entidades = pd.read_sql("SELECT * FROM entidad_federativa", conn)
        municipios = pd.read_sql("""
            SELECT m.id_municipio, m.nombre AS municipio, e.nombre AS entidad
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
            SELECT r.id_recoleccion, r.toneladas_dia, r.metodo_recoleccion,
                   r.cobertura_pct, r.anio, m.nombre AS municipio,
                   e.nombre AS entidad
            FROM recoleccion_residuos r
            JOIN municipio m ON r.id_municipio = m.id_municipio
            JOIN entidad_federativa e ON m.id_entidad = e.id_entidad
        """, conn)
    return canonos, entidades, municipios, programas, tipos, recoleccion

canonos, entidades, municipios, programas, tipos, recoleccion = cargar_datos()

# Agregar tamaño de punto según prioridad
prioridad_size = {"Alta": 25, "Media": 15, "Baja": 8}
prioridad_color = {"Alta": "#E74C3C", "Media": "#F39C12", "Baja": "#27AE60"}
canonos["size"] = canonos["nivel_prioridad"].map(prioridad_size)
canonos["color"] = canonos["nivel_prioridad"].map(prioridad_color)

# ── SIDEBAR ───────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/recycle.png", width=80)
st.sidebar.title("Eco-Barreras Inteligentes")
st.sidebar.markdown("**Tijuana, Baja California**")
st.sidebar.markdown("---")
dashboard = st.sidebar.radio("Selecciona Dashboard:", [
    "📊 KPIs Generales",
    "🗺️ Mapa de Cañones Críticos",
    "♻️ Tipos de Residuos",
    "🏙️ Info por Municipio",
    "⚔️ Tijuana vs Otros Municipios",
    "📈 Tendencias y Análisis",
])
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total registros:** {len(recoleccion):,}")
st.sidebar.markdown(f"**Municipios:** {recoleccion['municipio'].nunique()}")
st.sidebar.markdown(f"**Cañones críticos:** {len(canonos)}")


# ══════════════════════════════════════════════
# DASHBOARD 1 — KPIs GENERALES
# ══════════════════════════════════════════════
if dashboard == "📊 KPIs Generales":
    st.title("📊 KPIs Generales — Eco-Barreras Tijuana")
    st.markdown("Indicadores clave del proyecto de residuos sólidos en Tijuana.")
    st.markdown("---")

    # ── FILTROS DINÁMICOS ─────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        anios_disponibles = sorted(recoleccion["anio"].unique())
        anio_sel = st.selectbox("📅 Filtrar por año:", ["Todos"] + [str(a) for a in anios_disponibles])
    with col2:
        municipios_disponibles = sorted(recoleccion["municipio"].unique())
        mun_sel = st.selectbox("🏙️ Filtrar por municipio:", ["Todos"] + municipios_disponibles)
    with col3:
        tipos_disponibles = sorted(recoleccion["metodo_recoleccion"].unique())
        tipo_sel = st.selectbox("♻️ Filtrar por tipo:", ["Todos"] + tipos_disponibles)

    # Aplicar filtros
    df_filtrado = recoleccion.copy()
    if anio_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["anio"] == int(anio_sel)]
    if mun_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["municipio"] == mun_sel]
    if tipo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["metodo_recoleccion"] == tipo_sel]

    # Periodo anterior para comparacion
    if anio_sel != "Todos":
        anio_ant = int(anio_sel) - 1
        df_anterior = recoleccion[recoleccion["anio"] == anio_ant]
        if mun_sel != "Todos":
            df_anterior = df_anterior[df_anterior["municipio"] == mun_sel]
        if tipo_sel != "Todos":
            df_anterior = df_anterior[df_anterior["metodo_recoleccion"] == tipo_sel]
    else:
        df_anterior = pd.DataFrame()

    def delta(actual, anterior, formato=".2f"):
        if df_anterior.empty or anterior == 0:
            return None
        return round(actual - anterior, 2)

    st.markdown("---")
    st.markdown(f"### Mostrando datos para: **{anio_sel}** | **{mun_sel}** | **{tipo_sel}**")
    st.markdown("---")

    # ── KPIs FILA 1 ───────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    registros_act = len(df_filtrado)
    registros_ant = len(df_anterior) if not df_anterior.empty else 0
    col1.metric(
        "🗑️ Total Registros",
        f"{registros_act:,}",
        delta=f"{registros_act - registros_ant:+,}" if not df_anterior.empty else None
    )

    ton_act = round(df_filtrado["toneladas_dia"].mean(), 2) if not df_filtrado.empty else 0
    ton_ant = round(df_anterior["toneladas_dia"].mean(), 2) if not df_anterior.empty else 0
    col2.metric(
        "📦 Ton/día promedio",
        f"{ton_act:.2f}",
        delta=f"{ton_act - ton_ant:+.2f}" if not df_anterior.empty else None
    )

    cob_act = round(df_filtrado["cobertura_pct"].mean(), 1) if not df_filtrado.empty else 0
    cob_ant = round(df_anterior["cobertura_pct"].mean(), 1) if not df_anterior.empty else 0
    col3.metric(
        "🎯 Cobertura promedio",
        f"{cob_act:.1f}%",
        delta=f"{cob_act - cob_ant:+.1f}%" if not df_anterior.empty else None
    )

    ton_total_act = round(df_filtrado["toneladas_dia"].sum(), 2) if not df_filtrado.empty else 0
    ton_total_ant = round(df_anterior["toneladas_dia"].sum(), 2) if not df_anterior.empty else 0
    col4.metric(
        "⚖️ Total Toneladas",
        f"{ton_total_act:,.2f}",
        delta=f"{ton_total_act - ton_total_ant:+,.2f}" if not df_anterior.empty else None
    )

    # ── KPIs FILA 2 ───────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    mun_act = df_filtrado["municipio"].nunique()
    mun_ant = df_anterior["municipio"].nunique() if not df_anterior.empty else 0
    col1.metric(
        "🏙️ Municipios activos",
        mun_act,
        delta=f"{mun_act - mun_ant:+}" if not df_anterior.empty else None
    )

    tipo_top = df_filtrado.groupby("metodo_recoleccion")["toneladas_dia"].sum().idxmax() if not df_filtrado.empty else "N/A"
    col2.metric("🏆 Residuo predominante", tipo_top)

    mun_top = df_filtrado.groupby("municipio")["toneladas_dia"].sum().idxmax() if not df_filtrado.empty else "N/A"
    col3.metric("📍 Municipio mayor volumen", mun_top)

    col4.metric("⚠️ Cañones Alta Prioridad", len(canonos[canonos["nivel_prioridad"] == "Alta"]))

    st.markdown("---")

    # ── GRÁFICAS DINÁMICAS ────────────────────
    col1, col2 = st.columns(2)

    with col1:
        df_tipo = df_filtrado.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_tipo.columns = ["Tipo", "Toneladas"]
        df_tipo = df_tipo.sort_values("Toneladas", ascending=False)
        fig = px.bar(df_tipo, x="Tipo", y="Toneladas",
                     color="Toneladas", color_continuous_scale="Blues",
                     title=f"Toneladas por tipo — {anio_sel} | {mun_sel}",
                     hover_data={"Toneladas": ":.2f"})
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_prior = canonos["nivel_prioridad"].value_counts().reset_index()
        df_prior.columns = ["Prioridad", "Cantidad"]
        fig2 = px.pie(df_prior, names="Prioridad", values="Cantidad",
                      color="Prioridad",
                      color_discrete_map={"Alta": "#E74C3C", "Media": "#F39C12", "Baja": "#27AE60"},
                      title="Cañones por nivel de prioridad", hole=0.4)
        fig2.update_traces(
            hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>%{percent}<extra></extra>"
        )
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        df_anio = df_filtrado.groupby("anio")["toneladas_dia"].sum().reset_index()
        df_anio_cob = df_filtrado.groupby("anio")["cobertura_pct"].mean().reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_anio["anio"], y=df_anio["toneladas_dia"],
            name="Toneladas", marker_color="#2E75B6",
            hovertemplate="Año: %{x}<br>Toneladas: %{y:.2f}<extra></extra>"
        ))
        fig3.add_trace(go.Scatter(
            x=df_anio_cob["anio"], y=df_anio_cob["cobertura_pct"],
            name="Cobertura %", mode="lines+markers",
            marker_color="#E74C3C", yaxis="y2",
            hovertemplate="Año: %{x}<br>Cobertura: %{y:.1f}%<extra></extra>"
        ))
        fig3.update_layout(
            title=f"Toneladas vs Cobertura por año — {mun_sel}",
            yaxis=dict(title="Toneladas"),
            yaxis2=dict(title="Cobertura (%)", overlaying="y", side="right"),
            legend=dict(x=0, y=1)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        df_mun = df_filtrado.groupby("municipio")["toneladas_dia"].sum().reset_index()
        df_mun.columns = ["Municipio", "Toneladas"]
        df_mun = df_mun.sort_values("Toneladas", ascending=True)
        fig4 = px.bar(df_mun, x="Toneladas", y="Municipio", orientation="h",
                      color="Toneladas", color_continuous_scale="RdYlGn_r",
                      title=f"Toneladas por municipio — {anio_sel}",
                      hover_data={"Toneladas": ":.2f"})
        fig4.update_traces(hovertemplate="<b>%{y}</b><br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig4, use_container_width=True)

    # ── TABLA RESUMEN ─────────────────────────
    st.markdown("### Resumen por municipio")
    df_resumen = df_filtrado.groupby("municipio").agg(
        Registros=("id_recoleccion", "count"),
        Ton_promedio=("toneladas_dia", "mean"),
        Ton_total=("toneladas_dia", "sum"),
        Cobertura_prom=("cobertura_pct", "mean")
    ).reset_index().round(2)
    df_resumen.columns = ["Municipio", "Registros", "Ton/día prom", "Ton total", "Cobertura %"]
    df_resumen = df_resumen.sort_values("Ton total", ascending=False)
    st.dataframe(df_resumen, use_container_width=True)

# ══════════════════════════════════════════════
# DASHBOARD 2 — MAPA DE CAÑONES
# ══════════════════════════════════════════════
elif dashboard == "🗺️ Mapa de Cañones Críticos":
    st.title("🗺️ Mapa Interactivo de Cañones Críticos")
    st.markdown("**Pregunta:** ¿Cuáles son los cañones con mayor acumulación de residuos?")
    st.markdown("Pasa el mouse sobre cada punto para ver información detallada. Los puntos más grandes indican mayor prioridad.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cañones", len(canonos))
    col2.metric("🔴 Prioridad Alta", len(canonos[canonos["nivel_prioridad"] == "Alta"]))
    col3.metric("🟡 Prioridad Media", len(canonos[canonos["nivel_prioridad"] == "Media"]))

    st.markdown("---")

    # Mapa con plotly — puntos de tamaño según prioridad
    fig = px.scatter_mapbox(
        canonos,
        lat="latitud", lon="longitud",
        size="size",
        color="nivel_prioridad",
        color_discrete_map={"Alta": "#E74C3C", "Media": "#F39C12", "Baja": "#27AE60"},
        hover_name="nombre",
        hover_data={
            "nivel_prioridad": True,
            "descripcion": True,
            "latitud": ":.4f",
            "longitud": ":.4f",
            "size": False,
            "color": False
        },
        labels={"nivel_prioridad": "Prioridad", "descripcion": "Descripción"},
        mapbox_style="open-street-map",
        zoom=10,
        center={"lat": 32.48, "lon": -116.97},
        title="Cañones críticos de Tijuana — Tamaño indica nivel de urgencia",
        size_max=30,
        height=550
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Prioridad: %{customdata[0]}<br>%{customdata[1]}<br>Lat: %{lat:.4f} | Lon: %{lon:.4f}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Detalle de cada cañón")
    for _, row in canonos.iterrows():
        color = prioridad_color[row["nivel_prioridad"]]
        with st.expander(f"{'🔴' if row['nivel_prioridad']=='Alta' else '🟡'} {row['nombre']} — Prioridad {row['nivel_prioridad']}"):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Nivel de prioridad:** {row['nivel_prioridad']}")
            col1.markdown(f"**Latitud:** {row['latitud']}")
            col1.markdown(f"**Longitud:** {row['longitud']}")
            col2.markdown(f"**Descripción:** {row['descripcion']}")


# ══════════════════════════════════════════════
# DASHBOARD 3 — TIPOS DE RESIDUOS
# ══════════════════════════════════════════════
elif dashboard == "♻️ Tipos de Residuos":
    st.title("♻️ Análisis de Tipos de Residuos")
    st.markdown("**Pregunta:** ¿Qué tipos de residuos predominan en los cañones?")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total registros", f"{len(recoleccion):,}")
    col2.metric("Cobertura promedio", f"{recoleccion['cobertura_pct'].mean():.1f}%")
    col3.metric("Ton/día promedio", f"{recoleccion['toneladas_dia'].mean():.2f}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        df_tipo = recoleccion.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_tipo.columns = ["Tipo", "Toneladas"]
        df_tipo = df_tipo.sort_values("Toneladas", ascending=True)
        fig = px.bar(df_tipo, x="Toneladas", y="Tipo", orientation="h",
                     color="Toneladas", color_continuous_scale="RdYlGn_r",
                     title="Toneladas por tipo de residuo",
                     hover_data={"Toneladas": ":.2f"})
        fig.update_traces(hovertemplate="<b>%{y}</b><br>Toneladas: %{x:.2f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_tipo2 = recoleccion.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_tipo2.columns = ["Tipo", "Toneladas"]
        fig2 = px.pie(df_tipo2, names="Tipo", values="Toneladas",
                      title="Distribución porcentual de residuos", hole=0.35)
        fig2.update_traces(
            hovertemplate="<b>%{label}</b><br>Toneladas: %{value:.2f}<br>Porcentaje: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df_anio_tipo = recoleccion.groupby(["anio", "metodo_recoleccion"])["toneladas_dia"].sum().reset_index()
        fig3 = px.bar(df_anio_tipo, x="anio", y="toneladas_dia",
                      color="metodo_recoleccion", barmode="group",
                      title="Toneladas por tipo de residuo y año",
                      labels={"anio": "Año", "toneladas_dia": "Toneladas", "metodo_recoleccion": "Tipo"},
                      hover_data={"toneladas_dia": ":.2f"})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        df_cob_tipo = recoleccion.groupby("metodo_recoleccion")["cobertura_pct"].mean().reset_index()
        df_cob_tipo.columns = ["Tipo", "Cobertura (%)"]
        fig4 = px.bar(df_cob_tipo, x="Tipo", y="Cobertura (%)",
                      color="Cobertura (%)", color_continuous_scale="Blues",
                      title="Cobertura promedio por tipo de residuo",
                      hover_data={"Cobertura (%)": ":.1f"})
        fig4.update_traces(hovertemplate="<b>%{x}</b><br>Cobertura: %{y:.1f}%<extra></extra>")
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════
# DASHBOARD 4 — INFO POR MUNICIPIO
# ══════════════════════════════════════════════
elif dashboard == "🏙️ Info por Municipio":
    st.title("🏙️ Información por Municipio")
    st.markdown("Selecciona un municipio para ver su información detallada.")
    st.markdown("---")

    municipio_sel = st.selectbox("Selecciona un municipio:", sorted(recoleccion["municipio"].unique()))
    df_mun = recoleccion[recoleccion["municipio"] == municipio_sel]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros", len(df_mun))
    col2.metric("Ton/día promedio", f"{df_mun['toneladas_dia'].mean():.2f}")
    col3.metric("Cobertura promedio", f"{df_mun['cobertura_pct'].mean():.1f}%")
    col4.metric("Años registrados", df_mun["anio"].nunique())
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        df_tipo_mun = df_mun.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_tipo_mun.columns = ["Tipo", "Toneladas"]
        fig = px.pie(df_tipo_mun, names="Tipo", values="Toneladas",
                     title=f"Residuos en {municipio_sel} por tipo", hole=0.4)
        fig.update_traces(hovertemplate="<b>%{label}</b><br>Toneladas: %{value:.2f}<br>%{percent}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_anio_mun = df_mun.groupby("anio")["toneladas_dia"].sum().reset_index()
        fig2 = px.line(df_anio_mun, x="anio", y="toneladas_dia",
                       markers=True, title=f"Tendencia de toneladas en {municipio_sel}",
                       labels={"anio": "Año", "toneladas_dia": "Toneladas"},
                       color_discrete_sequence=["#E74C3C"])
        fig2.update_traces(hovertemplate="Año: %{x}<br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df_cob_mun = df_mun.groupby("anio")["cobertura_pct"].mean().reset_index()
        fig3 = px.bar(df_cob_mun, x="anio", y="cobertura_pct",
                      color="cobertura_pct", color_continuous_scale="Greens",
                      title=f"Cobertura de recolección en {municipio_sel}",
                      labels={"anio": "Año", "cobertura_pct": "Cobertura (%)"})
        fig3.update_traces(hovertemplate="Año: %{x}<br>Cobertura: %{y:.1f}%<extra></extra>")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.box(df_mun, x="metodo_recoleccion", y="toneladas_dia",
                      color="metodo_recoleccion",
                      title=f"Distribución de toneladas por tipo en {municipio_sel}",
                      labels={"metodo_recoleccion": "Tipo", "toneladas_dia": "Toneladas"})
        fig4.update_traces(hovertemplate="Tipo: %{x}<br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Datos completos del municipio")
    st.dataframe(df_mun[["anio", "metodo_recoleccion", "toneladas_dia", "cobertura_pct"]].rename(
        columns={"anio": "Año", "metodo_recoleccion": "Tipo Residuo",
                 "toneladas_dia": "Ton/día", "cobertura_pct": "Cobertura (%)"}
    ), use_container_width=True)


# ══════════════════════════════════════════════
# DASHBOARD 5 — TIJUANA VS OTROS
# ══════════════════════════════════════════════
elif dashboard == "⚔️ Tijuana vs Otros Municipios":
    st.title("⚔️ Tijuana vs Otros Municipios")
    st.markdown("**Pregunta:** ¿Cuántos residuos genera Tijuana comparado con otros municipios?")
    st.markdown("---")

    municipios_disponibles = [m for m in sorted(recoleccion["municipio"].unique()) if m != "Tijuana"]
    municipio_comp = st.selectbox("Selecciona municipio para comparar con Tijuana:", municipios_disponibles)

    df_tj = recoleccion[recoleccion["municipio"] == "Tijuana"]
    df_comp = recoleccion[recoleccion["municipio"] == municipio_comp]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏙️ Tijuana")
        st.metric("Registros", len(df_tj))
        st.metric("Ton/día promedio", f"{df_tj['toneladas_dia'].mean():.2f}")
        st.metric("Cobertura promedio", f"{df_tj['cobertura_pct'].mean():.1f}%")
    with col2:
        st.markdown(f"### 🏘️ {municipio_comp}")
        st.metric("Registros", len(df_comp))
        st.metric("Ton/día promedio", f"{df_comp['toneladas_dia'].mean():.2f}")
        st.metric("Cobertura promedio", f"{df_comp['cobertura_pct'].mean():.1f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        df_tj_anio = df_tj.groupby("anio")["toneladas_dia"].sum().reset_index()
        df_tj_anio["municipio"] = "Tijuana"
        df_comp_anio = df_comp.groupby("anio")["toneladas_dia"].sum().reset_index()
        df_comp_anio["municipio"] = municipio_comp
        df_combined = pd.concat([df_tj_anio, df_comp_anio])
        fig = px.line(df_combined, x="anio", y="toneladas_dia", color="municipio",
                      markers=True, title="Toneladas recolectadas por año",
                      labels={"anio": "Año", "toneladas_dia": "Toneladas", "municipio": "Municipio"},
                      color_discrete_map={"Tijuana": "#E74C3C", municipio_comp: "#2E75B6"})
        fig.update_traces(hovertemplate="<b>%{fullData.name}</b><br>Año: %{x}<br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_tj_tipo = df_tj.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_tj_tipo["municipio"] = "Tijuana"
        df_comp_tipo = df_comp.groupby("metodo_recoleccion")["toneladas_dia"].sum().reset_index()
        df_comp_tipo["municipio"] = municipio_comp
        df_comb_tipo = pd.concat([df_tj_tipo, df_comp_tipo])
        fig2 = px.bar(df_comb_tipo, x="metodo_recoleccion", y="toneladas_dia",
                      color="municipio", barmode="group",
                      title="Comparación por tipo de residuo",
                      labels={"metodo_recoleccion": "Tipo", "toneladas_dia": "Toneladas", "municipio": "Municipio"},
                      color_discrete_map={"Tijuana": "#E74C3C", municipio_comp: "#2E75B6"})
        fig2.update_traces(hovertemplate="<b>%{fullData.name}</b><br>Tipo: %{x}<br>Toneladas: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df_cob_tj = df_tj.groupby("anio")["cobertura_pct"].mean().reset_index()
        df_cob_tj["municipio"] = "Tijuana"
        df_cob_comp = df_comp.groupby("anio")["cobertura_pct"].mean().reset_index()
        df_cob_comp["municipio"] = municipio_comp
        df_cob_comb = pd.concat([df_cob_tj, df_cob_comp])
        fig3 = px.bar(df_cob_comb, x="anio", y="cobertura_pct", color="municipio",
                      barmode="group", title="Cobertura de recolección por año",
                      labels={"anio": "Año", "cobertura_pct": "Cobertura (%)", "municipio": "Municipio"},
                      color_discrete_map={"Tijuana": "#E74C3C", municipio_comp: "#2E75B6"})
        fig3.update_traces(hovertemplate="<b>%{fullData.name}</b><br>Año: %{x}<br>Cobertura: %{y:.1f}%<extra></extra>")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        resumen = pd.DataFrame({
            "Municipio": ["Tijuana", municipio_comp],
            "Total Ton": [df_tj["toneladas_dia"].sum(), df_comp["toneladas_dia"].sum()],
            "Promedio Ton/día": [df_tj["toneladas_dia"].mean(), df_comp["toneladas_dia"].mean()],
            "Cobertura %": [df_tj["cobertura_pct"].mean(), df_comp["cobertura_pct"].mean()],
        })
        fig4 = go.Figure(data=[
            go.Bar(name="Total Toneladas", x=resumen["Municipio"], y=resumen["Total Ton"],
                   marker_color=["#E74C3C", "#2E75B6"],
                   hovertemplate="<b>%{x}</b><br>Total Ton: %{y:.2f}<extra></extra>")
        ])
        fig4.update_layout(title="Comparación total de toneladas")
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════
# DASHBOARD 6 — TENDENCIAS Y ANÁLISIS
# ══════════════════════════════════════════════
elif dashboard == "📈 Tendencias y Análisis":
    st.title("📈 Tendencias y Análisis Avanzado")
    st.markdown("Análisis de patrones y tendencias en los datos de residuos.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        df_mun_total = recoleccion.groupby("municipio")["toneladas_dia"].sum().reset_index()
        df_mun_total = df_mun_total.sort_values("toneladas_dia", ascending=False).head(15)
        fig = px.bar(df_mun_total, x="toneladas_dia", y="municipio", orientation="h",
                     color="toneladas_dia", color_continuous_scale="Reds",
                     title="Top 15 municipios con mayor volumen de residuos",
                     labels={"toneladas_dia": "Toneladas", "municipio": "Municipio"})
        fig.update_traces(hovertemplate="<b>%{y}</b><br>Toneladas: %{x:.2f}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_scatter = recoleccion.groupby("municipio").agg(
            toneladas=("toneladas_dia", "mean"),
            cobertura=("cobertura_pct", "mean"),
            registros=("id_recoleccion", "count")
        ).reset_index()
        fig2 = px.scatter(df_scatter, x="cobertura", y="toneladas",
                          size="registros", color="toneladas",
                          hover_name="municipio",
                          color_continuous_scale="RdYlGn_r",
                          title="Cobertura vs Toneladas por municipio",
                          labels={"cobertura": "Cobertura (%)", "toneladas": "Ton/día promedio"},
                          size_max=40)
        fig2.update_traces(hovertemplate="<b>%{hovertext}</b><br>Cobertura: %{x:.1f}%<br>Ton/día: %{y:.2f}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        df_heat = recoleccion.groupby(["anio", "metodo_recoleccion"])["toneladas_dia"].mean().reset_index()
        df_pivot = df_heat.pivot(index="metodo_recoleccion", columns="anio", values="toneladas_dia")
        fig3 = px.imshow(df_pivot, color_continuous_scale="Blues",
                         title="Mapa de calor: Toneladas por tipo y año",
                         labels={"x": "Año", "y": "Tipo de Residuo", "color": "Ton/día"})
        fig3.update_traces(hovertemplate="Tipo: %{y}<br>Año: %{x}<br>Ton/día: %{z:.2f}<extra></extra>")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        df_cob_mun = recoleccion.groupby("municipio")["cobertura_pct"].mean().reset_index()
        df_cob_mun = df_cob_mun.sort_values("cobertura_pct", ascending=True).tail(15)
        fig4 = px.bar(df_cob_mun, x="cobertura_pct", y="municipio", orientation="h",
                      color="cobertura_pct", color_continuous_scale="Greens",
                      title="Top 15 municipios con mayor cobertura",
                      labels={"cobertura_pct": "Cobertura (%)", "municipio": "Municipio"})
        fig4.update_traces(hovertemplate="<b>%{y}</b><br>Cobertura: %{x:.1f}%<extra></extra>")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Análisis por municipio y tipo de residuo")
    df_pivot2 = recoleccion.groupby(["municipio", "metodo_recoleccion"])["toneladas_dia"].sum().reset_index()
    fig5 = px.sunburst(df_pivot2, path=["municipio", "metodo_recoleccion"], values="toneladas_dia",
                       color="toneladas_dia", color_continuous_scale="RdYlGn_r",
                       title="Distribución jerárquica: Municipio > Tipo de Residuo")
    fig5.update_traces(hovertemplate="<b>%{label}</b><br>Toneladas: %{value:.2f}<extra></extra>")
    st.plotly_chart(fig5, use_container_width=True)