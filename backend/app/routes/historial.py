from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.historial import (
    HistorialRegistroRequest,
    HistorialResponse,
    HistorialRegistroResponse,
)
from app.services.db_service import listar_historial_db, registrar_historial_db

router = APIRouter(prefix="/api/historial", tags=["Historial"])


@router.get(
    "",
    response_model=list[HistorialResponse],
    summary="Listar historial de recomendaciones",
    description="Devuelve el historial de consultas de recomendaciones mediante sp_ListarHistorial, con filtro opcional por id_ubicacion.",
)
def get_historial(
    id_ubicacion: int | None = Query(
        default=None,
        ge=1,
        description="Filtrar opcionalmente por identificador de ubicación (1: Huancayo)",
    )
):
    try:
        historial = listar_historial_db(id_ubicacion=id_ubicacion)
        return historial
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el historial de la base de datos: {e}",
        )


@router.post(
    "",
    response_model=HistorialRegistroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar consulta en el historial",
    description="Inserta un nuevo registro en la tabla Historial mediante el procedimiento almacenado sp_RegistrarHistorial.",
)
def create_historial_registro(datos: HistorialRegistroRequest):
    try:
        nuevo_id = registrar_historial_db(
            id_ubicacion=datos.id_ubicacion,
            id_recomendacion=datos.id_recomendacion,
            temperatura=datos.temperatura,
            probabilidad_lluvia=datos.probabilidad_lluvia,
            precipitacion_mm=datos.precipitacion_mm,
            humedad=datos.humedad,
            viento_kmh=datos.viento_kmh,
        )
        return HistorialRegistroResponse(
            id_historial=nuevo_id,
            mensaje="Consulta de recomendación registrada con éxito en el historial.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar en el historial: {e}",
        )
