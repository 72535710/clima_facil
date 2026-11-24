export interface ClimaActual {
  ubicacion: string;
  temperatura: number;
  humedad: number;
  probabilidad_lluvia: number;
  precipitacion: number;
  viento: number;
  descripcion: string;
  fecha_hora: string;
}

export interface PronosticoDia {
  fecha: string;
  dia_semana: string;
  temperatura_maxima: number;
  temperatura_minima: number;
  probabilidad_lluvia: number;
  precipitacion_mm: number;
  descripcion: string;
}
