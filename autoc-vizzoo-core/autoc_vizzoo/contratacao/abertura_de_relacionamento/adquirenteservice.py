from ..email_sender.apps import EnvioDeEmail
from ..utils import Utils

class AdquirenteServiceImpl:

    def abrirRelacionamentoComAdquirentes(self, adquirentes, grupo, estabelecimentos, usuario, dsNamesArquivos):
        print(adquirentes)
        temImplementacao = False
        for adquirente in adquirentes:
            if adquirente.fg_arquivo:
                self.implantarArquivo()
                temImplementacao = True

            if adquirente.fg_email:
                self.implantarEnvioDeEmail(estabelecimentos, usuario, grupo, adquirente, dsNamesArquivos)
                temImplementacao = True

            if adquirente.fg_infra_nexx:
                self.implantarInfraNexx(estabelecimentos, usuario, grupo, adquirente, dsNamesArquivos)
                temImplementacao = True

            if adquirente.fg_site_operadora:
                self.implantarSiteOperadora()
                temImplementacao = True

            if not temImplementacao:
                print("Adquirente (" + adquirente.__str__() + ") não implementada.")

        print("Abertura de Relacionamento com Adquirentes finalizado")

    def implantarEnvioDeEmail(self, estabelecimentos, usuario, grupo, adquirente, dsNamesArquivos):
        emailDeOrigem = "autocontratacaovizzo@nexxera.com"
        emailDestino = adquirente.email + "," + usuario.email
        titulo = "Abertura de Relacionamento Nexxera NIXEMPRESA X " + adquirente.nome
        mensagem = self.montarMensagemDeEmail(adquirente, estabelecimentos, grupo, dsNamesArquivos, usuario)
        service = EnvioDeEmail()
        service.envioPadrao(emailDeOrigem, emailDestino, titulo, mensagem, grupo.cnpj)
        print("implantação por email : " + adquirente.__str__())

    def implantarArquivo(self):
        print("implantação por email")

    def implantarSiteOperadora(self):
        print("implantar site de operadora")

    def implantarInfraNexx(self, estabelecimentos, usuario, grupo, adquirente, dsNamesArquivos):
        emailDeOrigem = "implantacao.nixempresa@nexxera.com "
        emailDestino = adquirente.email + "," + usuario.email
        titulo = "Abertura de Relacionamento Nexxera NIXEMPRESA X " + adquirente.nome
        mensagem = self.montarMensagemDeEmail(adquirente, estabelecimentos, grupo, dsNamesArquivos, usuario)
        service = EnvioDeEmail()
        service.envioPadrao(emailDeOrigem, emailDestino, titulo, mensagem, grupo.cnpj)
        print("implantação por email : " + adquirente.__str__())

    def montarMensagemDeEmail(self, adquirente, estabelecimentos, grupo, dsNamesArquivos, usuario):
        msg = "Empresa: " + grupo. __str__()
        msg = msg + "<br/>Responsável: " + usuario.nome + "<br/>Telefone: " + Utils().adicionarMascaraTelefone(usuario.telefone) + "<br/>Email: " + usuario.email
        msg = msg + "<br/><br/>Prezados, bom dia <br/><br/>Solicitamos a abertura de relacionamento para tráfego dos arquivos de extrato para os sequintes estabelecimentos: <br/>"
        for estabelecimento in estabelecimentos:
            msg = msg + "<br/>Razão Social: <strong>" + estabelecimento.razaosocial + "</strong><br/>CNPJ: <strong>" + Utils().adicionarCaracteresEspeciaisCNPJ(estabelecimento.cnpj) +"</strong><br/>"

        dsnames = dsNamesArquivos.get(adquirente.__str__())

        msg = msg + "<br/>Outras informações:<br/>DSName:"
        for name in dsnames:
            if str(name).strip() == "":
                del[name]

        dsname = str(dsnames).replace("[", "").replace("]", "").replace(", ''", "").replace("'',", "").replace("'", "")
        msg = msg + dsname + "<br/>Layout: " + adquirente.layout +"<br/>VAN: Nexxera<br/>Periodicidade:Diário<br/>"
        msg = msg + "<br/>Atenciosamente,<br/><br/>Sistema de auto-contratação Nexxera<br/>"
        return msg
