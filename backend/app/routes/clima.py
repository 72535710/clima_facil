from fastapi import APIRouter, HTTPException, status
from app.schemas.clima import ClimaActualResponse, PronosticoDiaItem
from app.services.open_meteo import (
    obtener_clima_actual_open_meteo,
    obtener_pronostico_open_meteo,
)

router = APIRouter(prefix="/api/clima", tags=["Clima"])


@router.get(
    "/actual",
    response_model=ClimaActualResponse,
    summary="Consultar clima actual de Huancayo",
    description="Consulta la API de Open-Meteo y devuelve temperatura, humedad, probabilidad de lluvia, precipitación, viento y descripción sencilla.",
)
async def get_clima_actual():
    try:
        datos = await obtener_clima_actual_open_meteo()
        return datos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al consultar el servicio meteorológico Open-Meteo: {e}",
        )


@router.get(
    "/pronostico",
    response_model=list[PronosticoDiaItem],
    summary="Consultar pronóstico de siete días",
    description="Devuelve el pronóstico de 7 días con fecha, día de la semana, temperaturas máxima y mínima, probabilidad máxima de lluvia y descripción sencilla.",
)
async def get_clima_pronostico():
    try:
        pronostico = await obtener_pronostico_open_meteo()
        return pronostico
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al obtener el pronóstico de Open-Meteo: {e}",
        )
