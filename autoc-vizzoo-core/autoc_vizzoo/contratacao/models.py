from __future__ import unicode_literals

from django.db import models, connection
from .enums import TipoTemplateEmail

class Adquirente(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    logo = models.CharField(max_length=400, blank=True, null=True)
    id_ordem = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    fg_arquivo = models.BooleanField()
    fg_email = models.BooleanField()
    fg_site_operadora = models.BooleanField()
    fg_infra_nexx = models.BooleanField()
    layout = models.CharField(max_length=100, blank=True, null=True)
    fg_ativo = models.NullBooleanField()

    class Meta:
        db_table = 'adquirente'

    def __str__(self):
        return self.nome

class Franquia(models.Model):
    qtde_transacao = models.IntegerField(null=True, blank=True)
    valor_fixo = models.FloatField(null=True, blank=True)
    valor_adicional = models.FloatField(null=True, blank=True)
    fg_ativo = models.NullBooleanField()
    merchant_plan_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'franquia'

    def __str__(self):
        return self.pk.__str__()

class Usuario(models.Model):
    nome = models.CharField(max_length=150, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    fg_ativo = models.NullBooleanField()
    is_vizzoo = models.NullBooleanField()
    dt_cadastro = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'usuario'

class Pagamento(models.Model):
    tipoPagamento = models.IntegerField(blank=True, null=True)
    numeroPedido = models.CharField(max_length=30, blank=True, null=True)
    tokenPagamento = models.CharField(max_length=50)
    statusPagamento = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pagamento'

    def __str__(self):
        return self.nomeImpresso

class PagamentoCartao(models.Model):
    numeroCartaoCredito = models.CharField(max_length=30, blank=True, null=True)
    codigoSeguranca = models.CharField(max_length=4, blank=True, null=True)
    dataValidade = models.DateField(blank=True, null=True)
    nomeImpresso = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=15, blank=True, null=True)
    tokenPagamento = models.CharField(max_length=50)
    tokenCard = models.CharField(max_length=50)
    statusPagamento = models.IntegerField(blank=True, null=True)
    codigoAutorizacao = models.CharField(max_length=20)
    retornoCodigoAutorizacao = models.CharField(max_length=20)
    bandeira = models.CharField(max_length=30)
    urlRetorno = models.CharField(max_length=2000)
    idCliente = models.BigIntegerField()
    pagamento = models.ForeignKey(Pagamento, related_name="PagamentoCartaoPag", default=None, null=True, blank=True)

    class Meta:
        db_table = 'pagamento_cartao'

    def __str__(self):
        return self.tokenPagamento

class PagamentoBoleto(models.Model):
    tokenPagamento = models.CharField(max_length=50)
    statusPagamento = models.IntegerField(blank=True, null=True)
    numeroBoleto = models.CharField(max_length=30)
    linhaDigitavel = models.CharField(max_length=70)
    urlRetorno = models.CharField(max_length=2000)
    dataExpiracao = models.DateField()
    pagamento = models.ForeignKey(Pagamento, related_name="PagamentoBoleto", default=None, null=True, blank=True)

    class Meta:
        db_table = 'pagamento_boleto'

    def __str__(self):
        return self.tokenPagamento

class Grupo(models.Model):
    razaosocial = models.CharField(max_length=200, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=8, blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    is_vizzoo = models.NullBooleanField()
    usuario = models.ForeignKey(Usuario, related_name="grupo")
    adquirentes = models.ManyToManyField(Adquirente, through='GrupoAdquirente')
    franquia = models.ForeignKey(Franquia, related_name="franquia", null=True)
    nome_caixa_postal = models.CharField(max_length=100, blank=True, null=True)
    pagamento = models.ForeignKey(Pagamento, related_name="GrupoPagamento", default=None, null=True, blank=True)

    class Meta:
        db_table = 'grupo'

    def __str__(self):
        return self.razaosocial

    def getNomeEmpresa(self):
        if not self.nome_fantasia:
            return self.nome_fantasia
        else:
            return self.razaosocial


class Estabelecimento(models.Model):
    razaosocial = models.CharField(max_length=200, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    is_vizzoo = models.NullBooleanField()
    grupo = models.ForeignKey(Grupo, related_name="estabelecimentos")

    class Meta:
        db_table = 'estabelecimento'

    def __str__(self):
        return self.razaosocial


class GrupoAdquirente(models.Model):
    grupo = models.ForeignKey(Grupo)
    adquirente = models.ForeignKey(Adquirente)
    fg_ativo = models.NullBooleanField(blank=False, null=False)

    class Meta:
        db_table = 'grupo_adquirente'


class AutoImplantar(models.Model):
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    grupo = models.ForeignKey(Grupo)
    usuario = models.ForeignKey(Usuario)
    dt_cadastro = models.DateField(blank=True, null=True)
    dt_vencimento = models.DateField(blank=True, null=True)
    hash_liberacao = models.CharField(max_length=255, blank=False, null=False)
    is_implantado = models.NullBooleanField(blank=False, null=False)

    class Meta:
        db_table = 'auto_implantar'

    def __str__(self):
        return self.cnpj

    def executeProcedureLimparGrupos(self, grupos):
        cur = connection.cursor()
        for grupo in grupos:
            cur.callproc('PROC_LIMPAR_POR_GRUPO', [grupo.pk, ])
        cur.close()


class Mascara(models.Model):
    adquirente = models.ForeignKey(Adquirente)
    id_caixa_postal = models.IntegerField()
    id_estacao = models.IntegerField()
    mask_banco_entrada = models.CharField(max_length=150, blank=True, null=True)
    mask_banco_saida = models.CharField(max_length=150, blank=True, null=True)
    mask_cliente_entrada = models.CharField(max_length=150, blank=True, null=True)
    mask_cliente_saida = models.CharField(max_length=150, blank=True, null=True)
    mask_envio_email = models.CharField(max_length=150, blank=True, null=True)
    nu_timeout = models.IntegerField()
    horas_iniciais = models.CharField(max_length=10, blank=True, null=True)
    horas_finais = models.CharField(max_length=10, blank=True, null=True)
    script_recepcao_banco = models.CharField(max_length=255, blank=False, null=False)
    script_transmissao_banco = models.CharField(max_length=255, blank=False, null=False)
    script_validacao_cliente = models.CharField(max_length=255, blank=False, null=False)
    observacao = models.CharField(max_length=255, blank=False, null=False)
    reset_cont_diario_rvs_cliente = models.BooleanField()
    herdar_cont_diario_rvs_cliente = models.BooleanField()
    contador_diario_rvs_cliente = models.IntegerField()
    verificar_duplicidade_rvs_cliente = models.BooleanField()
    reset_cont_diario_cliente_rvs = models.BooleanField()
    herdar_cont_diario_cliente_rvs = models.BooleanField()
    contador_diario_cliente_rvs = models.IntegerField()
    opcoes_envio_arquivo = models.IntegerField()
    script_envio = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        db_table = 'mascara'

    def __str__(self):
        return self.mask_banco_entrada

    def getMascaraBancoEntrada(self, cnpj):
        return self.mask_banco_entrada.__str__().replace("@CNPJ", cnpj)

    def getMascaraBancoSaida(self, cnpj, idCaixaPostal):
        return self.mask_banco_saida.__str__().replace("@ADQUIRENTE", self.adquirente.__str__()).replace("@CNPJ", cnpj).replace("@IDCXPOSTAL",  str(idCaixaPostal))

    def getMascaraEnvioEmail(self, cnpj, idCaixaPostal):
        return self.mask_envio_email.__str__().replace("@CNPJ", cnpj).replace("@IDCXPOSTAL", str(idCaixaPostal))

class AuditoriaImplantacao(models.Model):
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    dt_cadastro = models.DateField(blank=True, null=True)
    dt_ultima_alteracao = models.DateField(blank=True, null=True)
    fg_commander = models.NullBooleanField(blank=False, null=False)
    fg_gensky_caixa_postal = models.NullBooleanField(blank=False, null=False)
    fg_gensky_mascaras = models.NullBooleanField(blank=False, null=False)
    fg_vizzoo_grupo = models.NullBooleanField(blank=False, null=False)
    fg_vizzoo_estabelecimentos = models.NullBooleanField(blank=False, null=False)
    fg_vizzoo_usuario = models.NullBooleanField(blank=False, null=False)
    fg_abertura_relacionamento = models.NullBooleanField(blank=False, null=False)

    class Meta:
        db_table = 'auditoria_implantacao'

    def __str__(self):
        return self.cnpj

class AuditoriaErros(models.Model):
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    dt_erro = models.DateField(blank=True, null=True)
    header = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    dados_json = models.CharField(max_length=2000, blank=True, null=True)
    erro = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        db_table = 'auditoria_erros'

    def __str__(self):
        return self.cnpj

class BlackList_Estabelecimento(models.Model):
    razaosocial = models.CharField(max_length=200, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    is_ativo = models.NullBooleanField()

    class Meta:
        db_table = 'blacklist_estabelecimento'

    def __str__(self):
        return self.razaosocial

class TemplateEmail(models.Model):
    email_remetente = models.CharField(max_length=100, blank=True, null=True)
    assunto = models.CharField(max_length=200, blank=False, null=False)
    email_destinatario = models.CharField(max_length=100, blank=False, null=False)
    nome_destinatario = models.CharField(max_length=100, blank=True, null=True)
    corpo = models.TextField(blank=False, null=False)
    tipo_template = models.CharField(max_length=10, blank=False, null=False, choices=TipoTemplateEmail.choices)
    
    class Meta:
        db_table = 'TEMPLATE_EMAIL'