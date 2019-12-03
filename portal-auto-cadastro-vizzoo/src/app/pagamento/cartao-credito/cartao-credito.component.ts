import { Component, OnInit, LOCALE_ID } from '@angular/core';
import { FormBuilder, FormGroup, Validators} from '@angular/forms';
import { MomentDateAdapter} from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MatDatepicker} from '@angular/material/datepicker';
import { Moment } from 'moment';
import { ContratoService } from '../../shared/contrato.service';
import { MatDialogConfig, MatDialog } from '@angular/material';
import { ShowSuccessComponent } from '../../shared/modal/show-success/show-success.component';
import { ShowErrorComponent } from '../../shared/modal/show-error/show-error.component';
import { CreditCardValidator } from 'angular-cc-library';
import { Pagamento } from '../pagamento.model';
import { DatePipe } from '@angular/common';

export const MY_FORMATS = {
  parse: {
    dateInput: 'MM/YYYY',
  },
  display: {
    dateInput: 'MM/YYYY',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  },
};

@Component({
  selector: 'app-cartao-credito',
  templateUrl: './cartao-credito.component.html',
  styleUrls: ['./cartao-credito.component.css'],
  providers: [        
    {provide: DateAdapter, useClass: MomentDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: MY_FORMATS},
    {provide: MAT_DATE_LOCALE, useValue: 'pt-BR' },
    {provide: LOCALE_ID, useValue: "pt-BR"},    
  ]
})

export class CartaoCreditoComponent implements OnInit {
  pagamento: Pagamento = new Pagamento();
  cartaoFormGroup: FormGroup; 

  validationMessages = [
    { type: 'required', message: 'Campo obrigatório.' },
    { type: 'Mask error', message: 'Formato inválido.' },     
    { type: 'maxlength', message: 'Máximo 4 caracteres.' },
    { type: 'minlength', message: 'Mínimo 3 caracteres.' }, 
  ];

  constructor(private _formBuilder: FormBuilder, private dialog: MatDialog, public datepipe: DatePipe,
    private service: ContratoService) { 
      this.createForm();
  }

  createForm() {
      this.cartaoFormGroup = this._formBuilder.group({
        numeroCartao: ['', Validators.compose([Validators.required, CreditCardValidator.validateCCNumber])],
        dataValidade: ['', Validators.required],
        codigoSeguranca: ['',   Validators.compose([Validators.required, Validators.maxLength(4), Validators.minLength(3)])],          
        cpf: ['', Validators.required],
        nomeImpresso: ['', Validators.required],
      });
  }

  ngOnInit() {
  }

  escolherAno(normalizedYear: Moment, form: FormGroup) {     
    const ctrlValue =  new Date(form.get('dataValidade').value);
    ctrlValue.setFullYear(normalizedYear.year());
    form.get('dataValidade').setValue(ctrlValue);    
  }

  escolherMes(normalizedMonth: Moment, datepicker: MatDatepicker<Moment>, form: FormGroup) {        
    const ctrlValue =  new Date(form.get('dataValidade').value);
    ctrlValue.setMonth(normalizedMonth.month());  
    form.get('dataValidade').setValue(ctrlValue);
    datepicker.close();            
  }
  
  concluir(form: FormGroup) {  
    //pagamento por cartão
    this.pagamento.numeroCartaoCredito =  form.get('numeroCartao').value;
    this.pagamento.codigoSeguranca =  form.get('codigoSeguranca').value;
    this.pagamento.dataValidade =  this.datepipe.transform(new Date(form.get('dataValidade').value), 'yyyy-MM-dd');;
    this.pagamento.nomeImpresso = form.get('nomeImpresso').value;
    this.pagamento.cpf = form.get('cpf').value;
    this.pagamento.tipoPagamento = 1;  

    this.service.contrato.grupo.franquia = this.service.contrato.franquia;
    this.service.contrato.grupo.usuario = this.service.contrato.usuario;
    this.service.contrato.grupo.estabelecimentos = this.service.contrato.estabelecimento;
    this.service.contrato.grupo.adquirentes = this.service.contrato.adquirentes;
    this.service.contrato.pagamento = this.pagamento;
    this.service.contrato.grupo.pagamento = this.pagamento;    
    
    this.service.validarDadosCartao().subscribe(data => {    
      var pagamento = data            
      this.service.contrato.grupo.pagamento.tokenPagamento = pagamento['tokenPagamento'];
      this.service.contrato.grupo.pagamento.statusPagamento = pagamento['statusPagamento'];
      this.service.postGrupo().subscribe(dados => {        
        const dialogConfig = new MatDialogConfig();
        dialogConfig.disableClose = true;
        dialogConfig.autoFocus = true;
        dialogConfig.data = [
          'Dentro de alguns minutos você receberá um e-mail para confirmar os dados informados.',
          'Ao clicar em OK você será direcionado para a tela de login do Vizzoo.'
        ];
        dialogConfig.maxWidth = '500px';
        dialogConfig.width = '90%';
  
        this.dialog.open(ShowSuccessComponent, dialogConfig);       
      }, error => {     
        var mensagem = "Erro ao tentar salvar os dados do grupo. Por favor, entre em contato com o suporte. E-mail:suporte@nexxera.com";      
        const dialogConfig = new MatDialogConfig();
        dialogConfig.disableClose = true;
        dialogConfig.autoFocus = true;
        dialogConfig.data = mensagem;
        dialogConfig.maxWidth = '500px';
        dialogConfig.width = '90%';
        this.dialog.open(ShowErrorComponent, dialogConfig);
      })
    }, error => {
      var mensagem = error['error'];      
      const dialogConfig = new MatDialogConfig();
      dialogConfig.disableClose = true;
      dialogConfig.autoFocus = true;
      dialogConfig.data = mensagem['error'];
      dialogConfig.maxWidth = '500px';
      dialogConfig.width = '90%';
      this.dialog.open(ShowErrorComponent, dialogConfig);
    });
    
  }

}
