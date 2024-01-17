import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BusquedaBdComponent } from './busqueda-bd/busqueda-bd.component';
import { BusquedaOnlineComponent } from './busqueda-online/busqueda-online.component';

const routes: Routes = [
  {
    path:'',
    component:HomeComponent
  },
  {
    path:'busqueda-bd',
    component:BusquedaBdComponent
  },
  {
    path:'busqueda-online',
    component:BusquedaOnlineComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }