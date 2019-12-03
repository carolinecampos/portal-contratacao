from .commanderservice import CommanderServiceImpl
from ..utils import Utils

class CadastroCommander():

        def montarNomeCaixaPostal(self, cnpj):
            caixaPostal = "ACV" + cnpj + ".ACV" + cnpj
            return caixaPostal

        def cadastrar_no_commander(self, grupo):
            print('inicio do cadastro da caixa postal no commander')
            caixaPostal = "ACV" + grupo.cnpj + ".ACV" + grupo.cnpj
            descricao = "ACV" + grupo.cnpj
            self.cadastrar_caixa_postal(caixaPostal, descricao, grupo.cnpj)

        def cadastrar_caixa_postal(self, caixa_postal, descricao, cnpj):
            data_json = {
                "name": caixa_postal,
                "description": descricao
            }
            servico = CommanderServiceImpl()
            servico.criar_caixa_postal(data_json, cnpj)
            print('Caixa postal cadastrada')
