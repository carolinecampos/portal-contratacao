from rest_framework import serializers
from datetime import date, timedelta
from .models import Adquirente, Estabelecimento, Grupo, Usuario, AutoImplantar, GrupoAdquirente, Franquia, Mascara, BlackList_Estabelecimento, Pagamento, PagamentoCartao, PagamentoBoleto, TemplateEmail
from .email_sender.apps import EnvioDeEmail
from .abertura_de_relacionamento.adquirenteservice import AdquirenteServiceImpl
from .commander.apps import CadastroCommander
from .gensky.app import CadastroGenSky
from .vizzoo.apps import CadastroVizzoo
from .auditoria.app import Auditoria
from .utils import Utils
from .gateway.apps import Gateway
from .apps import AutoContratar

class GrupoAdquirenteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = GrupoAdquirente

    def buscarPorGrupo(self, grupo):
        return GrupoAdquirente.objects.filter(grupo=grupo)

    def buscarPorGrupoEAdquirente(self, grupo, adquirente):
        return GrupoAdquirente.objects.filter(adquirente=adquirente, grupo=grupo)

    def criar(self, grupo, adquirente):
        return GrupoAdquirente.objects.create(grupo=grupo, adquirente=adquirente, fg_ativo=False)

    def buscarPorCnpj(self, cnpj):
        try:
            soNumeros = Utils().removerCaracteresEspeciaisCNPJ(cnpj)
            grupoArray = GrupoSerializer().buscarPorCnpj(soNumeros)
            if not grupoArray:
                return []
            for grupo in grupoArray:
                return GrupoAdquirente.objects.filter(grupo=grupo)

        except Exception as err:
            raise Exception("Erro ao buscar as adquirentes do grupo. {}".format(err))

class MascaraSerialiazer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Mascara

    def buscarPorAdquirente(self, adquirente):
        return Mascara.objects.filter(adquirente=adquirente)

class AdquirenteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Adquirente

    def buscarAtivas(self):
        return Adquirente.objects.filter(fg_ativo=True).order_by('id_ordem')

    def buscarAdquirentePorPk(self, pk):
        return Adquirente.objects.filter(fg_ativo=True, pk=pk)

class FranquiaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Franquia

    def buscarAtivas(self):
        return Franquia.objects.filter(fg_ativo=True).order_by('qtde_transacao')

    def buscarPorPK(self, pk):
        return Franquia.objects.filter(pk=pk)

class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('grupo',)
        model = Estabelecimento

    def buscarPorGrupo(self, grupo):
        return Estabelecimento.objects.filter(grupo=grupo)

    def buscarPorCnpj(self, cnpj):
        return Estabelecimento.objects.filter(cnpj=cnpj)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def buscarPorEmail(self, email):
        return Usuario.objects.filter(email=email)

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    estabelecimentos = EstabelecimentoSerializer(many=True)
    adquirentes = serializers.PrimaryKeyRelatedField(many=True, queryset=Adquirente.objects.all())
    pagamento = PagamentoSerializer()

    class Meta:
        model = Grupo
        fields = '__all__'

    def atualizarCaixaPostal(self, cnpj, caixaPostal):
        Grupo.objects.filter(cnpj=cnpj).update(nome_caixa_postal=caixaPostal)

    def buscarPorCnpj(self, cnpj):
        return Grupo.objects.filter(cnpj=cnpj)

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        estabelecimentos_data = validated_data.pop('estabelecimentos')
        adquirentes_data = validated_data.pop('adquirentes')
        pagamento_date = validated_data.pop('pagamento')
        token = pagamento_date['tokenPagamento']

        usuario = Usuario.objects.create(**usuario_data)
        pagamento = Pagamento.objects.create(**pagamento_date)
        grupo = Grupo.objects.create(usuario=usuario, **validated_data)

        tipoPagamento = pagamento_date['tipoPagamento']
        franquia = validated_data['franquia']
        valorFranquia = Utils().convertNumberToStringSemVirgula(franquia.valor_fixo)
        numPedido = Gateway().montarNumeroPedido(valorFranquia, grupo.cnpj)
        # atualizar pagamento cartão
        if tipoPagamento == 1:
            Pagamento.objects.filter(pk=pagamento.pk).update(numeroPedido=numPedido)
            PagamentoCartaoSerializer().atualizarPagamento(token, pagamento)
        # atualizar pagamento Boleto
        else:
            Pagamento.objects.filter(pk=pagamento.pk).update(numeroPedido=numPedido)
            PagamentoBoletoSerializer().atualizarPagamento(token, pagamento)

        self.atualizarPagamento(grupo.pk, pagamento)

        lista_estabelecimentos = []
        lista_adquirentes = []
        
        for estabelecimento_data in estabelecimentos_data:
            estabelecimento = Estabelecimento.objects.create(grupo=grupo, **estabelecimento_data)
            if (estabelecimento.cnpj != grupo.cnpj):
                lista_estabelecimentos.append(estabelecimento)

        for adquirente_data in adquirentes_data:
            adquirente = GrupoAdquirente.objects.create(grupo=grupo, adquirente=adquirente_data, fg_ativo=False)
            lista_adquirentes.append(adquirente)

        autoInstance = AutoContratarSerializer()
        autoContratar = autoInstance.montarObjeto(grupo, usuario)
        AutoImplantar.objects.create(cnpj=autoContratar.cnpj, email=autoContratar.email, grupo=grupo, usuario=usuario,
                                     dt_cadastro=autoContratar.dt_cadastro, dt_vencimento=autoContratar.dt_vencimento,
                                     hash_liberacao=autoContratar.hash_liberacao,
                                     is_implantado=autoContratar.is_implantado)

        grupo.usuario = usuario
        instancia = EnvioDeEmail()
        instancia.enviarEmailParaConfirmarDados(grupo, lista_adquirentes, lista_estabelecimentos, autoContratar.hash_liberacao)

        backlistService = BlackListEstabelecimentoSerializer()
        backlistService.create(grupo.cnpj, grupo.razaosocial)
        for estab in lista_estabelecimentos:
            backlistService.create(estab.cnpj, estab.razaosocial)
        
        return grupo

    def get_last_object_created(self):
        return self.last_grupo

    def atualizarPagamento(self, pk, pagamento):
        return Grupo.objects.filter(pk=pk).update(pagamento=pagamento)


class AutoContratarSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoImplantar
        fields = ("email", "cnpj", "hash_liberacao")

    def buscarAutoImplantacoesVencidas(self):
        return AutoImplantar.objects.filter(dt_vencimento__lt=date.today())

    def montarObjeto(self, grupo, usuario):
        obj = AutoImplantar()
        obj.cnpj = grupo.cnpj
        obj.email = usuario.email
        obj.dt_cadastro = date.today()
        obj.dt_vencimento = date.today() + timedelta(days=7)
        obj.is_implantado = False
        hash = self.montarHash(obj)
        obj.hash_liberacao = hash
        return obj

    def montarHash(self, autoImplantar):
        hash = "autoc" + autoImplantar.dt_cadastro.strftime('%d%m%Y') + "uid" + autoImplantar.usuario_id.__str__() + "grid" + autoImplantar.grupo_id.__str__() + "dtvc" + autoImplantar.dt_vencimento.strftime('%d%m%Y')
        return hash

    def implantar(self, request):
        print("chamar métodos de auto-contratacao")
        cnpj = request.GET['cnpj']
        email = request.GET['email']
        hash_liberacao = request.GET['hash_liberacao']

        Auditoria().salvarImplantacao(cnpj)

        print("buscar grupo")
        gruSer = GrupoSerializer()
        arraygrupo = gruSer.buscarPorCnpj(cnpj)
        grupo = None
        for gru in arraygrupo:
            grupo = gru

        print("buscar usuario")
        usuSer = UsuarioSerializer()
        arrayUsuario = usuSer.buscarPorEmail(grupo.usuario.email)
        usuario = None
        for user in arrayUsuario:
            usuario = user
            break

        print("buscar lista_estabelecimentos")
        estabSer = EstabelecimentoSerializer()
        arrayestab = estabSer.buscarPorGrupo(grupo)
        estabelecimentos = []
        for estab in arrayestab:
            estabelecimentos.append(estab)

        print("cadastrar caixa postal commander")
        caixaPostal = ""
        try:
            commanderService = CadastroCommander()
            caixaPostal = commanderService.montarNomeCaixaPostal(cnpj)
            commanderService.cadastrar_no_commander(grupo)
            Auditoria().confirmarSucessoCommander(cnpj)
            gruSer.atualizarCaixaPostal(cnpj, caixaPostal)
        except Exception as err:
            print(err)

        print("buscar as adquirentes do grupo")
        grAdSer = GrupoAdquirenteSerializer()
        gruposAdquirentes = grAdSer.buscarPorGrupo(grupo)
        adquirentes = []
        for grupoAdq in gruposAdquirentes:
            adquirentes.append(grupoAdq.adquirente)

        maskInstance = MascaraSerialiazer()
        mascaras = []
        for adquirente in adquirentes:
            masks = maskInstance.buscarPorAdquirente(adquirente)
            mascaras.append(masks)
            for mascara in mascaras:
                mascara[0].adquirente = adquirente

        dsNamesArquivos = {}
        try:
            genskyService = CadastroGenSky()
            idCaixaPostal = genskyService.criar_caixa_postal(caixaPostal, cnpj)
            Auditoria().confirmarSucessoGenskyCaixaPostal(cnpj)

            service = AdquirenteServiceImpl()
            for arrayMask in mascaras:
                key = arrayMask[0].adquirente.__str__()
                value = genskyService.cadastrar(idCaixaPostal, cnpj, arrayMask)
                dsNamesArquivos[key] = []
                dsNamesArquivos[key].append(value)

            Auditoria().confirmarSucessoGenskyMascaras(cnpj)
        except Exception as err:
            print(err)

        try:
            service.abrirRelacionamentoComAdquirentes(adquirentes, grupo, estabelecimentos, usuario, dsNamesArquivos)
            Auditoria().confirmarSucessoAberturaRelacionamento(cnpj)
            print("enviar email para as adquirentes do grupo")
        except Exception as err:
            print(err)

        try:
            instancia = CadastroVizzoo()
            instancia.cadastrar_no_vizzoo(grupo, usuario, estabelecimentos)
        except Exception as err:
            print(err)

    def cancelar(self):
        """buscar todas as autoimplantacoes com data vencidas"""
        contratacoes = self.buscarAutoImplantacoesVencidas()
        grupos = []
        for contrato in contratacoes:
            grupos.append(contrato.grupo)
        instacia = AutoImplantar()
        instacia.executeProcedureLimparGrupos(grupos)
        print("autoimplantacoes vencidas foram apagadas")


class BlackListEstabelecimentoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = BlackList_Estabelecimento

    def buscarPorCnpj(self, cnpj):
        soNumeros = Utils().removerCaracteresEspeciaisCNPJ(cnpj)
        estabelecimentos = []
        arrayBackList = BlackList_Estabelecimento.objects.filter(cnpj=soNumeros, is_ativo=True)
        for item in arrayBackList:
            estabelecimentos.append(item)
        print(estabelecimentos)
        return estabelecimentos

    def create(self, cnpj, razaosocial):
        try:
            soNumeros = Utils().removerCaracteresEspeciaisCNPJ(cnpj)
            BlackList_Estabelecimento.objects.create(cnpj=soNumeros, razaosocial=razaosocial, is_ativo=True)
        except Exception as err:
            raise Exception("Erro ao salvar estabelecimento na Lista Negra {}".format(err))


class PagamentoCartaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PagamentoCartao
        fields = '__all__'

    def create(self, data):
        pagamento = data['pagamento']
        usuario = data['usuario']
        objetoCriado = AutoContratar().autenticarCartaoDeCredito(pagamento, data, usuario)
        return objetoCriado

    def buscarPagamentoCartao(self, tokenPagamento):
        return PagamentoCartao.objects.filter(tokenPagamento=tokenPagamento)

    def atualizarPagamento(self, tokenPagamento, pagamento):
        PagamentoCartao.objects.filter(tokenPagamento=tokenPagamento).update(pagamento=pagamento)


class PagamentoBoletoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PagamentoBoleto
        fields = '__all__'

    def create(self, data):
        usuario = data['usuario']
        objetoCriado = AutoContratar().criarBoletoBancario(data, usuario)
        return objetoCriado

    def atualizarPagamento(self, tokenPagamento, pagamento):
        PagamentoBoleto.objects.filter(tokenPagamento=tokenPagamento).update(pagamento=pagamento)


class TemplateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateEmail
        fields = '__all__'
