from pydantic import BaseModel, Field


class ClimaActualResponse(BaseModel):
    ubicacion: str = Field(default="Huancayo, Valle del Mantaro", description="Nombre de la zona de consulta")
    temperatura: float = Field(..., description="Temperatura en grados Celsius")
    humedad: float = Field(..., description="Humedad relativa del aire en porcentaje (%)")
    probabilidad_lluvia: float = Field(..., description="Probabilidad de lluvia estimada (%)")
    precipitacion: float = Field(..., description="Precipitación acumulada o esperada en milímetros (mm)")
    viento: float = Field(..., description="Velocidad del viento en kilómetros por hora (km/h)")
    descripcion: str = Field(..., description="Descripción sencilla de las condiciones del cielo")
    fecha_hora: str = Field(..., description="Fecha y hora de la observación")


class PronosticoDiaItem(BaseModel):
    fecha: str = Field(..., description="Fecha en formato YYYY-MM-DD")
    dia_semana: str = Field(..., description="Nombre del día (ej. Lunes, Martes)")
    temperatura_maxima: float = Field(..., description="Temperatura máxima prevista en °C")
    temperatura_minima: float = Field(..., description="Temperatura mínima prevista en °C")
    probabilidad_lluvia: float = Field(..., description="Probabilidad máxima de lluvia estimada (%)")
    precipitacion_mm: float = Field(default=0.0, description="Precipitación total esperada en mm")
    descripcion: str = Field(..., description="Descripción sencilla del estado del clima")


class PronosticoResponse(BaseModel):
    ubicacion: str = Field(default="Huancayo, Valle del Mantaro")
    total_dias: int = Field(default=7)
    pronostico: list[PronosticoDiaItem]
