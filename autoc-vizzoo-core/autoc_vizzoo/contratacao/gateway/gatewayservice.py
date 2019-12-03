from ..settings import GATEWAY_URL, GATEWAY_SECRET, GATEWAY_REQUEST_ID
from rest_framework.status import HTTP_200_OK
import requests
import json

class GatewayServiceImpl:

    def __init__(self):
        self._auth = None

    def _get_auth(self):
        try:
            if not self._auth:
                header = {
                    "Content-Type": "application/json; charset=utf-8",
                    "RequestId": GATEWAY_REQUEST_ID,
                    "Authorization": "Bearer " + GATEWAY_SECRET
                }
                return header
        except Exception as err:
            raise Exception("Erro ao montar header do gateway. {}".format(err))

    def autorizar(self, data_json):
        try:
            # header = self._get_auth()
            # url = GATEWAY_URL + '/Orders/CardPayments/Authorize'
            # response = requests.post(url=url, data=data_json, headers=header)
            # if response.status_code != HTTP_200_OK:
            #     print("Não conseguiu acessar o serviço de autorização de cartão de crédito")
            #     raise Exception(response.content)
            # else:
            #     print("cartão autorizado")
            #     resultado = json.loads(response.content.decode())
                return {'payment': {'card': {'cardNumber': '510322******2484', 'cardBrand': 'MasterCard',
                                             'holder': None}, 'transactionType': 1, 'paymentStatus': 2,
                                    'authorization': {'amount': 9990, 'processedDate': '2019-10-02T08:46:08.0115716',
                                                      'proofOfSale': '34571', 'authorizationCode': '2f1d35',
                                                      'returnCode': '0000'}, 'captures': [], 'reversals': [],
                                    'authenticationUrl': None, 'cardToken': 'fb0278f4-fadd-4e37-8559-ad25bb83c3a1',
                                    'installments': 12, 'paymentToken': '4332829a-ce0f-4bf8-bb34-0205677f344e',
                                    'recurrencePlan': {'merchantPlanId': 'ACV9990',
                                                       'name': 'Auto-Contratação Plano 9990',
                                                       'description': 'Plano inicial de 99.90 por mês',
                                                       'interval': 1, 'amount': 9990,
                                                       'created': '2019-06-12T15:28:25.84', 'active': True},
                                    'customer': {'tag': 'Diego Teste Ltda', 'name': 'Diego Teste Ltda',
                                                 'identity': '35421513000150', 'identityType': 'CNPJ',
                                                 'email': 'gipefa@itmailr.com', 'birthdate': None,
                                                 'address': {'country': 'Brasil', 'zipCode': '13225611',
                                                             'number': '10', 'street': 'Rua Ingá', 'complement': '',
                                                             'city': 'Várzea Paulista', 'state': 'SP', 'neighborhood':
                                                                 'Vila Iguaçu'}}, 'amount': 9990},
                        'merchantOrderId': 'ACV999035421513000150'}

        except Exception as err:
            raise Exception("Erro ao autorizar o pagamento via cartão de crédito no Gateway {}".format(err))


    def boleto(self, data_json):
        try:
            header = self._get_auth()
            url = GATEWAY_URL + '/Orders/BoletoPayments/Issue'
            response = requests.post(url=url, data=data_json, headers=header)
            if response.status_code != HTTP_200_OK:
                print("Não conseguiu acessar o serviço de criação do boleto")
                raise Exception(response.content)
            else:
                print("Boleto criado")
                resultado = json.loads(response.content.decode())
                return resultado

        except Exception as err:
            raise Exception("Erro ao autenticar a aplicação no Gateway {}".format(err))

    def imprimirBoletoPDF(self, data_json):
        print("boleto")




