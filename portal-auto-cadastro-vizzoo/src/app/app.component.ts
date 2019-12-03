import { Component, OnInit, ViewChild } from '@angular/core';
import { environment } from '../environments/environment';
import { PlanoComponent } from './plano/plano.component';
import { EmpresaComponent } from './empresa/empresa.component';
import { FilialComponent } from './filial/filial.component';
import { BreakpointObserver } from '@angular/cdk/layout';
import { AdquirentesComponent } from './adquirentes/adquirentes.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  logo = environment.URL_LOGO;
  isMobile: boolean;

  @ViewChild(PlanoComponent, { static: true }) stepPlano: PlanoComponent;
  @ViewChild(EmpresaComponent, { static: true }) stepEmpresa: EmpresaComponent;
  @ViewChild(FilialComponent, { static: true }) stepFilial: FilialComponent;
  @ViewChild(AdquirentesComponent, { static: true }) stepAdquirentes: AdquirentesComponent;

  constructor(breakpointObserver: BreakpointObserver) {
    breakpointObserver.observe('(max-width: 599px)')
      .subscribe(breakpoint => {
        this.isMobile = breakpoint.matches;
      });
  }

  ngOnInit() {
  }
}
