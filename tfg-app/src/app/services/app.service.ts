import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, catchError, of } from "rxjs";

@Injectable({
    providedIn: 'root'
})

export class AppService{

    constructor(private http: HttpClient){ }

    urlBuscarOnline: string = 'http://127.0.0.1:5000/api/buscaronline';
    urlBuscarBD: string = 'http://127.0.0.1:5000/api/buscarbd'
    urltest: string ='http://127.0.0.1:5000/api/test'


    getTest(busqueda: string, idioma: string, paginas: number): Observable<any>{
        let params = new HttpParams()
        .set('idioma', idioma)
        .set('busqueda', busqueda)
        .set('paginas', paginas);

       return this.http.get(this.urltest)
    }



}