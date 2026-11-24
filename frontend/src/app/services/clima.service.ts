import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ClimaActual, PronosticoDia } from '../models/clima.model';
import { API_BASE_URL } from '../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class ClimaService {
  private readonly baseUrl: string = API_BASE_URL;

  constructor(private http: HttpClient) {}

  obtenerClimaActual(): Observable<ClimaActual> {
    return this.http.get<ClimaActual>(`${this.baseUrl}/api/clima/actual`);
  }

  obtenerPronostico(): Observable<PronosticoDia[]> {
    return this.http.get<PronosticoDia[]>(`${this.baseUrl}/api/clima/pronostico`);
  }

  obtenerIconoClima(descripcion: string | undefined): string {
    if (!descripcion) return 'bi-cloud-sun text-secondary';
    const d = descripcion.toLowerCase();
    if (d.includes('tormenta')) return 'bi-cloud-lightning-rain-fill text-danger';
    if (d.includes('llovizna') || d.includes('chubasco')) return 'bi-cloud-drizzle-fill text-info';
    if (d.includes('lluvia')) return 'bi-cloud-rain-heavy-fill text-primary';
    if (d.includes('despejado') || d.includes('sol')) return 'bi-sun-fill text-warning';
    if (d.includes('parcialmente') || d.includes('mayormente')) return 'bi-cloud-sun-fill text-warning';
    if (d.includes('nublado')) return 'bi-cloud-fill text-secondary';
    if (d.includes('niebla') || d.includes('neblina')) return 'bi-cloud-fog2-fill text-secondary';
    return 'bi-cloud-sun text-secondary';
  }
}
