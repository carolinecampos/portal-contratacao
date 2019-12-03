import { Component, OnInit, Inject } from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
import { environment } from '../../../../environments/environment';

export const TELA_SUCESSO = 'Obrigado por contratar o Vizzoo!';

@Component({
  selector: 'app-show-success',
  templateUrl: './show-success.component.html',
  styleUrls: ['./show-success.component.scss']
})
export class ShowSuccessComponent implements OnInit {

  titulo: string;
  mensagem: string[];
  url: string;

  constructor(
    public dialogRef?: MatDialogRef<ShowSuccessComponent>,
    @Inject(MAT_DIALOG_DATA) public data?: any) {
      this.titulo = TELA_SUCESSO;
      this.mensagem = data;
      this.url = environment.URL_VIZZO;
  }

  ngOnInit() {

  }

  fechar() {
    this.dialogRef.close();
  }

}
