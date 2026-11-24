import httpx
from datetime import datetime
from app.config import settings

# Diccionario de interpretación sencilla de códigos meteorológicos WMO
WMO_DESCRIPCIONES: dict[int, str] = {
    0: "Cielo despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Cielo nublado",
    45: "Neblina",
    48: "Niebla densa",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna continua",
    56: "Llovizna fría",
    57: "Llovizna fría densa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    66: "Lluvia helada ligera",
    67: "Lluvia helada intensa",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada intensa",
    77: "Granizo menudo",
    80: "Chubascos suaves",
    81: "Chubascos moderados",
    82: "Chubascos fuertes",
    85: "Chubascos de nieve ligeros",
    86: "Chubascos de nieve intensos",
    95: "Tormenta eléctrica",
    96: "Tormenta eléctrica con granizo ligero",
    99: "Tormenta eléctrica con granizo fuerte",
}

DIAS_SEMANA_ES: dict[int, str] = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}


def traducir_weather_code(code: int | None) -> str:
    """Traduce el código numérico de Open-Meteo a una descripción sencilla en español."""
    if code is None:
        return "Condición no disponible"
    return WMO_DESCRIPCIONES.get(code, "Tiempo variable")


async def obtener_clima_actual_open_meteo() -> dict:
    """Consulta la API de Open-Meteo para obtener las condiciones meteorológicas actuales de Huancayo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": settings.HUANCAYO_LATITUDE,
        "longitude": settings.HUANCAYO_LONGITUDE,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ],
        "hourly": ["precipitation_probability"],
        "daily": ["precipitation_probability_max"],
        "timezone": "America/Lima",
        "forecast_days": 1,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})
    hourly = data.get("hourly", {})

    # Obtener probabilidad de lluvia estimada para hoy o la hora actual
    prob_lluvia = 0.0
    if daily and "precipitation_probability_max" in daily and daily["precipitation_probability_max"]:
        prob_lluvia = float(daily["precipitation_probability_max"][0])
    elif hourly and "precipitation_probability" in hourly and hourly["precipitation_probability"]:
        prob_lluvia = float(hourly["precipitation_probability"][0])

    temperatura = float(current.get("temperature_2m", 0.0))
    humedad = float(current.get("relative_humidity_2m", 0.0))
    precipitacion = float(current.get("precipitation", 0.0))
    viento = float(current.get("wind_speed_10m", 0.0))
    weather_code = current.get("weather_code")
    descripcion = traducir_weather_code(weather_code)
    fecha_hora = current.get("time", datetime.now().isoformat())

    return {
        "ubicacion": "Huancayo, Valle del Mantaro",
        "temperatura": round(temperatura, 1),
        "humedad": round(humedad, 1),
        "probabilidad_lluvia": round(prob_lluvia, 1),
        "precipitacion": round(precipitacion, 1),
        "viento": round(viento, 1),
        "descripcion": descripcion,
        "fecha_hora": fecha_hora,
    }


async def obtener_pronostico_open_meteo() -> list[dict]:
    """Consulta la API de Open-Meteo para obtener el pronóstico de 7 días para Huancayo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": settings.HUANCAYO_LATITUDE,
        "longitude": settings.HUANCAYO_LONGITUDE,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "precipitation_sum",
        ],
        "timezone": "America/Lima",
        "forecast_days": 7,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    daily = data.get("daily", {})
    fechas = daily.get("time", [])
    weather_codes = daily.get("weather_code", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    prob_lluvias = daily.get("precipitation_probability_max", [])
    precipitaciones = daily.get("precipitation_sum", [])

    dias_resultado = []
    for i in range(len(fechas)):
        fecha_str = fechas[i]
        try:
            dt = datetime.strptime(fecha_str, "%Y-%m-%d")
            dia_nombre = DIAS_SEMANA_ES.get(dt.weekday(), "Día")
        except Exception:
            dia_nombre = "Día"

        code = weather_codes[i] if i < len(weather_codes) else None
        dias_resultado.append({
            "fecha": fecha_str,
            "dia_semana": dia_nombre,
            "temperatura_maxima": round(float(max_temps[i]), 1) if i < len(max_temps) else 0.0,
            "temperatura_minima": round(float(min_temps[i]), 1) if i < len(min_temps) else 0.0,
            "probabilidad_lluvia": round(float(prob_lluvias[i]), 1) if i < len(prob_lluvias) else 0.0,
            "precipitacion_mm": round(float(precipitaciones[i]), 1) if i < len(precipitaciones) else 0.0,
            "descripcion": traducir_weather_code(code),
        })

    return dias_resultado
