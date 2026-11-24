import { provideZonelessChangeDetection } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Subject } from 'rxjs';
import { ClimaActual } from '../../models/clima.model';
import { Recomendacion } from '../../models/recomendacion.model';
import { ClimaService } from '../../services/clima.service';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { InicioComponent } from './inicio';

describe('InicioComponent', () => {
  let clima$: Subject<ClimaActual>;
  let recomendacion$: Subject<Recomendacion | null>;

  beforeEach(async () => {
    clima$ = new Subject<ClimaActual>();
    recomendacion$ = new Subject<Recomendacion | null>();

    await TestBed.configureTestingModule({
      imports: [InicioComponent],
      providers: [
        provideZonelessChangeDetection(),
        provideRouter([]),
        {
          provide: ClimaService,
          useValue: { obtenerClimaActual: () => clima$.asObservable() }
        },
        {
          provide: RecomendacionesService,
          useValue: {
            obtenerRecomendacionDestacada: () => recomendacion$.asObservable()
          }
        }
      ]
    }).compileComponents();
  });

  it('updates the view when the API subscriptions emit', async () => {
    const fixture = TestBed.createComponent(InicioComponent);
    fixture.detectChanges();

    clima$.next({
      ubicacion: 'Huancayo',
      temperatura: 13.4,
      humedad: 79,
      probabilidad_lluvia: 96,
      precipitacion: 0,
      viento: 0.8,
      descripcion: 'Cielo nublado',
      fecha_hora: '2026-11-23T23:15'
    });
    recomendacion$.next({
      id_recomendacion: 5,
      cultivo: 'Haba',
      condicion_climatica: 'helada_probable',
      nivel: 'Importante',
      mensaje: 'Proteger el cultivo ante heladas.'
    });

    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('13.4°C');
    expect(fixture.nativeElement.textContent).toContain('Proteger el cultivo ante heladas.');
    expect(fixture.nativeElement.textContent).not.toContain('Consultando datos meteorológicos');
    expect(fixture.nativeElement.textContent).not.toContain('Cargando recomendación desde SQL Server');
  });

  it('renders API errors and clears the loading indicators', async () => {
    const fixture = TestBed.createComponent(InicioComponent);
    fixture.detectChanges();

    clima$.error(new Error('weather unavailable'));
    recomendacion$.error(new Error('recommendations unavailable'));

    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('Error al obtener el clima:');
    expect(fixture.nativeElement.textContent).toContain('No se pudieron cargar las recomendaciones');
    expect(fixture.nativeElement.textContent).not.toContain('Consultando datos meteorológicos');
    expect(fixture.nativeElement.textContent).not.toContain('Cargando recomendación desde SQL Server');
  });
});
