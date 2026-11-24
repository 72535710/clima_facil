from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import test_db_connection
from app.routes.clima import router as clima_router
from app.routes.cultivos import router as cultivos_router
from app.routes.recomendaciones import router as recomendaciones_router
from app.routes.historial import router as historial_router
from app.services.weather_rules import SENAMHI_DISCLAIMER


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verificación de conexión a SQL Server al iniciar
    db_ok = test_db_connection()
    if db_ok:
        print("[INFO] Conexión exitosa a SQL Server (ClimaFacilDB).")
    else:
        print("[ALERTA] No se pudo verificar la conexión con SQL Server al iniciar.")
    yield


app = FastAPI(
    title="Clima Fácil API",
    version="1.0.0",
    description=(
        "Backend del proyecto académico Clima Fácil, orientado a pequeños agricultores "
        "de Huancayo y el Valle del Mantaro, Perú. Proporciona datos climáticos en tiempo real "
        "desde Open-Meteo y recomendaciones agrícolas almacenadas en SQL Server."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración de CORS para el frontend Angular (http://localhost:4200)
origins = [
    settings.CORS_ORIGIN,
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(clima_router)
app.include_router(cultivos_router)
app.include_router(recomendaciones_router)
app.include_router(historial_router)


@app.get("/", tags=["General"])
def root():
    return {
        "proyecto": "Clima Fácil - Backend API",
        "ambito": "Huancayo y Valle del Mantaro, Junín, Perú",
        "documentacion_swagger": "/docs",
        "estado": "Activo",
        "aviso_meteorologico": SENAMHI_DISCLAIMER,
    }
