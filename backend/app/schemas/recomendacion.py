from pydantic import BaseModel, Field


class RecomendacionResponse(BaseModel):
    id_recomendacion: int = Field(..., description="Identificador único de la recomendación")
    cultivo: str = Field(..., description="Nombre del cultivo al que aplica")
    condicion_climatica: str = Field(..., description="Condición meteorológica desencadenante (ej. lluvia_alta, helada_probable, calor_intenso)")
    nivel: str = Field(..., description="Nivel de atención de la recomendación (ej. Precaucion, Importante)")
    mensaje: str = Field(..., description="Mensaje con el consejo agrícola claro y comprensible")
