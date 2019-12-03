from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.http import HttpResponse
from .settings import VIZZO_URL
from .commander.serializer import CommanderSerializer
from .models import Estabelecimento, Grupo, Usuario, AutoImplantar, Franquia, BlackList_Estabelecimento, PagamentoCartao, PagamentoBoleto, Adquirente, GrupoAdquirente, TemplateEmail
from .serializers import AdquirenteSerializer, EstabelecimentoSerializer, GrupoSerializer, UsuarioSerializer, AutoContratarSerializer, FranquiaSerializer, BlackListEstabelecimentoSerializer, PagamentoCartaoSerializer, PagamentoBoletoSerializer, GrupoAdquirenteSerializer, TemplateEmailSerializer
from .gensky.serializer import GenskySerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .gateway.callbackserializer import CallBackSerializer


class AdquirenteViewSet(viewsets.ModelViewSet):
    serializer_class = AdquirenteSerializer
    queryset = AdquirenteSerializer().buscarAtivas()

class FranquiaViewSet(viewsets.ModelViewSet):
    serializer_class = FranquiaSerializer
    queryset = Franquia.objects.all()

    def get_queryset(self):
        return FranquiaSerializer().buscarAtivas()

class EstabelecimentoViewSet(viewsets.ModelViewSet):
    serializer_class = EstabelecimentoSerializer
    queryset = Estabelecimento.objects.all()

class BlackListEstabelecimentoViewSet(viewsets.ModelViewSet):
    serializer_class = BlackListEstabelecimentoSerializer
    queryset = BlackList_Estabelecimento.objects.all()

    def get_queryset(self):
        cnpj = self.request.query_params.get('cnpj')
        if cnpj is None:
            return BlackList_Estabelecimento.objects.all()
        else:
            return BlackListEstabelecimentoSerializer().buscarPorCnpj(cnpj)

class GrupoAdquirenteViewSet(viewsets.ModelViewSet):
    serializer_class = AdquirenteSerializer
    queryset = Adquirente.objects.all()

    def get_queryset(self):
        cnpj = self.request.query_params.get('cnpj')
        if cnpj is None:
            return GrupoAdquirente.objects.all()
        else:
            gruposAdq = GrupoAdquirenteSerializer().buscarPorCnpj(cnpj)
            adquirentes = []
            for gradq in gruposAdq:
                adquirentes.append(gradq.adquirente)
            return adquirentes

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()

    def get_queryset(self):
        cnpj = self.request.query_params.get('cnpj')
        return GrupoSerializer().buscarPorCnpj(cnpj)

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class CommanderViewSet(generics.ListCreateAPIView):
    serializer_class = CommanderSerializer
    queryset = AutoImplantar.objects.all()

    def put(self, request, *args, **kwargs):
        cnpj = request.GET['cnpj']
        msg = CommanderSerializer().autoImplantarCommanderPorGrupo(cnpj)

        html = "<!DOCTYPE html5><html><body><h2>%s</h2> <br/> </body></html>" % msg
        return HttpResponse(html)

class AutoImplantar(generics.ListCreateAPIView):
    queryset = AutoImplantar.objects.all()
    serializer_class = AutoContratarSerializer

    def get(self, request, *args, **kwargs):
        AutoContratarSerializer().implantar(request)
        # msg = 'Os dados de acesso serão enviados para o seu e-mail.'
        html = "<!DOCTYPE html5><html><head><script>setTimeout(function(){ window.location.href = '%s' }, 2000);" \
               "</script></head><body style='text-align: center; font-family: Sans'></br><h2>Nix Empresas</h2>" \
               "<p>Obrigado por confirmar! Aguarde...</p></body></html>" % (VIZZO_URL)
        return HttpResponse(html)

    def delete(self, request):
        AutoContratarSerializer().cancelar()
        content = {
            'status': 'Auto-Contratações vencidas canceladas com sucesso'
        }
        return Response(content)

class AdicionarAdquirenteViewSet(generics.ListCreateAPIView):
    serializer_class = GenskySerializer
    queryset = Adquirente.objects.all()

    def get(self, request, *args, **kwargs):
        cnpj = request.GET['cnpj']
        resultado = GenskySerializer().buscarAdquirentesDoGrupo(cnpj)
        print(resultado)
        return Response({"cnpj": cnpj, "adquirentes": resultado}, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        cnpj = request.GET['cnpj']
        numeroAdquirente = request.GET['adquirente']
        msg = GenskySerializer().adicionarNovaAdquirente(cnpj, numeroAdquirente)

        html = "<!DOCTYPE html5><html><body><h2>%s</h2> <br/> </body></html>" % msg
        return HttpResponse(html)

class AutenticarCartaoDeCreditoViewSet(generics.ListCreateAPIView):
    serializer_class = PagamentoCartaoSerializer
    queryset = PagamentoCartao.objects.all()

    def post(self, request):
        try:
            data = PagamentoCartaoSerializer().create(request.data)
            return Response({"tokenPagamento": data.tokenPagamento, "statusPagamento": data.statusPagamento}, status=HTTP_200_OK)

        except Exception as err:
            erro = err.__str__()
            if "SocialNumber is invalid" in erro:
               erro = "O CPF é inválido."

            if "not a valid credit card number" in erro:
                erro = "O número do cartão de crédito é inválido."

            if "Expired card" in erro:
                erro = "Cartão expirado."

            return Response({"error": erro}, status=HTTP_400_BAD_REQUEST)


class CallbackAutorizacaoCartaoDeCreditoViewSet(generics.ListCreateAPIView):
    serializer_class = CallBackSerializer
    queryset = PagamentoCartao.objects.all()

    def post(self, request):
        try:
            msg = CallBackSerializer().atualizarStatusPagamento(request.data)
            return Response({"message": msg}, status=HTTP_200_OK)

        except Exception as err:
            return Response({"error": err}, status=HTTP_400_BAD_REQUEST)


class CriarBoletoViewSet(generics.ListCreateAPIView):
    serializer_class = PagamentoBoletoSerializer
    queryset = PagamentoBoleto.objects.all()

    def post(self, request):
        try:
            print("criar boleto")
            data = PagamentoBoletoSerializer().create(request.data)
            return Response({"tokenPagamento": data.tokenPagamento, "statusPagamento": data.statusPagamento}, status=HTTP_200_OK)

        except Exception as err:
            erro = err.__str__()
            return Response({"error": erro}, status=HTTP_400_BAD_REQUEST)


class TemplateEmailViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateEmailSerializer
    queryset = TemplateEmail.objects.all()
