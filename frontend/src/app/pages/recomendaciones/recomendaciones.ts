import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { CultivosService } from '../../services/cultivos.service';
import { Recomendacion } from '../../models/recomendacion.model';
import { Cultivo } from '../../models/cultivo.model';

@Component({
  selector: 'app-recomendaciones',
  imports: [CommonModule],
  templateUrl: './recomendaciones.html',
  styleUrl: './recomendaciones.css'
})
export class RecomendacionesComponent implements OnInit {
  recomendaciones: Recomendacion[] = [];
  cultivos: Cultivo[] = [];
  idCultivoSeleccionado: number = 0; // 0 = Todos
  cargando = true;
  error: string | null = null;

  constructor(
    private recomendacionesService: RecomendacionesService,
    private cultivosService: CultivosService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarCultivos();
    this.cargarRecomendaciones(0);
  }

  cargarCultivos(): void {
    this.cultivosService.obtenerCultivos().subscribe({
      next: (data) => {
        this.cultivos = data;
        this.changeDetectorRef.markForCheck();
      },
      error: () => {
        // En caso de fallo se usarán los botones fijos por ID
      }
    });
  }

  cargarRecomendaciones(idCultivo: number): void {
    this.idCultivoSeleccionado = idCultivo;
    this.cargando = true;
    this.error = null;

    const paramId = idCultivo > 0 ? idCultivo : undefined;
    this.recomendacionesService.obtenerRecomendaciones(paramId).subscribe({
      next: (recs) => {
        this.recomendaciones = recs;
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        this.error = 'No se pudieron obtener las recomendaciones desde SQL Server.';
        this.cargando = false;
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
