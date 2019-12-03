import { Component, OnInit, Input } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { Usuario, Franquia, CrossFieldErrorMatcher} from './usuario.model';
import { ContratoService } from '../shared/contrato.service';
import { FranquiasService } from './franquias.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-plano',
  templateUrl: './plano.component.html',
  styleUrls: ['./plano.component.scss']
})
export class PlanoComponent implements OnInit {

  valorTotal = 0;
  usuario = new Usuario();
  franquias: Franquia[];
  franquia = new Franquia();
  planoFormGroup: FormGroup;
  errorMatcher = new CrossFieldErrorMatcher();
  contrato = environment.URL_CONTRATO_PDF;  

  @Input() isMobile: boolean;

  validationMessages = [
    { type: 'required', message: 'Campo obrigatório.' },
    { type: 'maxlength', message: 'Máximo 150 caracteres.' },
    { type: 'Mask error', message: 'Formato inválido.' },
    { type: 'email', message: 'E-mail inválido.' },
    { type: 'NoEmailMatch', message: 'Os e-mails são divergentes.' }
  ];

  constructor(private _formBuilder: FormBuilder, private service: ContratoService, public datepipe: DatePipe,
    private franquiasService: FranquiasService) {
    this.createForm();
  }

  ngOnInit() {
    this.franquiasService.getAllFranquias()
      .subscribe(data => this.franquias = data);
  }

  createForm() {
    this.planoFormGroup = this._formBuilder.group({
      franquia: ['', Validators.required],
      nome: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(150)
      ])],
      telefone: ['', Validators.compose([
        Validators.required
      ])],
      email: ['', Validators.compose([
        Validators.required,
        Validators.email
      ])],
      confirmaEmail: ['', Validators.compose([
        Validators.required,
        Validators.email
      ])],
      autorizacao: ['', Validators.required]
    }, {
      validator: this.validaSeMesmoEmail
    });
  }

  changeSelectFranquia($event) {
    this.franquia.id = $event.target.value;
  }

  validaSeMesmoEmail(control: AbstractControl) {
    const email: string = control.get('email').value;
    const confirmaEmail: string = control.get('confirmaEmail').value;

    if (email !== confirmaEmail) {
      control.get('confirmaEmail').setErrors({ NoEmailMatch: true });
    }
  }

  proximo(form: FormGroup) {
    this.usuario.nome = form.get('nome').value;
    this.usuario.telefone = form.get('telefone').value;
    this.usuario.email = form.get('email').value;
    this.usuario.dt_cadastro = this.datepipe.transform(new Date(), 'yyyy-MM-dd');
    this.usuario.fg_ativo = false;
    this.usuario.is_vizzoo = false;
    this.franquia = form.get('franquia').value;
    this.service.contrato.usuario = this.usuario;
    this.service.contrato.franquia = this.franquia;
  }
}
