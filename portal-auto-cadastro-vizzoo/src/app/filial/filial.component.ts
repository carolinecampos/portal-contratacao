import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Estabelecimento } from '../empresa/contratante.model';
import { MatPaginator, MatTableDataSource } from '@angular/material';
import { ContratoService } from '../shared/contrato.service';
import { MatDialogConfig, MatDialog } from '@angular/material';
import { ShowErrorComponent } from '../shared/modal/show-error/show-error.component';
import { BlackListValidator } from '../shared/validator/blacklist.validator';

@Component({
  selector: 'app-filial',
  templateUrl: './filial.component.html',
  styleUrls: ['./filial.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class FilialComponent implements OnInit {

  filialFormGroup: FormGroup;
  filial: Estabelecimento;
  filiais: Estabelecimento[];
  dataSource: MatTableDataSource<Estabelecimento>;
  columnsMatriz: string[] = ['cnpj', 'nomeEmpresa'];
  displayedColumns: string[] = ['cnpj', 'nomeEmpresa', 'acoes'];
  cnpjEmpresa = '';

  validationMessages = [
    { type: 'required', message: 'Campo obrigatório.' },
    { type: 'maxlength', message: 'Máximo permitido de caracteres.' },
    { type: 'minlength', message: 'Mínimo 3 caracteres.' },
    { type: 'Mask error', message: 'Formato inválido.' },
    { type: 'blackList', message: 'Número de CNPJ inválido ou já cadastrado. Por favor, entre em contato com o suporte da Nexxera.' }
  ];

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;

  constructor(private _formBuilder: FormBuilder, private service: ContratoService, private dialog: MatDialog,
    private blacklistValidator: BlackListValidator) {
    this.createForm();
  }

  createForm() {
    this.filialFormGroup = this._formBuilder.group({
      cnpjFilial: ['', [Validators.required], [this.blacklistValidator.validate]],
      razaoSocial: ['', Validators.compose([
        Validators.required,
        Validators.maxLength(100),
        Validators.minLength(3)
      ])],
    });
  }

  ngOnInit() {
    this.service.currentFiliais.subscribe((data) => {
      this.filiais = data;
      this.dataSource = new MatTableDataSource<Estabelecimento>(this.filiais);
      this.dataSource.paginator = this.paginator;
    });
  }

  adicionarFilial(cnpjFilial: string, razaoSocialFilial: string) {
    if (this.validaSeFilialJaCadastrada(cnpjFilial)) {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.disableClose = true;
      dialogConfig.autoFocus = true;
      dialogConfig.data = 'O CPNJ ' + cnpjFilial + ' já foi cadastrado.';
      dialogConfig.maxWidth = '500px';
      dialogConfig.width = '90%';

      this.dialog.open(ShowErrorComponent, dialogConfig);

    } else {
      this.filial = new Estabelecimento();
      this.filial.cnpj = cnpjFilial;
      this.filial.razaosocial = razaoSocialFilial;
      this.filial.is_matriz = false;
      this.service.adicionarFilial(this.filial);
      this.dataSource = new MatTableDataSource<Estabelecimento>(this.filiais);
      this.dataSource.paginator = this.paginator;
    }
  }

  validaSeFilialJaCadastrada(novoCNPJFilial: string) {
    for (const fil of this.filiais) {
      if (fil.cnpj === novoCNPJFilial) {
        return true;
      }
    }
    return false;
  }

  deleteFilial(_f: Estabelecimento) {
    const index = this.filiais.indexOf(_f);
    this.filiais.splice(index, 1);
    this.dataSource = new MatTableDataSource<Estabelecimento>(this.filiais);
    this.dataSource.paginator = this.paginator;
  }

  proximo() {
    if (this.filiais.length > 0) {
      this.service.contrato.estabelecimento = this.filiais;
    } else {
      const dialogConfig = new MatDialogConfig();
      dialogConfig.disableClose = true;
      dialogConfig.autoFocus = true;
      dialogConfig.data = 'É necessário adicionar pelo menos um estabelecimento.';
      dialogConfig.width = '30%';

      this.dialog.open(ShowErrorComponent, dialogConfig);
    }

  }
}
