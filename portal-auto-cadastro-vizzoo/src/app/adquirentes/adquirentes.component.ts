import { Component, OnInit } from '@angular/core';
import { ContratoService } from '../shared/contrato.service';
import { MatDialog } from '@angular/material';
import { AdquirentesService } from './adquirentes.service';
import { Adquirente } from './adquirente.model';

@Component({
  selector: 'app-adquirentes',
  templateUrl: './adquirentes.component.html',
  styleUrls: ['./adquirentes.component.scss']
})
export class AdquirentesComponent implements OnInit {

  todasAdquirentes: Adquirente[];
  adquirentesSelecionadas: number[] = [];
  index = 0;
  naoEscolheuAdq: boolean = true;

  constructor(private service: ContratoService,
    private dialog: MatDialog,
    private adquirentesService: AdquirentesService) {
  }

  ngOnInit() {
    this.adquirentesService.getAllAdquirentes()
      .subscribe(data => this.todasAdquirentes = data);
  }

  onChange(adq) {
    adq.checked = !adq.checked;

    if (adq.checked) {
      this.adquirentesSelecionadas.push(adq.id);
    } else {
      const index = this.adquirentesSelecionadas.indexOf(adq.id, 0);
      this.adquirentesSelecionadas.splice(index, 1);
    }
    if (this.adquirentesSelecionadas.length >= 1) {
      this.naoEscolheuAdq = false;
    } else {
      this.naoEscolheuAdq = true;
    }
  }

  proximo() {    
    this.service.contrato.adquirentes = this.adquirentesSelecionadas;
  }

}
