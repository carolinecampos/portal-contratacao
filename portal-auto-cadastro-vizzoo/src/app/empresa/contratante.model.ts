import { Usuario, Franquia } from '../plano/usuario.model';
import { Pagamento } from '../pagamento/pagamento.model';

export interface Estado {
  sigla: string;
  nomeCompleto: string;
}

export const ESTADOS_BRASILEIROS: Estado [] = [
  {sigla: 'AC', nomeCompleto: 'Acre'},
  {sigla: 'AL', nomeCompleto: 'Alagoas'},
  {sigla: 'AP', nomeCompleto: 'Amapá'},
  {sigla: 'AM', nomeCompleto: 'Amazonas'},
  {sigla: 'BA', nomeCompleto: 'Bahia'},
  {sigla: 'CE', nomeCompleto: 'Ceará'},
  {sigla: 'DF', nomeCompleto: 'Distrito Federal'},
  {sigla: 'ES', nomeCompleto: 'Espírito Santo'},
  {sigla: 'GO', nomeCompleto: 'Goiás'},
  {sigla: 'MA', nomeCompleto: 'Maranhão'},
  {sigla: 'MT', nomeCompleto: 'Mato Grosso'},
  {sigla: 'MS', nomeCompleto: 'Mato Grosso do Sul'},
  {sigla: 'MG', nomeCompleto: 'Minas Gerais'},
  {sigla: 'PA', nomeCompleto: 'Pará'},
  {sigla: 'PB', nomeCompleto: 'Paraíba'},
  {sigla: 'PR', nomeCompleto: 'Paraná'},
  {sigla: 'PE', nomeCompleto: 'Pernambuco'},
  {sigla: 'PI', nomeCompleto: 'Piauí'},
  {sigla: 'RJ', nomeCompleto: 'Rio de Janeiro'},
  {sigla: 'RN', nomeCompleto: 'Rio Grande do Norte'},
  {sigla: 'RS', nomeCompleto: 'Rio Grande do Sul'},
  {sigla: 'RO', nomeCompleto: 'Rondônia'},
  {sigla: 'RR', nomeCompleto: 'Roraima'},
  {sigla: 'SC', nomeCompleto: 'Santa Catarina'},
  {sigla: 'SP', nomeCompleto: 'São Paulo'},
  {sigla: 'SE', nomeCompleto: 'Sergipe'},
  {sigla: 'TO', nomeCompleto: 'Tocantins'}
];

export class Blacklist {
  id: number;
  razaosocial: string;
  cnpj: string;
  is_ativo: boolean;
}

export class Estabelecimento {
  id: number;
  cnpj: string;
  razaosocial: string;
  is_matriz: boolean;
}

export class Grupo {
  id: number;
  cnpj: string;
  razaosocial: string;
  nome_fantasia: string;
  inscricao_estadual: number;
  endereco: String;
  numero: string;
  complemento:string;
  bairro: string;
  cidade: string;
  uf: string;
  cep: number;
  usuario: Usuario;
  adquirentes: number[];
  estabelecimentos: Estabelecimento[];
  franquia: Franquia;
  pagamento: Pagamento;  
}

export class Endereco {
  address_description: string;
  address: string;  
  postal_code: string; 
  neighborhood: string;
  city: string;
  state: string;
}
