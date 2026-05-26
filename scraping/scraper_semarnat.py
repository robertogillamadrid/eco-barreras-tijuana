
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────

URLS_SEMARNAT = {
    "recoleccion_municipios": (
        "http://dgeiawf.semarnat.gob.mx:8080/ibi_apps/WFServlet"
        "?IBIF_ex=D3_RSM01_03&IBIC_user=dgeia_mce&IBIC_pass=dgeia_mce"
        "&NOMBREENTIDAD=*&NOMBREANIO=*"
    ),
    "generacion_entidad": (
        "http://dgeiawf.semarnat.gob.mx:8080/ibi_apps/WFServlet"
        "?IBIF_ex=D3_RSM01_02&IBIC_user=dgeia_mce&IBIC_pass=dgeia_mce"
        "&NOMBREENTIDAD=*&NOMBREANIO=*"
    ),
    "programas_municipios": (
        "http://dgeiawf.semarnat.gob.mx:8080/ibi_apps/WFServlet"
        "?IBIF_ex=D3_RSM03_04&IBIC_user=dgeia_mce&IBIC_pass=dgeia_mce"
        "&NOMBREENTIDAD=*&NOMBREANIO=*"
    ),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

RUTA_RAW = r"C:\Users\admin\Desktop\proyecto_parra\residuos\data\residuos_raw.csv"
RUTA_BC  = r"C:\Users\admin\Desktop\proyecto_parra\residuos\data\residuos_baja_california.csv"


# ─────────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────────

def extraer_tablas_html(url: str, nombre: str) -> list:
    print(f"\n[+] Extrayendo: {nombre}")
    print(f"    URL: {url[:80]}...")

    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=30)
        respuesta.raise_for_status()
        print(f"    Status: {respuesta.status_code} OK")
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] No se pudo conectar: {e}")
        return []

    soup = BeautifulSoup(respuesta.text, "html.parser")
    tablas_html = soup.find_all("table")
    print(f"    Tablas encontradas: {len(tablas_html)}")

    dataframes = []
    for i, tabla in enumerate(tablas_html):
        filas = []
        for fila in tabla.find_all("tr"):
            celdas = [td.get_text(strip=True) for td in fila.find_all(["td", "th"])]
            if celdas:
                filas.append(celdas)

        if not filas:
            continue

        try:
            encabezados = filas[0]
            datos = filas[1:]
            if datos and len(encabezados) == len(datos[0]):
                df = pd.DataFrame(datos, columns=encabezados)
            else:
                df = pd.DataFrame(filas)
        except Exception:
            df = pd.DataFrame(filas)

        df["fuente"] = nombre
        df["tabla_num"] = i + 1
        dataframes.append(df)
        print(f"    Tabla {i+1}: {df.shape[0]} filas x {df.shape[1]} columnas")

    return dataframes


def limpiar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.replace("", pd.NA, inplace=True)
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df.drop_duplicates(inplace=True)
    for col in df.select_dtypes(include="str").columns:
        df[col] = df[col].str.strip()
    df.reset_index(drop=True, inplace=True)
    return df


def filtrar_baja_california(df: pd.DataFrame) -> pd.DataFrame:
    mascara = df.apply(
        lambda col: col.astype(str).str.contains(
            "Baja California|Tijuana|BAJA CALIFORNIA",
            case=False, na=False
        )
    ).any(axis=1)
    return df[mascara].copy()


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────

def main():
    todos_los_datos = []
    dfs_combinados = []

    for nombre, url in URLS_SEMARNAT.items():
        dataframes = extraer_tablas_html(url, nombre)
        time.sleep(2)

        for df in dataframes:
            df_limpio = limpiar_dataframe(df)
            if not df_limpio.empty:
                dfs_combinados.append(df_limpio)
                todos_los_datos.append({
                    "fuente": nombre,
                    "registros": len(df_limpio),
                })

    # ── Reporte ────────────────────────────────
    print("\n" + "="*50)
    print("RESUMEN DE EXTRACCIÓN")
    print("="*50)
    total = 0
    for info in todos_los_datos:
        print(f"  {info['fuente']}: {info['registros']} registros")
        total += info["registros"]
    print(f"\n  TOTAL REGISTROS: {total}")

    # ── Guardar ────────────────────────────────
    if dfs_combinados:
        df_final = pd.concat(dfs_combinados, ignore_index=True)

        df_final.to_csv(RUTA_RAW, index=False, encoding="utf-8-sig")
        print(f"\n[✓] Guardado: residuos_raw.csv ({len(df_final)} filas)")

        df_bc = filtrar_baja_california(df_final)
        if not df_bc.empty:
            df_bc.to_csv(RUTA_BC, index=False, encoding="utf-8-sig")
            print(f"[✓] Guardado: residuos_baja_california.csv ({len(df_bc)} filas)")
        else:
            print("[!] No se encontraron filas de Baja California")

        print("\nPrimeras 5 filas:")
        print(df_final.head())
    else:
        print("\n[!] No se extrajeron datos.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()