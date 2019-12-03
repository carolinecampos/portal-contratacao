import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Adquirente } from './adquirente.model';
import { environment } from '../../environments/environment';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
    'Authorization': 'Basic ' + btoa(environment.API_LOGIN + ':' + environment.API_PASSWORD)
  })
};

@Injectable()
export class AdquirentesService {

  constructor(private http: HttpClient) {}

  getAllAdquirentes(): Observable<Adquirente[]> {
    return this.http.get<Adquirente[]>(environment.URL_API + '/adquirentes/', httpOptions);
  }
}
