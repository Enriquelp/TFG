import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, catchError, of } from "rxjs";
import { Articulo } from "../busqueda/busqueda.component";

@Injectable({
    providedIn: 'root'
})

export class AppService{

    constructor(private http: HttpClient){ }

    urlBuscarOnline: string = 'http://127.0.0.1:5000/api/buscar-online';
    urlBuscarBD: string = 'http://127.0.0.1:5000/api/busquedas-anteriores'
    urlBusquedaArticulos: string = 'http://127.0.0.1:5000/api/busqueda-bd'
    urlAlmacenarBusqueda: string = 'http://127.0.0.1:5000/api/almacenarBusqueda'
    urlDescargar: string = 'http://127.0.0.1:5000/api/descargarCSV'
    urlBorrarBusqueda: string = 'http://127.0.0.1:5000/api/borrarBusqueda'
    urltest: string ='http://127.0.0.1:5000/api/test'
    

    getBusquedaOnline(busqueda: string, idioma: string, paginas: number): Observable<any>{
        let params = new HttpParams()
        .set('idioma', idioma)
        .set('busqueda', busqueda)
        .set('paginas', paginas);
       return this.http.get(this.urlBuscarOnline, {params})
    }

    getBusquedasAnteriores(): Observable<any>{
        let params = new HttpParams()
       return this.http.get(this.urlBuscarBD, {params})
    }

    getBusquedasArticulos(id:number): Observable<any>{
        let params = new HttpParams()
        .set('idBusqueda', id);
       return this.http.get(this.urlBusquedaArticulos, {params})
    }

    postGuardarBusqueda(busqueda: string, articulos: Articulo[]): Observable<any>{
       return this.http.post(this.urlAlmacenarBusqueda, {busqueda, articulos})
    }

    postBorrarBusqueda(id:number){
        return this.http.post(this.urlBorrarBusqueda, {id})
    }

    getTest(busqueda: string, idioma: string, paginas: number): Observable<any>{
        let params = new HttpParams()
        .set('idioma', idioma)
        .set('busqueda', busqueda)
        .set('paginas', paginas);
       return this.http.get(this.urltest, {params})
    }




}