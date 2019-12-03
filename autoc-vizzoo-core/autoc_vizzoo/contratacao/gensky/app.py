from .genskyservice import GenSkyServiceImpl
from ..utils import Utils
import json

class CadastroGenSky():

    _dsNamesArquivos_ = []

    def __init__(self):
        self._auth = None
        self._dsNamesArquivos_ = []

    def cadastrar(self, idCaixaPostal, cnpj, mascaras):
        print("cadastro de mascaras")
        cnpjCompleto = Utils().adicionarCaracteresEspeciaisCNPJ(cnpj)
        dsNamesArquivos = []
        for mascara in mascaras:
            dsname = self.montarEnvioEmail(cnpj, idCaixaPostal, mascara)
            dsNamesArquivos.append(dsname)
            if mascara.id_caixa_postal == 0 or mascara.id_caixa_postal is None:
                mascara.id_caixa_postal = idCaixaPostal
            self.criar_mascaras(cnpj, mascara, idCaixaPostal, cnpjCompleto)

        print(dsNamesArquivos)
        return dsNamesArquivos


    def criar_caixa_postal(self, caixaPostal, cnpj):
        print("inicio do cadastro no GenSky")
        """
        Cria uma caixa postal
        :param data: dicionário com os dados da caixa postal.
        """
        data_json = {
            "name": caixaPostal,
            "required_layout_and_product": False
        }
        servico = GenSkyServiceImpl()
        return servico.criar_caixa_postal(json.dumps(data_json), cnpj)

    def criar_mascaras(self, cnpjSoNumeros, mascara, idCaixaPostal, cnpjOriginal):
        """
        Cria as mascaras.
        :param data: dicionário com os dados das mascaras dns.
        """
        data_json = {
            "postalbox": mascara.id_caixa_postal,
            "station": mascara.id_estacao,
            "timeout": mascara.nu_timeout,
            "send_begining_time": mascara.horas_iniciais,
            "send_ending_time": mascara.horas_finais,
            "send_entrance_mask": mascara.mask_cliente_entrada,
            "send_exit_mask": mascara.mask_cliente_saida,
            "return_entrance_mask": mascara.getMascaraBancoEntrada(cnpjSoNumeros),
            "return_exit_mask": mascara.getMascaraBancoSaida(cnpjSoNumeros, idCaixaPostal),
            "send_post_validation_script": mascara.script_validacao_cliente,
            "send_post_transmition_script": mascara.script_transmissao_banco,
            "return_post_transmition_script": mascara.script_recepcao_banco,
            "description": mascara.observacao,
            "reset_send_counter_daily": mascara.reset_cont_diario_cliente_rvs,
            "inherit_costumer_counter": mascara.herdar_cont_diario_cliente_rvs,
            "send_counter": mascara.contador_diario_cliente_rvs,
            "reset_return_counter_daily": mascara.reset_cont_diario_rvs_cliente,
            "inherit_bank_counter": mascara.herdar_cont_diario_rvs_cliente,
            "return_counter": mascara.contador_diario_rvs_cliente,
            "verify_duplicity": mascara.verificar_duplicidade_rvs_cliente,
            "send_option": mascara.opcoes_envio_arquivo,
            "connect_send_script": mascara.script_envio,
            "layout_name": "250",
            "product_name": "AutoContratação Vizzoo"
        }

        servico = GenSkyServiceImpl()
        servico.criar_mascara(json.dumps(data_json), cnpjOriginal)

    def montarEnvioEmail(self, cnpj, idCaixaPostal, mascara):
        return mascara.getMascaraEnvioEmail(cnpj, idCaixaPostal)

    def buscar_caixa_postal(self, caixaPostal, cnpj):
        servico = GenSkyServiceImpl()
        idCaixaPostal = servico.buscar_caixa_postal(caixaPostal, cnpj)
        return idCaixaPostal
