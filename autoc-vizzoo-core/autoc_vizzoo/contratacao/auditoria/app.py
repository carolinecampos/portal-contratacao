from ..models import AuditoriaErros, AuditoriaImplantacao
from datetime import date

class Auditoria:

    def salvarErro(self, cnpj, url, data_json, header, erro):
        AuditoriaErros.objects.create(cnpj=cnpj, header=header, url=url, dados_json=data_json, dt_erro=date.today(),
                                      erro=erro)
        print("Erro salvo para análise")

    def salvarImplantacao(self, cnpj):
        try:
            AuditoriaImplantacao.objects.create(cnpj=cnpj, dt_cadastro=date.today(), dt_ultima_alteracao=date.today(),
                                            fg_commander=False, fg_gensky_caixa_postal=False, fg_gensky_mascaras=False,
                                            fg_vizzoo_grupo=False, fg_vizzoo_estabelecimentos=False,
                                            fg_vizzoo_usuario=False, fg_abertura_relacionamento=False)
            print("Implantacao iniciada")
        except Exception as err:
            raise Exception("Erro ao salvar implantacao {}".format(err))


    def confirmarSucessoCommander(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_commander=True, dt_ultima_alteracao=date.today())
        print("atualizar fg commander")

    def confirmarSucessoGenskyCaixaPostal(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_gensky_caixa_postal=True,
                                                              dt_ultima_alteracao=date.today())
        print("atualizar fg gensky caixa postal")

    def confirmarSucessoGenskyMascaras(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_gensky_mascaras=True, dt_ultima_alteracao=date.today())
        print("atualizar fg gensky mascaras")

    def confirmarSucessoVizzooGrupo(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_vizzoo_grupo=True, dt_ultima_alteracao=date.today())
        print("atualizar fg vizzo grupo")

    def confirmarSucessoVizzooEstabelecimentos(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_vizzoo_estabelecimentos=True,
                                                              dt_ultima_alteracao=date.today())
        print("atualizar fg vizzo estabelecimento")

    def confirmarSucessoVizzooUsuario(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_vizzoo_usuario=True, dt_ultima_alteracao=date.today())
        print("atualizar fg vizzo usuario")

    def confirmarSucessoAberturaRelacionamento(self, cnpj):
        AuditoriaImplantacao.objects.filter(cnpj=cnpj).update(fg_abertura_relacionamento=True, dt_ultima_alteracao=date.today())
        print("atualizar fg_abertura_relacionamento")

