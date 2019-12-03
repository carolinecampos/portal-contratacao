from django.conf.urls import url, include
from rest_framework import routers
from .views import AdquirenteViewSet, GrupoViewSet, UsuarioViewSet, AutoImplantar, FranquiaViewSet, CommanderViewSet, AdicionarAdquirenteViewSet, BlackListEstabelecimentoViewSet, AutenticarCartaoDeCreditoViewSet, CallbackAutorizacaoCartaoDeCreditoViewSet, CriarBoletoViewSet, GrupoAdquirenteViewSet, TemplateEmailViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
URL_ROOT = 'autocontratacao/'

schema_view = get_schema_view(
    openapi.Info(title="Auto Contração Vizzoo", default_version='v1'),
    public=True,
)

router = routers.DefaultRouter()
router.register(r'adquirentes', AdquirenteViewSet)
router.register(r'blacklist', BlackListEstabelecimentoViewSet)
router.register(r'franquias', FranquiaViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'grupoAdquirente', GrupoAdquirenteViewSet)
router.register(r'templateEmail', TemplateEmailViewSet)

urlpatterns = [
    url(r'^{}'.format(URL_ROOT), include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'autoimplantar', AutoImplantar.as_view()),
    url(r'autocontratacao/commander', CommanderViewSet.as_view()),
    url(r'autocontratacao/adquirente/add', AdicionarAdquirenteViewSet.as_view()),
    url(r'autocontratacao/autenticarCartaoCredito', AutenticarCartaoDeCreditoViewSet.as_view()),
    url(r'autocontratacao/callbackCartaoCredito', CallbackAutorizacaoCartaoDeCreditoViewSet.as_view()),
    url(r'autocontratacao/criarBoleto', CriarBoletoViewSet.as_view()),
    url(r'api-docs', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
]
