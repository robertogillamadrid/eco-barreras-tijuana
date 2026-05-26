
import pymysql
from sqlalchemy import create_engine, text
import pandas as pd

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE CONEXIÓN
# ─────────────────────────────────────────────

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",        # cambia si tu usuario es diferente
    "password": "Transilvania2305",            # pon tu contraseña de MySQL aquí
    "database": "eco_barreras_tijuana",
    "charset":  "utf8mb4",
}


def get_engine():
    """Crea y retorna un engine de SQLAlchemy."""
    url = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
        f"/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
    )
    engine = create_engine(url, echo=False)
    return engine


def get_connection():
    """Retorna una conexión directa con pymysql."""
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
    )
    return conn


def probar_conexion():
    """Prueba que la conexión a MySQL funcione correctamente."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            resultado = conn.execute(text("SELECT VERSION()"))
            version = resultado.fetchone()[0]
            print(f"[✓] Conexión exitosa a MySQL")
            print(f"    Versión: {version}")
            print(f"    Base de datos: {DB_CONFIG['database']}")

            # Verificar tablas existentes
            tablas = conn.execute(text("SHOW TABLES"))
            print(f"\n    Tablas encontradas:")
            for tabla in tablas:
                print(f"      - {tabla[0]}")

    except Exception as e:
        print(f"[✗] Error de conexión: {e}")
        print("    Verifica usuario, contraseña y que MySQL esté corriendo.")


if __name__ == "__main__":
    probar_conexion()