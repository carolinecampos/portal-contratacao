from django.contrib import admin

from .models import Adquirente, Estabelecimento, Grupo, Usuario


class AdquirenteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'logo', 'id_ordem', 'email', 'fg_arquivo',
                    'fg_email', 'fg_site_operadora', 'fg_infra_nexx']


class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'razaosocial', 'cnpj', 'is_vizzoo', 'grupo']


class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id', 'razaosocial', 'cnpj', 'nome_fantasia', 'inscricao_estadual',
                    'endereco', 'bairro', 'cidade', 'cep', 'uf', 'is_vizzoo', 'usuario']


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'telefone', 'email', 'fg_ativo', 'is_vizzoo', 'dt_cadastro']


admin.site.register(Adquirente, AdquirenteAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
