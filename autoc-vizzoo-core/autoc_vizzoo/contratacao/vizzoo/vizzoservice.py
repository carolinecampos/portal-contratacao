from ..settings import VIZZOO_MANAGER_URL, VIZZOO_URL_GET_TOKEN, VIZZOO_SSO_CLIENT_SECRET
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from ..auditoria.app import Auditoria

import requests
import json

VIZZOO_USERNAME = 'vizzoo@nexxera.com'
VIZZOO_PASSWORD = '@Vizzoo#43210'
VIZZOO_CLIENT_ID = 'vizzoo-cli'

class VizzooServiceImpl:

    def __init__(self):
        self._vizzoo_url = VIZZOO_MANAGER_URL
        self._auth = None

    def _get_auth(self, cnpj):
        """
        Retorna dados para autenticação básica de http
        :return: Objeto  com os dados de acesso.
        """
        try:
            if not self._auth:
                url = VIZZOO_URL_GET_TOKEN
                header = {"Content-Type": "application/x-www-form-urlencoded"}
                data = {
                    "grant_type": "password",
                    "username": VIZZOO_USERNAME,
                    "password": VIZZOO_PASSWORD,
                    "client_id": VIZZOO_CLIENT_ID,
                    "client_secret": VIZZOO_SSO_CLIENT_SECRET
                }
                response = requests.post(url=url, data=data, headers=header)
                if response.status_code != HTTP_200_OK:
                    Auditoria().salvarErro(cnpj, url, data, header, str(response.content))
                    raise Exception("Erro ao autenticar o usuário no Vizzoo. {}".format(response.content.decode()))
                else:
                    resultado = json.loads(response.content.decode())
                    if 'access_token' in resultado:
                        token = resultado['access_token']
                        self._auth = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

            return self._auth
        except Exception as err:
            raise Exception("Erro ao autenticar a aplicação {}".format(err))


    def post_grupo(self, data_json, cnpj):
        """
        Cadastra os dados do grupo no vizzo;
        :return: id_grupo
        """
        try:
            auth = self._get_auth(cnpj)
            url = VIZZOO_MANAGER_URL+"groups"

            response = requests.post(url=url, data=data_json, headers=auth)
            if response.status_code != HTTP_200_OK:
                Auditoria().salvarErro(cnpj, url, data_json, auth, str(response.content))
                raise Exception("Erro ao cadastrar grupo no Vizzoo. {}".format(response.content.decode()))
            else:
                json_ret = json.loads(response.content.decode())
                retorno = json_ret['data']

                if 'id' in retorno:
                    return retorno['id']
                else:
                    raise Exception("ID do Grupo não encontrado")

        except Exception as err:
            raise Exception("Erro ao criar grupo {}".format(err))


    def post_estabelecimento(self, data_json, cnpj):
        """
        Cadastra os dados do estabelecimento no vizzo;
        :return: id de estabelecimento
        """
        try:
            auth = self._get_auth(cnpj)
            url = VIZZOO_MANAGER_URL + "establishments"
            response = requests.post(url=url, data=data_json, headers=auth)

            if response.status_code != HTTP_200_OK:
                Auditoria().salvarErro(cnpj, url, data_json, auth, str(response.content))
                raise Exception("Erro ao cadastrar estabelecimentos no Vizzoo. {}".format(response.content.decode()))
            else:
                json_ret = json.loads(response.content.decode())
                retorno = json_ret['data']

                if "id" in retorno:
                    return retorno['id']
                else:
                    raise Exception("ID do estabelecimento não encontrado")

        except Exception as err:
            raise Exception("Erro ao criar estabelecimento {}".format(err))


    def post_usuario_keyclock(self, data_json, cnpj):
        """
        Cadastra os dados do usuário no keyclock para acessar o vizzoo;
        :return: id do usuário
        """
        try:
            auth = self._get_auth(cnpj)
            url = VIZZOO_MANAGER_URL + "auth/users"

            response = requests.post(url=url, data=data_json, headers=auth)
            if response.status_code != 200:
                Auditoria().salvarErro(cnpj, url, data_json, auth, str(response.content))
                raise Exception("ID do usuário (vizzoo) não encontrado")

        except Exception as err:
            raise Exception("Erro ao criar usuario no keyclock {}".format(err))

    def post_usuario_vizzoo(self, data_json, cnpj):
        """
        Cadastra os dados do usuário no vizzo;
        :return: id do usuário
        """
        try:
            auth = self._get_auth(cnpj)
            url = VIZZOO_MANAGER_URL + "users"

            response = requests.post(url=url, data=data_json, headers=auth)

            if response.status_code != HTTP_200_OK:
                Auditoria().salvarErro(cnpj, url, data_json, auth, str(response.content))
                raise Exception("Erro ao cadastrar usuário no Vizzoo. {}".format(response.content.decode()))
            else:
                json_ret = json.loads(response.content.decode())
                retorno = json_ret['data']

                if "id" in retorno:
                    return retorno['id']
                else:
                    raise Exception("ID do usuário (vizzoo) não encontrado")

        except Exception as err:
            raise Exception("Erro ao criar usuário no vizzoo {}".format(err))

