from rest_framework import serializers
from ..models import AuditoriaImplantacao
from .apps import CadastroCommander
from ..auditoria.app import Auditoria
from ..serializers import GrupoSerializer

class CommanderSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
        model = AuditoriaImplantacao

    def autoImplantarCommanderPorGrupo(self, cnpj):
        caixaPostal = ""
        msg = ""
        try:
            gruSer = GrupoSerializer()
            arraygrupo = gruSer.buscarPorCnpj(cnpj)
            grupo = None
            for gru in arraygrupo:
                grupo = gru

            if grupo != None:
                commanderService = CadastroCommander()
                caixaPostal = commanderService.montarNomeCaixaPostal(cnpj)
                commanderService.cadastrar_no_commander(grupo)
                Auditoria().confirmarSucessoCommander(cnpj)
                msg = "O grupo %s realizou o cadastro da caixa postal %s com sucesso." % (cnpj, caixaPostal)
            else:
                msg = "Grupo não encontrado"
        except Exception as err:
            msg = err
            print(err)
        return msg
