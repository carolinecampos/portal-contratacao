from ..settings import CONFIRMAR_DADOS_USUARIO
from .notifiersender import NotifierSenderImpl
from ..utils import Utils
import json

class EnvioDeEmail:

    def envioPadrao(self, emailDeOrigem, destinatarios, titulo, mensagem, cnpj):
        data_json = {
            'to': destinatarios,
            'from': emailDeOrigem,
            'content': mensagem,
            'subject': titulo
        }
        servico = NotifierSenderImpl()
        servico.post_message(json.dumps(data_json), cnpj)

    def enviarEmailParaConfirmarDados(self, Grupo, lista_adquirentes, lista_estabelecimentos, hash):
        mensagem = self.criarMensagem(Grupo, lista_adquirentes, lista_estabelecimentos, hash)
        data_json = {
            'to': Grupo.usuario.email,
            'from': 'no-reply@nexxera.com',
            'content': mensagem,
            'subject': 'Conciliação de Cartões - Nix Empresas'
        }
        servico = NotifierSenderImpl()
        servico.post_message(json.dumps(data_json), Grupo.cnpj)

    def criarMensagem(self, Grupo, lista_adquirentes, lista_estabelecimentos, hash):
        nome = "<br/>Nome: <strong>" + Grupo.usuario.nome + "</strong>"
        telefone = "<br/>Telefone: <strong>" + Utils().adicionarMascaraTelefone(Grupo.usuario.telefone) + "</strong>"
        email = "<br/>E-mail: <strong>" + Grupo.usuario.email + "</strong>"
#       data = "\nData do Cadastro= ".join(str(Grupo.usuario.dt_cadastro) for dt in None)
        maskCnpj = Utils().adicionarCaracteresEspeciaisCNPJ(Grupo.cnpj)
        grupo = "<br/>Grupo: <strong>" + Grupo.razaosocial + " - " + maskCnpj + "</strong>"

        """Estabelecimentos"""
        estabelecimentos = " <br/>Estabelecimentos Adicionais: <strong>"
        for estab in lista_estabelecimentos:
            maskCnpj = Utils().adicionarCaracteresEspeciaisCNPJ(estab.cnpj)
            estabelecimentos += estab.razaosocial + " - " + maskCnpj + ", "
        estabelecimentos = estabelecimentos[:-2] + "</strong>"

        """Adquirentes"""
        adquirentes = " <br/>Adquirentes: <strong>"
        for objeto in lista_adquirentes:
            adquirentes += objeto.adquirente.nome + ", "
        adquirentes = adquirentes[:-2] + "</strong>"

        src = CONFIRMAR_DADOS_USUARIO + "?email=" + Grupo.usuario.email + "&cnpj=" + Grupo.cnpj + "&hash_liberacao=" + hash
        link = "<br/><br/><a href='%s' target='_blank'>Clique aqui para ativar</a><br/><br/>Nix Empresas" % src

        msg = "Você contratou a Conciliação de Cartões. Por favor, confirme os dados e ative o recurso.<br/>"
        msgAlerta = "<br/>As adquirentes serão notificadas para serem integradas ao sistema."
        msg += nome + telefone + email + grupo + estabelecimentos + adquirentes + msgAlerta + link

        return msg


