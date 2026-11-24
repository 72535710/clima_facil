from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.recomendacion import RecomendacionResponse
from app.services.db_service import listar_recomendaciones_db

router = APIRouter(prefix="/api/recomendaciones", tags=["Recomendaciones"])


@router.get(
    "",
    response_model=list[RecomendacionResponse],
    summary="Listar recomendaciones agrícolas",
    description="Devuelve las recomendaciones agrícolas existentes en SQL Server mediante sp_ListarRecomendaciones, permitiendo filtro opcional por id_cultivo.",
)
def get_recomendaciones(
    id_cultivo: int | None = Query(
        default=None,
        ge=1,
        description="Filtrar opcionalmente por identificador del cultivo (1: Papa, 2: Maiz, 3: Haba)",
    )
):
    try:
        recomendaciones = listar_recomendaciones_db(id_cultivo=id_cultivo)
        return recomendaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar recomendaciones en la base de datos: {e}",
        )
