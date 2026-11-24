import { provideZonelessChangeDetection } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { PronosticoDia } from '../../models/clima.model';
import { ClimaService } from '../../services/clima.service';
import { PronosticoComponent } from './pronostico';

const DIA_MOCK: PronosticoDia = {
  fecha: '2026-11-24',
  dia_semana: 'Martes',
  temperatura_maxima: 20,
  temperatura_minima: 8,
  probabilidad_lluvia: 60,
  precipitacion_mm: 3.2,
  descripcion: 'Parcialmente nublado'
};

describe('PronosticoComponent', () => {
  let pronostico$: Subject<PronosticoDia[]>;

  beforeEach(async () => {
    pronostico$ = new Subject<PronosticoDia[]>();

    await TestBed.configureTestingModule({
      imports: [PronosticoComponent],
      providers: [
        provideZonelessChangeDetection(),
        {
          provide: ClimaService,
          useValue: {
            obtenerPronostico: () => pronostico$.asObservable(),
            obtenerIconoClima: (_: string) => 'bi-cloud-sun text-secondary'
          }
        }
      ]
    }).compileComponents();
  });

  it('muestra el spinner mientras carga y los datos al recibir respuesta', async () => {
    const fixture = TestBed.createComponent(PronosticoComponent);
    fixture.detectChanges();

    // Durante la carga debe mostrar el spinner
    expect(fixture.nativeElement.textContent).toContain('Obteniendo pronóstico semanal desde Open-Meteo');

    pronostico$.next([DIA_MOCK]);
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Obteniendo pronóstico semanal desde Open-Meteo');
    expect(fixture.nativeElement.textContent).toContain('Martes');
    expect(fixture.nativeElement.textContent).toContain('20°C');
  });

  it('oculta el spinner y muestra el error cuando la API falla', async () => {
    const fixture = TestBed.createComponent(PronosticoComponent);
    fixture.detectChanges();

    pronostico$.error(new Error('error de red'));
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Obteniendo pronóstico semanal desde Open-Meteo');
    expect(fixture.nativeElement.textContent).toContain('No se pudo obtener el pronóstico');
    expect(fixture.nativeElement.querySelector('button')).toBeTruthy();
  });
});
