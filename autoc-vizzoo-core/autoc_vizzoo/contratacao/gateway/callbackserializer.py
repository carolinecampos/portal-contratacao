from rest_framework import serializers
from ..models import PagamentoCartao, Pagamento
import json

class CallBackSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'

    def atualizarStatusPagamento(self, data):
        try:
            pagamento = None
            for d in data:
               pagamento = d

            pag_json = json.loads(pagamento)
            payment = pag_json['payment']
            statusPagamento = payment['paymentStatus']
            tokenPagamento = payment['paymentToken']
            tokenCartao = payment['cardToken']

            PagamentoCartao.objects.filter(tokenPagamento=tokenPagamento, tokenCard=tokenCartao).update(statusPagamento=statusPagamento)
            Pagamento.objects.filter(tokenPagamento=tokenPagamento).update(statusPagamento=statusPagamento)

            mensagem = "O pagamento {} atualizado para o status {}".format(tokenPagamento, statusPagamento)
            print(mensagem)
            return mensagem

        except Exception as err:
            raise Exception("Erro ao atualizar o status do pagamento {}".format(err))




