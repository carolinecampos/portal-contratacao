import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Franquia } from './usuario.model';
import { environment } from '../../environments/environment';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
    Authorization:
      'Basic ' + btoa(environment.API_LOGIN + ':' + environment.API_PASSWORD)
  })
};

@Injectable()
export class FranquiasService {
  constructor(private http: HttpClient) {}

  getAllFranquias(): Observable<Franquia[]> {
    return this.http.get<Franquia[]>(
      environment.URL_API + '/franquias/',
      httpOptions
    );
  }
}
