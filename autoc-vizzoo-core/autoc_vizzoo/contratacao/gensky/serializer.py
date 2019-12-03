from rest_framework import serializers
from ..models import AuditoriaImplantacao
from ..serializers import AdquirenteSerializer, GrupoSerializer, GrupoAdquirenteSerializer, MascaraSerialiazer, UsuarioSerializer, EstabelecimentoSerializer
from ..gensky.app import CadastroGenSky
from ..abertura_de_relacionamento.adquirenteservice import AdquirenteServiceImpl
from ..commander.apps import CadastroCommander

class GenskySerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        model = AuditoriaImplantacao

    def adicionarNovaAdquirente(self, cnpj, numeroAdquirente):
        try:
            msg = ""
            # buscar grupo
            arrayGrupo = GrupoSerializer().buscarPorCnpj(cnpj)
            grupo = None
            for gr in arrayGrupo:
                grupo = gr
            if grupo is None:
                msg = "Grupo %s não encontrado" % cnpj
                return msg

            # buscar adquirente
            adquirente = None
            arrayAdquirente = AdquirenteSerializer().buscarAdquirentePorPk(numeroAdquirente)
            for adq in arrayAdquirente:
                adquirente = adq
            if adquirente is None:
                msg = "Adquirente %s não encontrada" % str(numeroAdquirente)
                return msg

            arrayAdquirentesEncontrada = GrupoAdquirenteSerializer().buscarPorGrupoEAdquirente(grupo, adquirente)
            if len(arrayAdquirentesEncontrada) == 0:
                GrupoAdquirenteSerializer().criar(grupo, adquirente)
                msg = "Adquirente cadastrada para o grupo.<br/>"

            #buscar mascaras da adquirente
            mascaras = []
            arrayMasks = MascaraSerialiazer().buscarPorAdquirente(adquirente)
            for mascara in arrayMasks:
                mascaras.append(mascara)

            #montar caixaPostal
            commanderService = CadastroCommander()
            caixaPostal = commanderService.montarNomeCaixaPostal(cnpj)

            # buscar idCaixaPostal no Gensky
            genskyService = CadastroGenSky()
            idCaixaPostal = genskyService.buscar_caixa_postal(caixaPostal, cnpj)

            dsNamesArquivos = {}
            key = mascaras[0].adquirente.__str__()
            value = genskyService.cadastrar(idCaixaPostal, cnpj, mascaras)
            dsNamesArquivos[key] = []
            dsNamesArquivos[key].append(value)
            msg = msg + "Nova mascara cadastrada no Gensky.<br/>"

            #busca usuario
            usuSer = UsuarioSerializer()
            arrayUsuario = usuSer.buscarPorEmail(grupo.usuario.email)
            usuario = None
            for user in arrayUsuario:
                usuario = user
                break

            #buscar estabelecimentos
            estabSer = EstabelecimentoSerializer()
            arrayestab = estabSer.buscarPorGrupo(grupo)
            estabelecimentos = []
            for estab in arrayestab:
                estabelecimentos.append(estab)

            #chama serviço de envio de email
            service = AdquirenteServiceImpl()
            service.abrirRelacionamentoComAdquirentes(arrayAdquirente, grupo, estabelecimentos, usuario, dsNamesArquivos)
            msg = msg + "Abertura de relacionamento realizada"

            return msg
        except Exception as err:
            print(err)


