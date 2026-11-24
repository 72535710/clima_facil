import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env ubicado en la raíz del backend
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    # Servidor SQL Server y Base de Datos
    DB_SERVER: str = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
    DB_NAME: str = os.getenv("DB_NAME", "ClimaFacilDB")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_TRUSTED_CONNECTION: str = os.getenv("DB_TRUSTED_CONNECTION", "yes")
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")

    # Coordenadas de Huancayo / Valle del Mantaro
    HUANCAYO_LATITUDE: float = float(os.getenv("HUANCAYO_LATITUDE", "-12.0651"))
    HUANCAYO_LONGITUDE: float = float(os.getenv("HUANCAYO_LONGITUDE", "-75.2049"))

    # Servidor y CORS
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost:4200")


settings = Settings()
