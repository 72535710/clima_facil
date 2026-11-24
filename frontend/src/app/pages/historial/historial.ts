import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { ClimaService } from '../../services/clima.service';
import { Historial, Recomendacion, HistorialRegistroRequest } from '../../models/recomendacion.model';
import { ClimaActual } from '../../models/clima.model';

@Component({
  selector: 'app-historial',
  imports: [CommonModule, FormsModule],
  templateUrl: './historial.html',
  styleUrl: './historial.css'
})
export class HistorialComponent implements OnInit {
  registrosHistorial: Historial[] = [];
  recomendacionesDisponibles: Recomendacion[] = [];
  climaActual?: ClimaActual;

  cargando = true;
  error: string | null = null;

  // Formulario para registro explícito
  mostrarFormularioRegistro = false;
  guardando = false;
  idRecomendacionSeleccionada: number = 1;
  mensajeExito: string | null = null;
  mensajeErrorRegistro: string | null = null;

  constructor(
    private recomendacionesService: RecomendacionesService,
    private climaService: ClimaService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarHistorial();
    this.cargarDatosAuxiliares();
  }

  cargarHistorial(): void {
    this.cargando = true;
    this.error = null;
    this.recomendacionesService.obtenerHistorial().subscribe({
      next: (datos) => {
        this.registrosHistorial = datos;
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        this.error = 'No se pudo obtener el historial desde SQL Server. Verifica la conexión con el backend.';
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  cargarDatosAuxiliares(): void {
    // Cargar recomendaciones disponibles para el registro manual explícito
    this.recomendacionesService.obtenerRecomendaciones().subscribe({
      next: (recs) => {
        this.recomendacionesDisponibles = recs;
        if (recs.length > 0) {
          this.idRecomendacionSeleccionada = recs[0].id_recomendacion;
        }
        this.changeDetectorRef.markForCheck();
      }
    });

    // Cargar clima actual de Open-Meteo para precargar métricas
    this.climaService.obtenerClimaActual().subscribe({
      next: (clima) => {
        this.climaActual = clima;
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  toggleFormularioRegistro(): void {
    this.mostrarFormularioRegistro = !this.mostrarFormularioRegistro;
    this.mensajeExito = null;
    this.mensajeErrorRegistro = null;
    this.changeDetectorRef.markForCheck();
  }

  registrarConsultaExplicita(): void {
    if (this.guardando) return;

    if (!this.idRecomendacionSeleccionada) {
      this.mensajeErrorRegistro = 'Por favor selecciona una recomendación.';
      return;
    }

    if (!this.climaActual) {
      this.mensajeErrorRegistro = 'No hay datos climáticos actuales disponibles. Espera a que carguen o vuelve a consultar el clima antes de guardar.';
      return;
    }

    this.guardando = true;
    this.mensajeExito = null;
    this.mensajeErrorRegistro = null;

    const payload: HistorialRegistroRequest = {
      id_ubicacion: 1, // Huancayo
      id_recomendacion: Number(this.idRecomendacionSeleccionada),
      temperatura: this.climaActual.temperatura,
      probabilidad_lluvia: this.climaActual.probabilidad_lluvia,
      precipitacion_mm: this.climaActual.precipitacion,
      humedad: this.climaActual.humedad,
      viento_kmh: this.climaActual.viento
    };

    this.recomendacionesService.registrarHistorial(payload).subscribe({
      next: (resp) => {
        this.mensajeExito = `¡Consulta registrada con éxito en SQL Server (ID #${resp.id_historial})!`;
        this.guardando = false;
        this.mostrarFormularioRegistro = false;
        // Recargar la tabla con el nuevo registro
        this.cargarHistorial();
        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        this.mensajeErrorRegistro = 'Error al registrar la consulta en el historial de SQL Server.';
        this.guardando = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  obtenerClaseNivel(nivel: string): string {
    const n = nivel.toLowerCase();
    if (n.includes('importante') || n.includes('urgente')) return 'badge-alerta';
    if (n.includes('precaucion') || n.includes('precaución')) return 'badge-precaucion';
    return 'badge-favorable';
  }
}
