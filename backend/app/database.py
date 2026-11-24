import pyodbc
from contextlib import contextmanager
from app.config import settings


def build_connection_string() -> str:
    """Construye la cadena de conexión ODBC a SQL Server sin exponer credenciales fijas."""
    params = [
        f"DRIVER={{{settings.DB_DRIVER}}}",
        f"SERVER={settings.DB_SERVER}",
        f"DATABASE={settings.DB_NAME}",
    ]

    if settings.DB_USER and settings.DB_PASSWORD:
        params.append(f"UID={settings.DB_USER}")
        params.append(f"PWD={settings.DB_PASSWORD}")
    else:
        params.append(f"Trusted_Connection={settings.DB_TRUSTED_CONNECTION}")

    # En ODBC Driver 18 es necesario confiar en el certificado si no hay CA firmada
    if "18" in settings.DB_DRIVER:
        params.append("TrustServerCertificate=yes")

    return ";".join(params) + ";"


@contextmanager
def get_db_connection():
    """Generador contextual para obtener una conexión segura a SQL Server mediante pyodbc."""
    conn_str = build_connection_string()
    conn = None
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        yield conn
    except pyodbc.Error as e:
        raise RuntimeError(f"Error al conectar con SQL Server ({settings.DB_NAME}): {e}") from e
    finally:
        if conn:
            conn.close()


def test_db_connection() -> bool:
    """Verifica si la conexión a la base de datos ClimaFacilDB responde correctamente."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"[ERROR DB] Fallo al verificar conexión: {e}")
        return False
