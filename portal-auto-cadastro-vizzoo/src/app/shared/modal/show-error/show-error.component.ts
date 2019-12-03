import { Component, OnInit, Inject } from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

export const TELA_ERRO = 'Atenção';

@Component({
  selector: 'app-show-error',
  templateUrl: './show-error.component.html',
  styleUrls: ['./show-error.component.scss']
})
export class ShowErrorComponent implements OnInit {

  titulo: string;
  mensagem: string;

  constructor(
    public dialogRef?: MatDialogRef<ShowErrorComponent>,
    @Inject(MAT_DIALOG_DATA) public data?: any) {
      this.titulo = TELA_ERRO;
      this.mensagem = data;
  }

  ngOnInit() {
  }

  fechar() {
    this.dialogRef.close();
  }

}
