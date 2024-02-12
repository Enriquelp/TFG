import { Component, AfterViewInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { AppService } from '../services/app.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';



@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})

export class BusquedaComponent implements AfterViewInit {

  constructor(private service : AppService){}

  datosBusqueda: Articulo[] = []
  displayedColumns: string[] = ['Titulo', 'Citas', 'Autor 1', 'Autor 2', 'Resto autores', 'Año de publicación', 'Enlace'];
  dataSource = new MatTableDataSource<Articulo>(this.datosBusqueda);

  @ViewChild(MatPaginator)
  paginator!: MatPaginator;
  @ViewChild(MatSort) 
  sort!: MatSort;

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  busqueda: string = ""
  idioma: string = ""
  paginas: number = 0
  error!: string 
  cargando: boolean = false;
  botonDesactivado: boolean = false;


  guardarDatos(){
    console.log('Datos guardados:', this.busqueda, this.idioma, this.paginas);
  }
  
  buscarEnBD() {
    this.botonDesactivado = true
    console.log('Buscando en base de datos.');
  }

  async buscarEnInternet() {
    this.cargando = true
    this.botonDesactivado = false
    console.log('Buscando en Google Schoolar.');
    this.service.getBusquedaOnline(this.busqueda, this.idioma, this.paginas).pipe(
      catchError(err => {
        this.error = 'Ha ocurrido un error al obtener los datos.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      this.datosBusqueda = response
      this.error = ''
      console.log(this.datosBusqueda)
      this.cargando = false
      this.dataSource.data = this.datosBusqueda;
    })
  }

  subirABD(){
    console.log('Subiendo busqueda a base de datos')
  }

}

export interface Articulo{
  Titulo: string;
  Citas: number;
  'Autor 1': string;
  'Autor 2': string;
  'Resto autores': string;
  'Año': number;
  Enlace: string;
}

