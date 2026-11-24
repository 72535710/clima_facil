import { Routes } from '@angular/router';
import { InicioComponent } from './pages/inicio/inicio';
import { PronosticoComponent } from './pages/pronostico/pronostico';
import { RecomendacionesComponent } from './pages/recomendaciones/recomendaciones';
import { CultivosComponent } from './pages/cultivos/cultivos';
import { HistorialComponent } from './pages/historial/historial';

export const routes: Routes = [
  { path: '', redirectTo: 'inicio', pathMatch: 'full' },
  { path: 'inicio', component: InicioComponent },
  { path: 'pronostico', component: PronosticoComponent },
  { path: 'recomendaciones', component: RecomendacionesComponent },
  { path: 'cultivos', component: CultivosComponent },
  { path: 'historial', component: HistorialComponent },
  { path: '**', redirectTo: 'inicio' }
];
