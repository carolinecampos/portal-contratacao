from rest_framework.status import HTTP_200_OK
from ..settings import NOTIFIER_SENDER
from ..auditoria.app import Auditoria
import requests

class NotifierSenderImpl:

    def post_message(self, data_json, cnpj):
        """
        Envia mensagem por email;
        """
        header = {"Content-Type": "application/json"}
        response = requests.post(url=NOTIFIER_SENDER, data=data_json, headers=header)

        if response.status_code != HTTP_200_OK:
            Auditoria().salvarErro(cnpj, NOTIFIER_SENDER, data_json, header, str(response.content))
            raise Exception("Erro ao enviar email. {}".format(response.content.decode()))
        else:
            print('email de confirmação enviado com sucesso!')

