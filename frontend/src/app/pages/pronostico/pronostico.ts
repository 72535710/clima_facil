import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClimaService } from '../../services/clima.service';
import { PronosticoDia } from '../../models/clima.model';

@Component({
  selector: 'app-pronostico',
  imports: [CommonModule],
  templateUrl: './pronostico.html',
  styleUrl: './pronostico.css'
})
export class PronosticoComponent implements OnInit {
  diasPronostico: PronosticoDia[] = [];
  cargando = true;
  error: string | null = null;

  constructor(
    public climaService: ClimaService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarPronostico();
  }

  cargarPronostico(): void {
    this.cargando = true;
    this.error = null;
    this.climaService.obtenerPronostico().subscribe({
      next: (dias) => {
        this.diasPronostico = dias;
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        this.error = 'No se pudo obtener el pronóstico de 7 días desde el servidor meteorológico.';
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }
}
