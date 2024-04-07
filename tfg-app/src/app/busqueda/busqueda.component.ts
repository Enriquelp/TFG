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
  busquedaAnterior: [] = []
  articulos_displayedColumns: string[] = ['Titulo', 'Citas', 'Autor 1', 'Autor 2', 'Autor 3', 'Año de publicación', 'Enlace'];
  articulos_dataSource = new MatTableDataSource<Articulo>(this.datosBusqueda);

  busquedas_displayedColumns: string[] = ['Titulo', 'Citas', 'Autor 1', 'Autor 2', 'Autor 3', 'Año de publicación', 'Enlace'];
  busquedas_dataSource = new MatTableDataSource<Articulo>(this.datosBusqueda);

  @ViewChild(MatPaginator)
  paginator!: MatPaginator;
  @ViewChild(MatSort) 
  sort!: MatSort;

  ngAfterViewInit() {
    this.articulos_dataSource.paginator = this.paginator;
    this.articulos_dataSource.sort = this.sort;
  }

  busqueda: string = ""
  idioma: string = ""
  paginas: number = 0
  error!: string 
  cargando: boolean = false;


  almacenarDatos(busqueda:string , listaArticulos: Articulo[]){
    console.log('Datos guardados:', busqueda, listaArticulos);
    this.service.postGuardarBusqueda(busqueda, listaArticulos).pipe(
      catchError(err => {
        this.error = 'Ha ocurrido un error al almacenar la busqueda.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      console.log('Búsqueda y artículos guardados correctamente:', response);
    })

  }
  
  cargarBusquedasAnteriores() {
    console.log('Cargando busquedas anteriores.');
    this.service.getBusquedasAnteriores().pipe(
      catchError(err => {
        this.error = 'Error al cargar busquedas anteriores.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      this.busquedaAnterior = response;
      this.error = ''
      console.log(this.busquedaAnterior)
    })
  }

  onClickFila(rdo:any){
    console.log("Se hizo clic en la fila:", rdo);
    this.service.getBusquedasArticulos(rdo[0]).pipe(
      catchError(err => {
        this.error = 'Error al obtener los articulos de la busqueda seleccionada.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      this.datosBusqueda = response
      this.error = ''
      console.log(this.datosBusqueda)
      this.cargando = false
      this.articulos_dataSource.data = this.datosBusqueda;
    })
  }

  async buscarEnInternet() {
    this.cargando = true
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
      this.articulos_dataSource.data = this.datosBusqueda;
      this.almacenarDatos(this.busqueda, this.datosBusqueda)
    })
  }
}

export interface Articulo{
  Titulo: string;
  Citas: number;
  'Autor 1': string;
  'Autor 2': string;
  'Autor 3': string;
  'Año': number;
  Enlace: string;
}

