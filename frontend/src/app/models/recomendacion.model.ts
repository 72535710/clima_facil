export interface Recomendacion {
  id_recomendacion: number;
  cultivo: string;
  condicion_climatica: string;
  nivel: string;
  mensaje: string;
}

export interface Historial {
  id_historial: number;
  ubicacion: string;
  cultivo: string;
  nivel: string;
  mensaje: string;
  fecha_consulta: string;
  temperatura: number;
  probabilidad_lluvia: number;
  precipitacion_mm: number;
  humedad: number;
  viento_kmh: number;
}

export interface HistorialRegistroRequest {
  id_ubicacion: number;
  id_recomendacion: number;
  temperatura: number;
  probabilidad_lluvia: number;
  precipitacion_mm: number;
  humedad: number;
  viento_kmh: number;
}

export interface HistorialRegistroResponse {
  id_historial: number;
  mensaje: string;
}
