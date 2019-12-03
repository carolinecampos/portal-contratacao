import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AdquirentesComponent } from './adquirentes/adquirentes.component';
import { EmpresaComponent } from './empresa/empresa.component';
import { PlanoComponent } from './plano/plano.component';
import { ContratoService } from './shared/contrato.service';
import { FilialComponent } from './filial/filial.component';
import { ShowErrorComponent } from './shared/modal/show-error/show-error.component';
import { ShowSuccessComponent } from './shared/modal/show-success/show-success.component';
import { AdquirentesService } from './adquirentes/adquirentes.service';
import { FranquiasService } from './plano/franquias.service';
import { BlackListValidator } from './shared/validator/blacklist.validator';
import { CnpjValidator } from './shared/validator/cnpj.validator';
import { CartaoCreditoComponent } from './pagamento/cartao-credito/cartao-credito.component';
import { BoletoComponent } from './pagamento/boleto/boleto.component';
import { LoaderService } from './shared/loader/loader.service';

// plugins
import { NgxMaskModule } from 'ngx-mask';
import { PagamentoComponent } from './pagamento/pagamento.component';
import { CreditCardDirectivesModule } from 'angular-cc-library';
import { LoaderComponent } from './shared/loader/loader.component';
import { LoaderInterceptor } from './loader.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    AdquirentesComponent,
    EmpresaComponent,
    PlanoComponent,
    FilialComponent,
    ShowErrorComponent,
    ShowSuccessComponent,
    PagamentoComponent,
    CartaoCreditoComponent,
    BoletoComponent,
    LoaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FlexLayoutModule,
    NgxMaskModule.forRoot(),  
    CreditCardDirectivesModule,
  ],
  providers: [ContratoService, AdquirentesService, FranquiasService, DatePipe, BlackListValidator, CnpjValidator, LoaderService, 
    {provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true}],
  bootstrap: [AppComponent],
  entryComponents: [ShowErrorComponent, ShowSuccessComponent]
})
export class AppModule { }
