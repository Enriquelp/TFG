import { Component, AfterViewInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort, Sort, MatSortModule } from '@angular/material/sort';
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
  articulos_displayedColumns: string[] = ['Titulo', 'Citas', 'Autor 1', 'Autor 2', 'Autor 3', 'Año de publicación', 'Enlace'];
  articulos_dataSource = new MatTableDataSource<Articulo>(this.datosBusqueda);

  busquedaAnterior: Busqueda[] = []
  busquedas_displayedColumns: string[] = ['Busqueda', 'Fecha', 'Accion'];
  busquedas_dataSource = new MatTableDataSource<Busqueda>(this.busquedaAnterior);

  panelOpenState = false;

  @ViewChild('paginatorArticulos') paginatorArticulos!: MatPaginator;
  @ViewChild('sortArticulos') sortArticulos!: MatSort;


  

  ngAfterViewInit() {
    this.articulos_dataSource.paginator = this.paginatorArticulos;
    this.articulos_dataSource.sort = this.sortArticulos;

  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.busquedas_dataSource.filter = filterValue.trim().toLowerCase();
  }

  busqueda: string = ""
  idioma: string = ""
  paginas: number = 0
  error!: string 
  cargando: boolean = false;


  almacenarDatos(){
    console.log('Datos guardados:', this.busqueda, this.articulos_dataSource.data);
    this.service.postGuardarBusqueda(this.busqueda, this.articulos_dataSource.data).pipe(
      catchError(err => {
        this.error = 'Ha ocurrido un error al almacenar la busqueda.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      console.log('Búsqueda y artículos guardados correctamente:', response);
      if (this.panelOpenState == true){
        this.cargarBusquedasAnteriores()
      }

    })
  }

  borrarBusqueda(row:any){
      this.service.postBorrarBusqueda(row[0]).pipe(
        catchError(err => {
          this.error = 'Ha ocurrido un error al borrar la busqueda.';
          console.error(err);
          return of(null);
        })
      ).subscribe(response =>{
        console.log('Búsqueda borrada correctamente:', response);
        this.cargarBusquedasAnteriores()
      })
  }

  cargarBusqueda(row:any){
    this.service.getBusquedasArticulos(row[0]).pipe(
      catchError(err => {
        this.error = 'Error al obtener los articulos de la busqueda seleccionada.';
        console.error(err);
        return of(null);
      })
    ).subscribe(response =>{
      this.datosBusqueda = response
      this.error = ''
      this.cargando = false
      this.articulos_dataSource.data = this.datosBusqueda;
      this.busqueda = row[1]
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
      this.busquedas_dataSource.data = this.busquedaAnterior
      console.log(this.busquedas_dataSource)
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
      this.datosBusqueda = response;
      this.error = ''
      // console.log(this.datosBusqueda)
      this.cargando = false
      this.articulos_dataSource.data = this.datosBusqueda;
      // console.log(this.articulos_dataSource.data)
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

export interface Busqueda{
  ID: number;
  Busqueda: string;
  Fecha: string;
}

