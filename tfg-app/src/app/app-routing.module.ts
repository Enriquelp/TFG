import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BusquedaComponent } from './busqueda/busqueda.component';

const routes: Routes = [
  {
    path:'',
    component:HomeComponent
  },
  {
    path:'busqueda',
    component:BusquedaComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }