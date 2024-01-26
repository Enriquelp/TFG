import { HttpClient } from "@angular/common/http";
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


    getTest() {
       return 'esta es la respuesta del backend'
    }



}