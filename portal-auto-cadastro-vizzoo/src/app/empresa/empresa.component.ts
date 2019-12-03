import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Grupo, ESTADOS_BRASILEIROS, Estabelecimento, Endereco } from './contratante.model';
import { ContratoService } from '../shared/contrato.service';
import { BlackListValidator } from '../shared/validator/blacklist.validator';
import { CnpjValidator } from '../shared/validator/cnpj.validator';

@Component({
  selector: 'app-empresa',
  templateUrl: './empresa.component.html',
  styleUrls: ['./empresa.component.scss']
})
export class EmpresaComponent implements OnInit {

  grupo = new Grupo;
  matriz = new Estabelecimento;
  estados = ESTADOS_BRASILEIROS;
  empresaFormGroup: FormGroup;

  validationMessages = [
    { type: 'required', message: 'Campo obrigatório.' },
    { type: 'maxlength', message: 'Máximo permitido de caracteres.' },
    { type: 'blackList', message: 'Número de CNPJ inválido ou já cadastrado. Por favor, entre em contato com o suporte da Nexxera.' },
    { type: 'Mask error', message: 'Formato inválido.' },
    { type: 'cnpjValidator', message: 'CNPJ inválido'},
  ];

  constructor(private _formBuilder: FormBuilder, private service: ContratoService, private blacklistValidator: BlackListValidator,
    private cnpjValidator: CnpjValidator) {
    this.createForm();
  }

  ngOnInit() {
  }

  createForm() {
    this.empresaFormGroup = this._formBuilder.group({
      razaosocial: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(200)
      ])],
      cnpj: ['', Validators.compose([Validators.required, this.cnpjValidator.validate]), [this.blacklistValidator.validate]],
      nome_fantasia: ['', Validators.maxLength(20)],
      inscricao_estadual: ['', Validators.maxLength(30)],
      cep: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(20)
      ])],
      endereco: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(200)
      ])],
      bairro: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(100)
      ])],
      cidade: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(100)
      ])],
      uf: ['', Validators.required],
      numero: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(8)
      ])],
      complemento: ['', Validators.maxLength(50)],
    });
  }

  changeSelectUF($event) {
    this.grupo.uf = $event.target.value;
  }

  changeSelectEndereco($event, form: FormGroup) {
    this.grupo.cep = $event.target.value;
    let cep: string = this.grupo.cep.toString();
    cep = cep.replace('.', '').replace('-', '');
    let end: Endereco = new Endereco();
    this.service.buscarCEP(cep).subscribe(data => {
      end = data;
      form.get('endereco').setValue(end.address);
      form.get('bairro').setValue(end.neighborhood);
      form.get('cidade').setValue(end.city);
      form.get('uf').setValue(end.state);
    });
  }

  proximo(form: FormGroup) {
    this.grupo.razaosocial = form.get('razaosocial').value;
    this.grupo.cnpj = form.get('cnpj').value;
    this.grupo.nome_fantasia = form.get('nome_fantasia').value;
    this.grupo.inscricao_estadual = form.get('inscricao_estadual').value;
    this.grupo.endereco = form.get('endereco').value;
    this.grupo.bairro = form.get('bairro').value;
    this.grupo.cidade = form.get('cidade').value;
    this.grupo.uf = form.get('uf').value;
    this.grupo.cep = form.get('cep').value;
    this.grupo.numero = form.get('numero').value;
    this.grupo.complemento = form.get('complemento').value;

    this.service.contrato.grupo = this.grupo;
    this.matriz.cnpj = this.grupo.cnpj;
    this.matriz.razaosocial = this.grupo.razaosocial;
    this.matriz.is_matriz = true;
    this.service.adicionarFilial(this.matriz);
  }

}
