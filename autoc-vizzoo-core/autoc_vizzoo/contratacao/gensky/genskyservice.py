from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from ..settings import GENSKY_URL, GENSKY_USER, GENSKY_PASS
from ..auditoria.app import Auditoria
import requests
import json

class GenSkyServiceImpl:

    def __init__(self):
        self._skyline_url =GENSKY_URL
        self._auth = None

    def _get_auth(self, cnpj):
        """
        Retorna dados para autenticação básica de http
        :return: chave para o acesso.
        """
        try:
            if not self._auth:
                url = GENSKY_URL + 'rest-auth/login/'
                header = {"Content-Type": "application/x-www-form-urlencoded"}
                data = {
                    "username": GENSKY_USER,
                    "password": GENSKY_PASS,
                }
                response = requests.post(url=url, data=data, headers=header)

                if response.status_code != HTTP_200_OK:
                    Auditoria().salvarErro(cnpj, url, data, header, str(response.content))
                else:
                    resultado = json.loads(response.content.decode())
                    if 'key' in resultado:
                        token = resultado['key']
                        self._auth = {'Content-Type': 'application/json', 'Authorization': 'Token ' + token}

            return self._auth
        except Exception as err:
            raise Exception("Erro ao autenticar a aplicação {}".format(err))

    def criar_caixa_postal(self, data_json, cnpj):
        """
        Cria uma caixa postal
        :param data: dicionário com os dados da caixa postal.
        """
        try:
            auth = self._get_auth(cnpj)
            url_login = GENSKY_URL + "postalbox/"
            response = requests.post(url=url_login, data=data_json, headers=auth)

            if response.status_code != HTTP_201_CREATED:
                Auditoria().salvarErro(cnpj, url_login, data_json, auth, str(response.content))
                raise Exception("Erro ao cadastrar caixa postal no GenSky. {}".format(response.content.decode()))
            else:
                json_ret = response.json()
                if 'id' in json_ret:
                    print('Cadastro de caixa postal no Gensky realizado com sucesso!')
                    idCaixaPostal = json_ret['id']
                    return idCaixaPostal

        except Exception as err:
            raise Exception("Erro ao criar caixa postal no GenSky. {}".format(err))

    def criar_mascara(self, data_json, cnpj):
        """
        Cria uma mascara
        :param data: dicionário com os dados da mascara.
        """
        try:
            auth = self._get_auth(cnpj)
            url = GENSKY_URL + "mask/"
            response = requests.post(url=url, data=data_json, headers=auth)

            if response.status_code != HTTP_201_CREATED:
                Auditoria().salvarErro(cnpj, url, data_json, auth, str(response.content))
                raise Exception("Erro ao cadastrar máscara no GenSky. {}".format(response.content.decode()))
            else:
                if 'id' in response:
                    print('Cadastro de máscara no Gensky realizado com sucesso!')
                    idMascara = response['id']
                    return idMascara

        except Exception as err:
            raise Exception("Erro ao criar máscara no Gensky {}".format(err))


    def buscar_caixa_postal(self, caixaPostal, cnpj):
        """
        Buscar uma caixa postal
        :param data: dicionário com os dados da caixa postal.
        """
        try:
            auth = self._get_auth(cnpj)
            url_login = GENSKY_URL + "postalbox/"
            params = {'pb_name': caixaPostal}
            response = requests.get(url=url_login, params=params, headers=auth)

            if response.status_code != HTTP_200_OK:
                Auditoria().salvarErro(cnpj, url_login, params, auth, str(response.content))
                raise Exception("Erro ao buscar caixa postal no GenSky. {}".format(response.content.decode()))
            else:
                json_ret = response.json()
                if 'results' in json_ret:
                    resultado = json_ret['results']
                    data = resultado[0]
                    idCaixaPostal = data['id']
                    return idCaixaPostal

        except Exception as err:
            raise Exception("Erro ao buscar caixa postal no GenSky. {}".format(err))
