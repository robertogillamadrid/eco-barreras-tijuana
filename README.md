# 🌊 Eco-Barreras Inteligentes Tijuana

Proyecto ETL - Residuos sólidos en cañones de Tijuana  
**Meta 4.1 - Programación para la Extracción de Datos**  
Universidad Autónoma de Baja California | Facultad de Contaduría y Administración  

---

## 👥 Equipo

| Integrante |
|---|
| Gil Lamadrid Hernandez Roberto Alan |
| Ixmatlahua Martinez Hanna Sayury |
| Morales Lopez Wuendy Alejandra |
| Soto Romano Jessica Mariel |

**Docente:** Josue Miguel Flores Parra  
**Grupo:** 951 | **Carrera:** Inteligencia de Negocios

---

## 📋 Descripción del Problema

La acumulación de residuos sólidos en los cañones de Tijuana representa una de las crisis ambientales más urgentes de la región fronteriza. Durante las temporadas de lluvias, los escurrimientos arrastran toneladas de basura hacia el Río Tijuana y las playas de San Diego, generando un conflicto binacional de alto impacto ambiental.

---

## ❓ Preguntas que responde el proyecto

1. ¿Cuáles son los cañones de Tijuana con mayor acumulación de residuos sólidos?
2. ¿Qué tipos de residuos predominan en los cañones prioritarios?
3. ¿Cómo influye la temporada de lluvias en el volumen de residuos?
4. ¿Qué colonias generan mayor flujo de basura hacia los cañones?
5. ¿Cuántos residuos genera Tijuana comparado con otros municipios de Baja California?

---

## 🛠️ Tecnologías utilizadas

| Librería | Uso |
|---|---|
| BeautifulSoup4 | Scraping de datos SEMARNAT |
| Selenium | Scraping dinámico Ayuntamiento Tijuana |
| Pandas | Limpieza y transformación de datos |
| PyMySQL | Conector a MySQL |
| SQLAlchemy | ORM para inserción de datos |
| Streamlit | Desarrollo de dashboards |
| Plotly | Gráficas interactivas |

---

## 📊 Datos recolectados

| Fuente | Herramienta | Registros |
|---|---|---|
| SEMARNAT | BeautifulSoup4 | 507 |
| Ayuntamiento Tijuana (6 municipios) | Selenium | 528 |
| **TOTAL** | | **1,035** |

---

## 🗄️ Base de datos

- **Motor:** MySQL
- **Base de datos:** `eco_barreras_tijuana`
- **Tablas:** 7 tablas normalizadas (3FN)

| Tabla | Registros |
|---|---|
| entidad_federativa | 32 |
| municipio | 78 |
| tipo_residuo | 9 |
| canon_tijuana | 5 |
| programa_municipal | 64 |
| recoleccion_residuos | 528 |

---

## 📈 Dashboards

El proyecto cuenta con **6 dashboards interactivos** en Streamlit:

1. **📊 KPIs Generales** — Indicadores con filtros dinámicos por año, municipio y tipo de residuo. Incluye comparación con año anterior.
2. **🗺️ Mapa de Cañones Críticos** — Mapa interactivo con puntos de tamaño proporcional a la gravedad. Tooltips con información detallada.
3. **♻️ Tipos de Residuos** — Análisis de residuos con gráficas de barras, pastel y agrupadas.
4. **🏙️ Info por Municipio** — Selecciona cualquier municipio y ve su información detallada.
5. **⚔️ Tijuana vs Otros Municipios** — Comparativa directa entre Tijuana y otro municipio.
6. **📈 Tendencias y Análisis** — Heatmap, scatter, sunburst y análisis avanzado.

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/robertogillamadrid/eco-barreras-tijuana.git
cd eco-barreras-tijuana
```

### 2. Instalar dependencias
```bash
pip install requests beautifulsoup4 selenium pandas sqlalchemy pymysql streamlit plotly webdriver-manager
```

### 3. Configurar la base de datos
- Abrir MySQL Workbench
- Ejecutar los archivos `.sql` de la carpeta `database/`

### 4. Configurar la conexión
- Editar `database/conexion.py`
- Cambiar `password` por tu contraseña de MySQL

### 5. Cargar los datos
```bash
python scraping/scraper_semarnat.py
python scraping/scraper_selenium.py
python database/cargar_datos.py
```

### 6. Correr el dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📁 Estructura del proyecto
eco-barreras-tijuana/
├── scraping/
│   ├── scraper_semarnat.py    # Scraping con BeautifulSoup4
│   └── scraper_selenium.py    # Scraping con Selenium
├── database/
│   ├── conexion.py            # Conexión a MySQL
│   ├── cargar_datos.py        # Carga de datos a MySQL
│   └── *.sql                  # Archivos SQL con estructura e inserts
├── dashboard/
│   └── app.py                 # 6 dashboards en Streamlit
├── data/
│   ├── residuos_raw.csv       # Datos SEMARNAT
│   ├── residuos_selenium.csv  # Datos 6 municipios BC
│   └── residuos_baja_california.csv
└── README.md
---

## 🗺️ Cañones Críticos identificados

| Cañón | Prioridad | Descripción |
|---|---|---|
| Cañón Los Laureles | 🔴 Alta | Flujo directo hacia Río Tijuana y frontera |
| Cañón El Florido | 🔴 Alta | Alta densidad poblacional en zonas aledañas |
| Cañón La Morita | 🔴 Alta | Asentamientos irregulares con alto flujo de residuos |
| Cañón El Refugio | 🟡 Media | Flujo intermitente en temporada de lluvias |
| Cañón Matamoros | 🟡 Media | Zona industrial con residuos mixtos |

---

## 📄 Licencia

Proyecto académico — Universidad Autónoma de Baja California — Mayo 2026