
import pandas as pd
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_engine

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_RAW = os.path.join(BASE_DIR, "data", "residuos_raw.csv")
def cargar_entidades(engine):
    """Carga entidades federativas desde el CSV."""
    entidades = [
        ("Aguascalientes", "01"), ("Baja California", "02"),
        ("Baja California Sur", "03"), ("Campeche", "04"),
        ("Coahuila", "05"), ("Colima", "06"), ("Chiapas", "07"),
        ("Chihuahua", "08"), ("Ciudad de México", "09"), ("Durango", "10"),
        ("Guanajuato", "11"), ("Guerrero", "12"), ("Hidalgo", "13"),
        ("Jalisco", "14"), ("México", "15"), ("Michoacán", "16"),
        ("Morelos", "17"), ("Nayarit", "18"), ("Nuevo León", "19"),
        ("Oaxaca", "20"), ("Puebla", "21"), ("Querétaro", "22"),
        ("Quintana Roo", "23"), ("San Luis Potosí", "24"), ("Sinaloa", "25"),
        ("Sonora", "26"), ("Tabasco", "27"), ("Tamaulipas", "28"),
        ("Tlaxcala", "29"), ("Veracruz", "30"), ("Yucatán", "31"),
        ("Zacatecas", "32"),
    ]
    with engine.connect() as conn:
        for nombre, clave in entidades:
            conn.execute(text("""
                INSERT IGNORE INTO entidad_federativa (nombre, clave_inegi)
                VALUES (:nombre, :clave)
            """), {"nombre": nombre, "clave": clave})
        conn.commit()
    print(f"[✓] Entidades cargadas: {len(entidades)}")


def cargar_municipios_desde_csv(engine):
    """Extrae municipios únicos del CSV y los carga en MySQL."""
    df = pd.read_csv(RUTA_RAW, low_memory=False)

    # Buscar columnas que puedan tener nombres de municipios
    posibles_cols = [c for c in df.columns if any(
        k in str(c).lower() for k in ["municipio", "entidad", "estado", "0"]
    )]

    municipios_insertados = 0
    municipios_vistos = set()

    with engine.connect() as conn:
        # Obtener entidades existentes
        resultado = conn.execute(text("SELECT id_entidad, nombre FROM entidad_federativa"))
        entidades_map = {row[1]: row[0] for row in resultado}

        # Buscar filas con nombres de entidades conocidas
        for _, fila in df.iterrows():
            for val in fila.values:
                val_str = str(val).strip()
                for entidad, id_ent in entidades_map.items():
                    if entidad.lower() in val_str.lower() and val_str not in municipios_vistos:
                        municipios_vistos.add(val_str)
                        try:
                            conn.execute(text("""
                                INSERT IGNORE INTO municipio (nombre, id_entidad)
                                VALUES (:nombre, :id_entidad)
                            """), {"nombre": val_str[:150], "id_entidad": id_ent})
                            municipios_insertados += 1
                        except Exception:
                            pass
        conn.commit()

    print(f"[✓] Municipios cargados: {municipios_insertados}")


def cargar_programas_desde_csv(engine):
    """Carga datos de programas municipales desde el CSV."""
    df = pd.read_csv(RUTA_RAW, low_memory=False)
    df_prog = df[df["fuente"] == "programas_municipios"].copy()

    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT id_municipio, nombre FROM municipio"))
        municipios_map = {row[1]: row[0] for row in resultado}

        insertados = 0
        for _, fila in df_prog.iterrows():
            for col_val in fila.values:
                nombre = str(col_val).strip()
                if nombre in municipios_map:
                    id_mun = municipios_map[nombre]
                    try:
                        conn.execute(text("""
                            INSERT INTO programa_municipal
                                (id_municipio, anio, tiene_programa, tiene_recoleccion, fuente)
                            VALUES (:id_mun, 2020, 1, 1, 'SEMARNAT/INEGI')
                        """), {"id_mun": id_mun})
                        insertados += 1
                    except Exception:
                        pass
        conn.commit()

    print(f"[✓] Programas municipales cargados: {insertados}")


def verificar_carga(engine):
    """Muestra resumen de registros en cada tabla."""
    tablas = [
        "entidad_federativa", "municipio", "tipo_residuo",
        "canon_tijuana", "programa_municipal",
        "recoleccion_residuos", "generacion_residuos"
    ]
    print("\n" + "="*45)
    print("RESUMEN DE DATOS EN MYSQL")
    print("="*45)
    with engine.connect() as conn:
        for tabla in tablas:
            resultado = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
            total = resultado.fetchone()[0]
            print(f"  {tabla:<30} {total:>5} registros")


def main():
    print("Iniciando carga de datos a MySQL...\n")
    engine = get_engine()

    cargar_entidades(engine)
    cargar_municipios_desde_csv(engine)
    cargar_programas_desde_csv(engine)
    cargar_datos_selenium(engine)
    verificar_carga(engine)

    print("\n[✓] Carga completada.")



def cargar_datos_selenium(engine):
    """Carga los datos de colonias desde el CSV de Selenium para múltiples municipios."""
    import os
    ruta = os.path.join(BASE_DIR, "data", "residuos_selenium.csv")
    if not os.path.exists(ruta):
        print("[!] No se encontró residuos_selenium.csv")
        return

    df = pd.read_csv(ruta)
    print(f"\n[+] Cargando {len(df)} registros de Selenium a MySQL...")

    with engine.connect() as conn:
        # Obtener entidades
        resultado = conn.execute(text("SELECT id_entidad FROM entidad_federativa WHERE nombre = 'Baja California'"))
        id_bc = resultado.fetchone()[0]

        # Insertar municipios que no existan
        municipios_csv = df["municipio"].unique()
        for mun in municipios_csv:
            conn.execute(text("""
                INSERT IGNORE INTO municipio (nombre, id_entidad)
                VALUES (:nombre, :id_entidad)
            """), {"nombre": mun, "id_entidad": id_bc})
        conn.commit()

        # Obtener mapa de municipios actualizado
        resultado = conn.execute(text("SELECT id_municipio, nombre FROM municipio"))
        municipios_map = {row[1]: row[0] for row in resultado}

        insertados = 0
        for _, fila in df.iterrows():
            id_mun = municipios_map.get(fila["municipio"])
            if not id_mun:
                continue
            try:
                conn.execute(text("""
                    INSERT INTO recoleccion_residuos
                        (id_municipio, anio, toneladas_dia, metodo_recoleccion,
                         cobertura_pct, fuente)
                    VALUES
                        (:id_mun, :anio, :toneladas, :metodo, :cobertura, :fuente)
                """), {
                    "id_mun":    id_mun,
                    "anio":      int(fila["anio"]),
                    "toneladas": float(fila["toneladas_recolectadas"]),
                    "metodo":    str(fila["tipo_residuo"]),
                    "cobertura": float(fila["cobertura_pct"]),
                    "fuente":    str(fila["fuente"]),
                })
                insertados += 1
            except Exception:
                pass
        conn.commit()

    print(f"[✓] Registros de Selenium cargados: {insertados}")
if __name__ == "__main__":
    main()