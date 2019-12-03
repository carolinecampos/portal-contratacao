
class Utils:

    def removerCaracteresEspeciaisCNPJ(self, text):
        text1 = text.replace(".", "")
        text2 = text1.replace("-", "")
        return text2.replace("/", "")

    def adicionarCaracteresEspeciaisCNPJ(self, cnpj):
        return cnpj[0:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:14]

    def adicionarMascaraTelefone(self, telefone):
        tamanho = telefone.__sizeof__()
        return "(" + telefone[0:2] + ") " + telefone[2:6] + "-" + telefone[6:tamanho]

    def convertNumberToStringSemVirgula(self, number):
        s = "%8.2f" % number
        num = s.replace(" ", "").replace(".", "")
        return num

    def completarComZerosAEsquerda(self, number):
        novoValor = "%02d" % number
        return novoValor

