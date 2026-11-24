import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cultivo } from '../models/cultivo.model';
import { API_BASE_URL } from '../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class CultivosService {
  private readonly baseUrl: string = API_BASE_URL;

  constructor(private http: HttpClient) {}

  obtenerCultivos(): Observable<Cultivo[]> {
    return this.http.get<Cultivo[]>(`${this.baseUrl}/api/cultivos`);
  }

  obtenerIconoCultivo(nombre: string | undefined): string {
    if (!nombre) return 'bi-flower2 text-success';
    const n = nombre.toLowerCase();
    if (n.includes('papa')) return 'bi-record-circle-fill text-success';
    if (n.includes('maiz') || n.includes('maíz')) return 'bi-flower1 text-warning-emphasis';
    if (n.includes('haba')) return 'bi-seedling text-success';
    return 'bi-flower2 text-success';
  }
}
