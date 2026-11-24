"""
Módulo de Reglas y Umbrales Meteorológicos de Orientación Agrícola.

IMPORTANTE / AVISO:
Las reglas de evaluación y umbrales definidos en este módulo son de carácter estrictamente
orientativo con fines académicos para apoyo a los pequeños agricultores del Valle del Mantaro.
NO constituyen alertas meteorológicas oficiales emitidas por el Servicio Nacional de Meteorología
e Hidrología del Perú (SENAMHI).
"""

SENAMHI_DISCLAIMER: str = (
    "Aviso: Las reglas y umbrales meteorológicos son de carácter orientativo con fines académicos "
    "para apoyo a pequeños productores del Valle del Mantaro. No constituyen alertas oficiales de SENAMHI."
)

# Umbrales centralizados para el clima de Huancayo / Sierra Central (aprox. 3,250 m s.n.m.)
# 1. Helada probable: temperatura mínima <= 4.0 °C (frecuente en madrugadas secas o noches despejadas)
UMBRAL_HELADA_TEMP_C: float = 4.0

# 2. Lluvia alta: probabilidad de lluvia >= 60% o precipitación acumulada >= 5.0 mm
UMBRAL_LLUVIA_ALTA_PROB: float = 60.0
UMBRAL_LLUVIA_ALTA_MM: float = 5.0

# 3. Calor intenso: temperatura máxima >= 22.0 °C (alta radiación solar en altitud)
UMBRAL_CALOR_INTENSO_TEMP_C: float = 22.0


def evaluar_condiciones_meteorologicas(
    temperatura: float,
    probabilidad_lluvia: float,
    precipitacion_mm: float,
    temperatura_minima: float | None = None,
) -> list[str]:
    """
    Evalúa las métricas meteorológicas contra los umbrales orientativos y retorna
    las etiquetas coincidentes con la base de datos: 'lluvia_alta', 'helada_probable', 'calor_intenso'.
    """
    condiciones_detectadas: list[str] = []

    # Evaluación de helada probable
    temp_ref_frio = temperatura_minima if temperatura_minima is not None else temperatura
    if temp_ref_frio <= UMBRAL_HELADA_TEMP_C:
        condiciones_detectadas.append("helada_probable")

    # Evaluación de lluvia alta
    if probabilidad_lluvia >= UMBRAL_LLUVIA_ALTA_PROB or precipitacion_mm >= UMBRAL_LLUVIA_ALTA_MM:
        condiciones_detectadas.append("lluvia_alta")

    # Evaluación de calor intenso / fuerte radiación solar
    if temperatura >= UMBRAL_CALOR_INTENSO_TEMP_C:
        condiciones_detectadas.append("calor_intenso")

    return condiciones_detectadas
