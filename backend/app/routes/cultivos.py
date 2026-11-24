from fastapi import APIRouter, HTTPException, status
from app.schemas.cultivo import CultivoResponse
from app.services.db_service import listar_cultivos_db

router = APIRouter(prefix="/api/cultivos", tags=["Cultivos"])


@router.get(
    "",
    response_model=list[CultivoResponse],
    summary="Listar cultivos",
    description="Devuelve el catálogo de cultivos registrados en SQL Server mediante el procedimiento almacenado sp_ListarCultivos.",
)
def get_cultivos():
    try:
        cultivos = listar_cultivos_db()
        return cultivos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar cultivos en la base de datos: {e}",
        )
