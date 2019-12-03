import { Usuario, Franquia } from '../plano/usuario.model';
import { Grupo, Estabelecimento } from '../empresa/contratante.model';
import { Pagamento } from '../pagamento/pagamento.model';

export class Contrato {
    usuario : Usuario;
    grupo: Grupo;
    estabelecimento : Estabelecimento[];
    franquia : Franquia;   
    adquirentes: number[];
    pagamento : Pagamento;   
};