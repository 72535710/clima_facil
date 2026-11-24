import { provideZonelessChangeDetection } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { Cultivo } from '../../models/cultivo.model';
import { CultivosService } from '../../services/cultivos.service';
import { CultivosComponent } from './cultivos';

const CULTIVOS_MOCK: Cultivo[] = [
  { id_cultivo: 1, nombre: 'Papa', descripcion: 'Tubérculo andino resistente al frío.' },
  { id_cultivo: 2, nombre: 'Maíz', descripcion: 'Cereal de alto rendimiento.' }
];

describe('CultivosComponent', () => {
  let cultivos$: Subject<Cultivo[]>;

  beforeEach(async () => {
    cultivos$ = new Subject<Cultivo[]>();

    await TestBed.configureTestingModule({
      imports: [CultivosComponent],
      providers: [
        provideZonelessChangeDetection(),
        {
          provide: CultivosService,
          useValue: {
            obtenerCultivos: () => cultivos$.asObservable(),
            obtenerIconoCultivo: (_: string) => 'bi-flower2 text-success'
          }
        }
      ]
    }).compileComponents();
  });

  it('muestra el spinner mientras carga y el catálogo al recibir respuesta', async () => {
    const fixture = TestBed.createComponent(CultivosComponent);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Cargando cultivos desde SQL Server');

    cultivos$.next(CULTIVOS_MOCK);
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Cargando cultivos desde SQL Server');
    expect(fixture.nativeElement.textContent).toContain('Papa');
    expect(fixture.nativeElement.textContent).toContain('Maíz');
  });

  it('oculta el spinner y muestra el error cuando la API falla', async () => {
    const fixture = TestBed.createComponent(CultivosComponent);
    fixture.detectChanges();

    cultivos$.error(new Error('conexión rechazada'));
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).not.toContain('Cargando cultivos desde SQL Server');
    expect(fixture.nativeElement.textContent).toContain('No se pudo conectar con la base de datos SQL Server');
    expect(fixture.nativeElement.querySelector('button')).toBeTruthy();
  });
});
