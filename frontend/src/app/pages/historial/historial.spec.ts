import { provideZonelessChangeDetection } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { ClimaActual } from '../../models/clima.model';
import { Historial, Recomendacion, HistorialRegistroResponse } from '../../models/recomendacion.model';
import { ClimaService } from '../../services/clima.service';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { HistorialComponent } from './historial';

const HISTORIAL_MOCK: Historial[] = [
  {
    id_historial: 6,
    ubicacion: 'Huancayo',
    cultivo: 'Papa',
    nivel: 'Precaucion',
    mensaje: 'Revisa que el terreno tenga buen drenaje.',
    fecha_consulta: '2026-11-23 23:44:53',
    temperatura: 13.4,
    probabilidad_lluvia: 96.0,
    precipitacion_mm: 0.0,
    humedad: 79.0,
    viento_kmh: 0.9
  }
];

const RECS_MOCK: Recomendacion[] = [
  {
    id_recomendacion: 1,
    cultivo: 'Papa',
    condicion_climatica: 'lluvia_alta',
    nivel: 'Precaucion',
    mensaje: 'Revisa que el terreno tenga buen drenaje.'
  }
];

const CLIMA_MOCK: ClimaActual = {
  ubicacion: 'Huancayo',
  temperatura: 13.4,
  humedad: 79,
  probabilidad_lluvia: 96,
  precipitacion: 0,
  viento: 0.9,
  descripcion: 'Cielo nublado',
  fecha_hora: '2026-11-23T23:44'
};

describe('HistorialComponent', () => {
  let historial$: Subject<Historial[]>;
  let recs$: Subject<Recomendacion[]>;
  let clima$: Subject<ClimaActual>;
  let registrarCalls: number;

  beforeEach(async () => {
    historial$ = new Subject<Historial[]>();
    recs$ = new Subject<Recomendacion[]>();
    clima$ = new Subject<ClimaActual>();
    registrarCalls = 0;

    await TestBed.configureTestingModule({
      imports: [HistorialComponent],
      providers: [
        provideZonelessChangeDetection(),
        {
          provide: RecomendacionesService,
          useValue: {
            obtenerHistorial: () => historial$.asObservable(),
            obtenerRecomendaciones: () => recs$.asObservable(),
            registrarHistorial: () => {
              registrarCalls++;
              return new Subject<HistorialRegistroResponse>().asObservable();
            }
          }
        },
        {
          provide: ClimaService,
          useValue: {
            obtenerClimaActual: () => clima$.asObservable()
          }
        }
      ]
    }).compileComponents();
  });

  it('muestra el spinner mientras carga y la tabla al recibir el historial', async () => {
    const fixture = TestBed.createComponent(HistorialComponent);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Consultando historial en SQL Server');

    historial$.next(HISTORIAL_MOCK);
    recs$.next(RECS_MOCK);
    clima$.next(CLIMA_MOCK);
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Consultando historial en SQL Server');
    expect(fixture.nativeElement.textContent).toContain('Papa');
    expect(fixture.nativeElement.textContent).toContain('13.4°C');
  });

  it('oculta el spinner y muestra el error cuando la API falla', async () => {
    const fixture = TestBed.createComponent(HistorialComponent);
    fixture.detectChanges();

    historial$.error(new Error('error SQL Server'));
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Consultando historial en SQL Server');
    expect(fixture.nativeElement.textContent).toContain('No se pudo obtener el historial desde SQL Server');
    expect(fixture.nativeElement.querySelector('button')).toBeTruthy();
  });

  it('no registra datos simulados ni permite envíos repetidos sin clima', async () => {
    const fixture = TestBed.createComponent(HistorialComponent);
    fixture.detectChanges();
    fixture.componentInstance.toggleFormularioRegistro();
    await fixture.whenStable();

    fixture.componentInstance.registrarConsultaExplicita();
    fixture.componentInstance.registrarConsultaExplicita();

    expect(registrarCalls).toBe(0);
    expect(fixture.nativeElement.textContent).toContain('Datos climáticos no disponibles');
  });
});
