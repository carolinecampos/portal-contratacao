from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from ..settings import COMMANDER_URL, COMMANDER_USER, COMMANDER_PASS
from ..auditoria.app import Auditoria
import requests

class CommanderServiceImpl:

    def __init__(self):
        self._skyline_url =COMMANDER_URL
        self._auth = None

    def criar_caixa_postal(self, data, cnpj):
        """
        Cria uma caixa postal
        :param data: dicionário com os dados da caixa postal.
        """
        try:
            if not self._auth:
                url_login = COMMANDER_URL + "skyadmin/login"
                data_user = {
                    "username": COMMANDER_USER,
                    "password": COMMANDER_PASS
                }

                with requests.Session() as session:
                    response = session.post(url=url_login, data=data_user)
                    if response.status_code != HTTP_200_OK:
                        Auditoria().salvarErro(cnpj, url_login, data_user, None, str(response.content))
                        raise Exception("Erro ao acessar a caixa postal {}".format(response.content))

                    try:
                        skyline_url = COMMANDER_URL + 'skyadmin/users'
                        ret = session.post(url=skyline_url, data=data)
                        if ret.status_code != HTTP_200_OK:
                            Auditoria().salvarErro(cnpj, skyline_url, data, None, str(ret.content))
                            raise Exception("Erro ao criar caixa postal no Commander {}".format(ret.content))
                        else:
                            print('Cadastro de caixa postal no Commander realizado com sucesso!')

                    except ConnectionError as ccn:
                        raise Exception(error='Erro de conexão com o Commander.'.format(ccn))

        except Exception as err:
            raise Exception("Erro ao criar caixa postal no Commander {}".format(err))
