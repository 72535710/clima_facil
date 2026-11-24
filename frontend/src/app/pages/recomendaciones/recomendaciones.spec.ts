import { provideZonelessChangeDetection } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { Cultivo } from '../../models/cultivo.model';
import { Recomendacion } from '../../models/recomendacion.model';
import { CultivosService } from '../../services/cultivos.service';
import { RecomendacionesService } from '../../services/recomendaciones.service';
import { RecomendacionesComponent } from './recomendaciones';

const RECS_MOCK: Recomendacion[] = [
  {
    id_recomendacion: 1,
    cultivo: 'Papa',
    condicion_climatica: 'lluvia_intensa',
    nivel: 'Importante',
    mensaje: 'Drenar los campos antes de la siembra.'
  }
];

const CULTIVOS_MOCK: Cultivo[] = [
  { id_cultivo: 1, nombre: 'Papa', descripcion: 'Tubérculo andino.' }
];

describe('RecomendacionesComponent', () => {
  let recs$: Subject<Recomendacion[]>;
  let cultivos$: Subject<Cultivo[]>;

  beforeEach(async () => {
    recs$ = new Subject<Recomendacion[]>();
    cultivos$ = new Subject<Cultivo[]>();

    await TestBed.configureTestingModule({
      imports: [RecomendacionesComponent],
      providers: [
        provideZonelessChangeDetection(),
        {
          provide: RecomendacionesService,
          useValue: {
            obtenerRecomendaciones: () => recs$.asObservable()
          }
        },
        {
          provide: CultivosService,
          useValue: {
            obtenerCultivos: () => cultivos$.asObservable()
          }
        }
      ]
    }).compileComponents();
  });

  it('muestra el spinner mientras carga y las recomendaciones al recibir respuesta', async () => {
    const fixture = TestBed.createComponent(RecomendacionesComponent);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Consultando recomendaciones en SQL Server');

    recs$.next(RECS_MOCK);
    cultivos$.next(CULTIVOS_MOCK);
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Consultando recomendaciones en SQL Server');
    expect(fixture.nativeElement.textContent).toContain('Drenar los campos antes de la siembra.');
    expect(fixture.nativeElement.textContent).toContain('Papa');
  });

  it('oculta el spinner y muestra el error cuando la API falla', async () => {
    const fixture = TestBed.createComponent(RecomendacionesComponent);
    fixture.detectChanges();

    recs$.error(new Error('error SQL Server'));
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Consultando recomendaciones en SQL Server');
    expect(fixture.nativeElement.textContent).toContain('No se pudieron obtener las recomendaciones desde SQL Server');
    expect(fixture.nativeElement.querySelector('button')).toBeTruthy();
  });

  it('muestra los botones de cultivos dinámicos cuando llegan desde la API', async () => {
    const fixture = TestBed.createComponent(RecomendacionesComponent);
    fixture.detectChanges();

    cultivos$.next(CULTIVOS_MOCK);
    recs$.next(RECS_MOCK);
    await fixture.whenStable();

    // El botón dinámico "Papa" debe aparecer (distinto del fallback)
    expect(fixture.nativeElement.textContent).toContain('Papa');
  });
});
