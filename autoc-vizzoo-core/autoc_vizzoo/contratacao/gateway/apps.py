from .gatewayservice import GatewayServiceImpl
from ..utils import Utils
from ..models import Franquia
from ..settings import AUTOCONTRATACAO_URL
from datetime import date

import json


class Gateway:

    def autenticarCartaoDeCredito(self, pagamento_date, validated_data, usuario_data):
        numeroCartao = pagamento_date['numeroCartaoCredito']
        numeroCartao = numeroCartao.replace(" ", "")
        codigoSeguranca = pagamento_date['codigoSeguranca']
        dataValidade = pagamento_date['dataValidade']
        ano = dataValidade[0:4]
        mes = dataValidade[5:7]

        nomeImpresso = pagamento_date['nomeImpresso']
        cpf = pagamento_date['cpf']

        razaoSocial = validated_data['razaosocial']
        cnpj = validated_data['cnpj']
        nome_fantasia = validated_data['nome_fantasia']
        endereco = validated_data['endereco']
        numero = validated_data['numero']
        bairro = validated_data['bairro']
        cidade = validated_data['cidade']
        cep = validated_data['cep']
        uf = validated_data['uf']
        email = usuario_data['email']
        idFranquia = int(validated_data['franquia'])
        arrayFranquia = Franquia.objects.filter(pk=idFranquia)
        valorFranquia = 0
        for franquia in arrayFranquia:
            valorFranquia = Utils().convertNumberToStringSemVirgula(franquia.valor_fixo)

        data_json = {
            "installments": 12,
            "capture": True,
            "returnUrl": AUTOCONTRATACAO_URL,
            "transactionType": "1",
            "card": {
                "number": numeroCartao,
                "securityCode": codigoSeguranca,
                "expirationDate": {
                    "year": ano,
                    "month": mes
                },
                "holder": {
                    "name": nomeImpresso,
                    "socialNumber": cpf
                },
                "saveCard": True
            },
            "enableAntifraud": False,
            "merchantOrderId": self.montarNumeroPedido(valorFranquia, cnpj),
            "customer": {
                "tag": nome_fantasia,
                "name": razaoSocial,
                "identity": cnpj,
                "identityType": "CNPJ",
                "email": email,
                "address": {
                      "country": "Brasil",
                      "zipCode": cep,
                      "number": numero,
                      "street": endereco,
                      "city": cidade,
                      "state": uf,
                      "neighborhood": bairro
                }
            },
            "amount": valorFranquia,
            "recurrence": {
                "merchantPlanId": "ACV" + valorFranquia
            },
            "callbackUrl": AUTOCONTRATACAO_URL + "/callbackCartaoCredito"
        }

        service = GatewayServiceImpl()
        return service.autorizar(json.dumps(data_json))


    def montarNumeroPedido(self, valorPlano, cnpj):
        return "ACV" + valorPlano + cnpj

    def cadastrarNovoBoleto(self, validated_data, usuario_data):
        razaoSocial = validated_data['razaosocial']
        cnpj = validated_data['cnpj']
        nome_fantasia = validated_data['nome_fantasia']
        endereco = validated_data['endereco']
        numero = validated_data['numero']
        bairro = validated_data['bairro']
        cidade = validated_data['cidade']
        cep = validated_data['cep']
        uf = validated_data['uf']
        email = usuario_data['email']

        idFranquia = int(validated_data['franquia'])
        arrayFranquia = Franquia.objects.filter(pk=idFranquia)
        valorFranquia = 0
        for franquia in arrayFranquia:
            valorFranquia = Utils().convertNumberToStringSemVirgula(franquia.valor_fixo)

        hoje = date.today()
        dataExpiracao = date.fromordinal(hoje.toordinal()+7)

        data_json = {
          "expirationDate": str(dataExpiracao),
          "demonstrative": ["Boleto"],
          "instructions": ["Não receber após vencimento."],
          "merchantOrderId": self.montarNumeroPedido(valorFranquia, cnpj),
          "customer": {
            "tag": nome_fantasia,
            "name": razaoSocial,
            "identity": cnpj,
            "identityType": "CNPJ",
            "email": email,
            "birthdate": str(hoje),
            "address": {
              "country": "Brasil",
              "zipCode": cep,
              "number": numero,
              "street": endereco,
              "city": cidade,
              "state": uf,
              "neighborhood": bairro
            }
          },
          "amount": valorFranquia
        }

        service = GatewayServiceImpl()
        return service.boleto(json.dumps(data_json))


