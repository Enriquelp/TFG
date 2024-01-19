import { Component } from '@angular/core';


@Component({
  selector: 'app-busqueda-online',
  templateUrl: './busqueda-online.component.html',
  styleUrls: ['./busqueda-online.component.css']
})

export class BusquedaOnlineComponent {

  busqueda: string = ""
  idioma: string = ""
  paginas: number = 0
  
  guardarDatos() {
    console.log('Datos guardados:', this.busqueda, this.idioma, this.paginas);
  }

  buscarEnInternet() {
    console.log('Se ha hecho clic en el botón de buscar.');
  }

}
