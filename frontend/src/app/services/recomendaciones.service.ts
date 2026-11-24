import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { 
  Recomendacion, 
  Historial, 
  HistorialRegistroRequest, 
  HistorialRegistroResponse 
} from '../models/recomendacion.model';
import { API_BASE_URL } from '../config/api.config';

@Injectable({
  providedIn: 'root'
})
export class RecomendacionesService {
  private readonly baseUrl: string = API_BASE_URL;

  constructor(private http: HttpClient) {}

  obtenerRecomendaciones(idCultivo?: number): Observable<Recomendacion[]> {
    let params = new HttpParams();
    if (idCultivo !== undefined && idCultivo !== null && idCultivo > 0) {
      params = params.set('id_cultivo', idCultivo.toString());
    }
    return this.http.get<Recomendacion[]>(`${this.baseUrl}/api/recomendaciones`, { params });
  }

  obtenerRecomendacionDestacada(): Observable<Recomendacion | null> {
    return this.obtenerRecomendaciones().pipe(
      map(recs => (recs && recs.length > 0 ? recs[0] : null))
    );
  }

  obtenerHistorial(idUbicacion?: number): Observable<Historial[]> {
    let params = new HttpParams();
    if (idUbicacion !== undefined && idUbicacion !== null && idUbicacion > 0) {
      params = params.set('id_ubicacion', idUbicacion.toString());
    }
    return this.http.get<Historial[]>(`${this.baseUrl}/api/historial`, { params });
  }

  registrarHistorial(datos: HistorialRegistroRequest): Observable<HistorialRegistroResponse> {
    return this.http.post<HistorialRegistroResponse>(`${this.baseUrl}/api/historial`, datos);
  }
}
