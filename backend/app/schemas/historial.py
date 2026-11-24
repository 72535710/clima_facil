from pydantic import BaseModel, Field


class HistorialRegistroRequest(BaseModel):
    id_ubicacion: int = Field(..., ge=1, description="ID de la ubicación en la tabla Ubicacion")
    id_recomendacion: int = Field(..., ge=1, description="ID de la recomendación en la tabla Recomendacion")
    temperatura: float = Field(..., description="Temperatura registrada en °C")
    probabilidad_lluvia: float = Field(..., ge=0, le=100, description="Probabilidad de lluvia registrada (0-100%)")
    precipitacion_mm: float = Field(..., ge=0, description="Precipitación registrada en mm")
    humedad: float = Field(..., ge=0, le=100, description="Humedad relativa en porcentaje (0-100%)")
    viento_kmh: float = Field(..., ge=0, description="Velocidad del viento en km/h")


class HistorialResponse(BaseModel):
    id_historial: int
    ubicacion: str
    cultivo: str
    nivel: str
    mensaje: str
    fecha_consulta: str
    temperatura: float
    probabilidad_lluvia: float
    precipitacion_mm: float
    humedad: float
    viento_kmh: float


class HistorialRegistroResponse(BaseModel):
    id_historial: int
    mensaje: str = "Registro en historial creado correctamente"
