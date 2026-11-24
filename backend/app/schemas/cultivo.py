from pydantic import BaseModel, Field


class CultivoResponse(BaseModel):
    id_cultivo: int = Field(..., description="Identificador único del cultivo en SQL Server")
    nombre: str = Field(..., description="Nombre común del cultivo (ej. Papa, Maiz, Haba)")
    descripcion: str = Field(..., description="Descripción general del cultivo y sus requerimientos")
