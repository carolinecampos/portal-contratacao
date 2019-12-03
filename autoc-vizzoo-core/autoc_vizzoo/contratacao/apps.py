from django.apps import AppConfig
from .models import PagamentoCartao, PagamentoBoleto
from .gateway.apps import Gateway

from datetime import datetime

class ContratacaoConfig(AppConfig):
    name = 'contratacao'


class AutoContratar:

    def autenticarCartaoDeCredito(self, pagamento_date, validated_data, usuario_data):
        servicoGategay = Gateway()
        resultado = servicoGategay.autenticarCartaoDeCredito(pagamento_date, validated_data, usuario_data)
        dadosTransacao = resultado['payment']
        urlRetorno = str(resultado)
        urlRetorno = urlRetorno[0:2000]
        cartao = dadosTransacao['card']
        numeroCartao = cartao['cardNumber']
        bandeira = cartao['cardBrand']

        autorizacao = dadosTransacao['authorization']
        codigoAutorizacao = autorizacao['authorizationCode']
        retornoCodigoAutorizacao = autorizacao['returnCode']

        statusPagamento = dadosTransacao['paymentStatus']
        tokenCartao = dadosTransacao['cardToken']
        tokenPagamento = dadosTransacao['paymentToken']

        cliente = dadosTransacao['customer']
        idClienteGateway = cliente['identity']

        codigoSeguranca = pagamento_date['codigoSeguranca']
        dataValidade = pagamento_date['dataValidade']
        nomeImpresso = pagamento_date['nomeImpresso']
        cpf = pagamento_date['cpf']

        if statusPagamento == 9:
            raise Exception("Pagamento não autorizado!")
        else:
            return PagamentoCartao.objects.create(tokenCard=tokenCartao, tokenPagamento=tokenPagamento,
                                                  statusPagamento=statusPagamento, codigoAutorizacao=codigoAutorizacao,
                                                  retornoCodigoAutorizacao=retornoCodigoAutorizacao, bandeira=bandeira,
                                                  urlRetorno=urlRetorno, idCliente=idClienteGateway, numeroCartaoCredito=numeroCartao,
                                                  codigoSeguranca=codigoSeguranca, dataValidade=dataValidade,
                                                  nomeImpresso=nomeImpresso, cpf=cpf)

    def criarBoletoBancario(self, validated_data, usuario_data):
        servicoGategay = Gateway()
        resultado = servicoGategay.cadastrarNovoBoleto(validated_data, usuario_data)
        urlRetorno = str(resultado)
        urlRetorno = urlRetorno[0:2000]
        dadosBoleto = resultado['payment']
        boleto = dadosBoleto['boleto']
        numeroBoleto = boleto['boletoNumber']
        linhaDigitavel = boleto['digitableLine']
        dataExpiracaoStr = boleto['expirationDate']
        dataExpiracao = datetime.strptime(dataExpiracaoStr, '%Y-%m-%dT%H:%M:%S')
        statusPagamento = dadosBoleto['paymentStatus']
        tokenPagamento = dadosBoleto['paymentToken']

        return PagamentoBoleto.objects.create(tokenPagamento=tokenPagamento, statusPagamento=statusPagamento,
                                              numeroBoleto=numeroBoleto, linhaDigitavel=linhaDigitavel,
                                              urlRetorno=urlRetorno, dataExpiracao=dataExpiracao.date())
