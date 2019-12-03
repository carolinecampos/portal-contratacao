import { Estabelecimento, Blacklist, Endereco } from './../empresa/contratante.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

import { Contrato } from './contrato.model';
import { environment } from  '../../environments/environment';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
    'Authorization': 'Basic ' + btoa(environment.API_LOGIN+':'+environment.API_PASSWORD)
  })
};

@Injectable()
export class ContratoService {

  contrato: Contrato = new Contrato();
  filiais: Estabelecimento[] = [];

  private filiaisSource = new BehaviorSubject<Estabelecimento[]>(this.filiais);
  currentFiliais = this.filiaisSource.asObservable();

  constructor(private http: HttpClient) { }

  postGrupo() {
    var grupo = {
      ...this.contrato.grupo
    };    
    return this.http.post(environment.URL_API+'/grupos/', grupo, httpOptions)
  }

  validarDadosCartao() {
    var grupo = {
      ...this.contrato.grupo
    };  
    return this.http.post(environment.URL_API+"/autenticarCartaoCredito/", grupo, httpOptions);
  }

  criarBoleto() {
    var grupo = {
      ...this.contrato.grupo
    };  
    return this.http.post(environment.URL_API+"/criarBoleto/", grupo, httpOptions);
  }

  adicionarFilial(filial: Estabelecimento) {
    this.filiais.push(filial);
    this.filiaisSource.next(this.filiais);
  }

  validarCNPJJaCadastrado(cnpj:string)  { 
    return this.http.get<Blacklist>(environment.URL_API+'/blacklist/?cnpj='+cnpj);    
  }
  
  buscarCEP(cep:string){
    return this.http.get<Endereco>(environment.CEP_URL_API+cep);        
  }

  abrirPDF(tokenPagamento:string) {
    var url = environment.URL_GERAR_BOLETO + tokenPagamento + '/PDF';        
    return this.http.get(url, { responseType: 'blob' });
  }


}
