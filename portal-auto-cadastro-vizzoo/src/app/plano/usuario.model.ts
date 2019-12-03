import {ErrorStateMatcher} from '@angular/material';
import {FormControl, FormGroupDirective, NgForm} from '@angular/forms';

export class Usuario {
  id: number;
  nome: string;
  telefone: string;
  email: string;
  dt_cadastro: string;
  is_vizzoo: boolean;
  fg_ativo: boolean;
}

export class Franquia {
  id: number;
  qtde_transacao: number;
  valor_fixo: string;
  valor_adicional: string;
  fg_ativo: boolean;
  merchant_plan_id: string;
}

/** Error when the email is invalid */
export class CrossFieldErrorMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    return control.dirty && form.invalid;
  }
}
