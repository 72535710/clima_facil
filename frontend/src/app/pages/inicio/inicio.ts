import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ClimaService } from '../../services/clima.service';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { ClimaActual } from '../../models/clima.model';
import { Recomendacion } from '../../models/recomendacion.model';

@Component({
  selector: 'app-inicio',
  imports: [CommonModule, RouterLink],
  templateUrl: './inicio.html',
  styleUrl: './inicio.css'
})
export class InicioComponent implements OnInit {
  clima?: ClimaActual;
  recomendacionDestacada?: Recomendacion;

  cargandoClima = true;
  cargandoRecomendacion = true;
  errorClima: string | null = null;
  errorRecomendacion: string | null = null;

  guardandoHistorial = false;
  mensajeHistorialExito: string | null = null;
  mensajeHistorialError: string | null = null;

  constructor(
    public climaService: ClimaService,
    private recomendacionesService: RecomendacionesService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargarClima();
    this.cargarRecomendacion();
  }

  cargarClima(): void {
    this.cargandoClima = true;
    this.errorClima = null;
    this.climaService.obtenerClimaActual().subscribe({
      next: (datos) => {
        this.clima = datos;
        this.cargandoClima = false;
        this.changeDetectorRef.markForCheck();
      },
      error: () => {
        this.errorClima = 'No se pudo conectar con el servicio meteorológico. Verifica que el servidor backend esté activo.';
        this.cargandoClima = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  cargarRecomendacion(): void {
    this.cargandoRecomendacion = true;
    this.errorRecomendacion = null;
    this.recomendacionesService.obtenerRecomendacionDestacada().subscribe({
      next: (rec) => {
        this.recomendacionDestacada = rec ?? undefined;
        this.cargandoRecomendacion = false;
        this.changeDetectorRef.markForCheck();
      },
      error: () => {
        this.errorRecomendacion = 'No se pudieron cargar las recomendaciones desde la base de datos SQL Server.';
        this.cargandoRecomendacion = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  guardarConsultaEnHistorial(): void {
    if (!this.clima || !this.recomendacionDestacada || this.guardandoHistorial) return;

    this.guardandoHistorial = true;
    this.mensajeHistorialExito = null;
    this.mensajeHistorialError = null;

    const payload = {
      id_ubicacion: 1, // Huancayo
      id_recomendacion: this.recomendacionDestacada.id_recomendacion,
      temperatura: this.clima.temperatura,
      probabilidad_lluvia: this.clima.probabilidad_lluvia,
      precipitacion_mm: this.clima.precipitacion,
      humedad: this.clima.humedad,
      viento_kmh: this.clima.viento
    };

    this.recomendacionesService.registrarHistorial(payload).subscribe({
      next: (resp) => {
        this.mensajeHistorialExito = `Consulta guardada en el historial con ID #${resp.id_historial}.`;
        this.guardandoHistorial = false;
        this.changeDetectorRef.markForCheck();
      },
      error: () => {
        this.mensajeHistorialError = 'No se pudo registrar la consulta en la base de datos.';
        this.guardandoHistorial = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }
}
