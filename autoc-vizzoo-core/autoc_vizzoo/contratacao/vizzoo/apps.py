from datetime import date, datetime
import json
from .vizzoservice import VizzooServiceImpl
from ..utils import Utils
from ..auditoria.app import Auditoria

class CadastroVizzoo:

    def cadastrar_no_vizzoo(self, Grupo, Usuario, lista_estabelecimentos):
        print('inicio do cadastro no vizzo')
        try:
          id_grupo_vizzoo = self.criar_grupo(Grupo)
          Auditoria().confirmarSucessoVizzooGrupo(Grupo.cnpj)

          try:
              for estabelecimento in lista_estabelecimentos:
                  if estabelecimento.cnpj != Grupo.cnpj:
                        self.criar_estabelecimento(estabelecimento, id_grupo_vizzoo, Grupo.cnpj)

              Auditoria().confirmarSucessoVizzooEstabelecimentos(Grupo.cnpj)
          except Exception as err:
            print(err)

          try:
            self.criar_usuario(Usuario, id_grupo_vizzoo, Grupo.cnpj)
            Auditoria().confirmarSucessoVizzooUsuario(Grupo.cnpj)
          except Exception as err:
            print(err)

          print('cadastro no vizzoo realizado com sucesso')
        except Exception as err:
            print(err)

    def criar_grupo(self, Grupo):
        cnpj_so_numeros = Utils().removerCaracteresEspeciaisCNPJ(Grupo.cnpj)
        data_json = {
            'active_flag': 1,
            'cnpj_number': cnpj_so_numeros,
            'creation_date': self.data_hoje(),
            'creation_hour': self.get_horas(),
            'name': Grupo.razaosocial,
            'postal_box': 'VIZZOO.' + cnpj_so_numeros,
            'report_path': 'PADRAO',
            'size_id': 0,
            'template': 'VIZZOO_MAIN_TEMPLATE',
            'use_rules_file_flag': 1
        }
        servico = VizzooServiceImpl()
        id_grupo = servico.post_grupo(json.dumps(data_json), Grupo.cnpj)
        print("cadastrou o grupo: " + Grupo.__str__())
        return id_grupo

    def criar_estabelecimento(self, Estabelecimento, id_grupo_vizzoo, cnpjGrupo):
        cnpj_so_numeros = Utils().removerCaracteresEspeciaisCNPJ(Estabelecimento.cnpj)
        data_json = {
          'active_flag': 1,
          'auto_conc_by_sale_flag': 0,
          'cnpj_number': cnpj_so_numeros,
          'creation_date': self.data_hoje(),
          'creation_hour': self.get_horas(),
          'group_id': id_grupo_vizzoo,
          'inclusion_date': self.data_hoje(),
          'name': Estabelecimento.razaosocial,
          'report_path': 'PADRAO'
        }
        servico = VizzooServiceImpl()
        id_estabelecimento = servico.post_estabelecimento(json.dumps(data_json), cnpjGrupo)
        print("cadastrou o estabelecimento: " + Estabelecimento.__str__())
        return id_estabelecimento

    def criar_usuario(self, Usuario, id_grupo_vizzoo, cnpj):
        data_auth_user = {
            "email": Usuario.email,
            "last_name": Usuario.nome,
            "name": Usuario.nome,
            "username": Usuario.email,
            "group_id": id_grupo_vizzoo
        }
        data_json_user = {
            "email": Usuario.email,
            "enabled": 1,
            "group_id": id_grupo_vizzoo,
            "last_name": Usuario.nome,
            "name": Usuario.nome,
            "role": 1,
            "username": Usuario.email
        }
        servico = VizzooServiceImpl()
        id_usuario_vizzoo = servico.post_usuario_vizzoo(json.dumps(data_json_user), cnpj)
        print("cadastrou o usuário no vizzoo: " + Usuario.__str__())
        servico.post_usuario_keyclock(json.dumps(data_auth_user), cnpj)
        print("cadastrou o usuário no keyclock: " + Usuario.__str__())
        return id_usuario_vizzoo

    def data_hoje(self):
        return date.today().strftime('%Y-%m-%d')

    def get_horas(self):
        return datetime.now().strftime('%H:%M:%S')

