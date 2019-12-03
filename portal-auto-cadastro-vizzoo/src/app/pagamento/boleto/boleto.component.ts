import { Component, OnInit } from '@angular/core';
import { environment } from '../../../environments/environment';
import { MatDialogConfig, MatDialog } from '@angular/material';
import { ShowSuccessComponent } from '../../shared/modal/show-success/show-success.component';
import { ShowErrorComponent } from '../../shared/modal/show-error/show-error.component';
import { ContratoService } from '../../shared/contrato.service';
import { Pagamento } from '../pagamento.model';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-boleto',
  templateUrl: './boleto.component.html',
  styleUrls: ['./boleto.component.css']
})
export class BoletoComponent implements OnInit {

  pagamento: Pagamento = new Pagamento();
  iconeBoleto = environment.URL_ICON_BOLETO;

  constructor(private dialog: MatDialog, private service: ContratoService, public datepipe: DatePipe) { }

  ngOnInit() {
  }

  concluir() {            
    this.service.contrato.grupo.franquia = this.service.contrato.franquia;
    this.service.contrato.grupo.usuario = this.service.contrato.usuario;
    this.service.contrato.grupo.estabelecimentos = this.service.contrato.estabelecimento;
    this.service.contrato.grupo.adquirentes = this.service.contrato.adquirentes;
    
    //pagamento por boleto
    var dataValidade = new Date();
    dataValidade.setDate(dataValidade.getDate() + 7)
    this.pagamento.dataValidade =  this.datepipe.transform(dataValidade, 'yyyy-MM-dd');;
    this.pagamento.nomeImpresso = this.service.contrato.grupo.razaosocial;
    this.pagamento.cpf = this.service.contrato.grupo.cnpj;
    this.pagamento.tipoPagamento = 2;  

    this.service.contrato.grupo.pagamento = this.pagamento;
    
    this.service.criarBoleto().subscribe(data => {          
      var pagamento = data;      
      this.service.contrato.grupo.pagamento.tokenPagamento = pagamento['tokenPagamento'];
      this.service.contrato.grupo.pagamento.statusPagamento = pagamento['statusPagamento'];
      this.service.abrirPDF(pagamento['tokenPagamento']).subscribe( res => {
          this.downloadArquivo(res, 'boleto.pdf', 'application/pdf');
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
            console.log(mensagem);
            this.mostrarErro(mensagem);        
          });
        });   
    }, error => {
      var mensagem = error['error'];            
      console.log(mensagem);
      this.mostrarErro(mensagem['error']);      
    });  
  }

  mostrarErro(mensagem:string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.data = mensagem;
    dialogConfig.maxWidth = '500px';
    dialogConfig.width = '90%';
    this.dialog.open(ShowErrorComponent, dialogConfig);
  }

  downloadArquivo(content, fileName, contentType) {
    const a = document.createElement('a');
    const file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }


}



