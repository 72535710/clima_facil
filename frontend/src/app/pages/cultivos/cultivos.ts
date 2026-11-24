import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CultivosService } from '../../services/cultivos.service';
import { Cultivo } from '../../models/cultivo.model';

@Component({
  selector: 'app-cultivos',
  imports: [CommonModule],
  templateUrl: './cultivos.html',
  styleUrl: './cultivos.css'
})
export class CultivosComponent implements OnInit {
  cultivos: Cultivo[] = [];
  cargando = true;
  error: string | null = null;

  constructor(
    public cultivosService: CultivosService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarCultivos();
  }

  cargarCultivos(): void {
    this.cargando = true;
    this.error = null;
    this.cultivosService.obtenerCultivos().subscribe({
      next: (datos) => {
        this.cultivos = datos;
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        this.error = 'No se pudo conectar con la base de datos SQL Server para obtener los cultivos.';
        this.cargando = false;
        this.changeDetectorRef.markForCheck();
      }
    });
  }
}
