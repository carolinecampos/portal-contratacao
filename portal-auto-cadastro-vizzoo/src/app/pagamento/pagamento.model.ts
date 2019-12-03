///tipoPagamento: number; 1 - Cartão de Cédito; 2 - Boleto Bancário;
export class Pagamento {    
    numeroCartaoCredito: string;
    codigoSeguranca: string;
    dataValidade: string;
    nomeImpresso: string;
    cpf: string;    
    tipoPagamento: number;
    tokenPagamento : string;
    statusPagamento: number;
  }