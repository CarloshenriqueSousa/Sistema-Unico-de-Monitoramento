from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    health_check, api_info, custom_admin_view, api_documentation_view,
    system_status_view, custom_404_view, custom_500_view, generic_error_view
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Páginas personalizadas
    path('admin/custom/', custom_admin_view, name='custom_admin'),
    path('api/docs/', api_documentation_view, name='api_docs'),
    path('status/', system_status_view, name='system_status'),
    
    # Health check específico para admin
    path('admin/health/', health_check, name='admin_health_check'),

    # Endpoints de API (agrupados sob /api/)
    path('api/health/', health_check, name='api_health_check'),
    path('api/info/', api_info, name='api_info'),
    path('api/ping/', health_check, name='api_ping'),

    # Core (autenticação)
    path('api/auth/', include('core.urls')),

    # AI endpoints
    # Included inside core app paths already; exposed here via /api/auth/ai/*
    # Frontend calls use /api/ai/*, so include a direct alias as well
    path('api/ai/', include(('core.urls', 'core'), namespace='ai_alias')),

    # Apps principais
    path('api/escola/', include(('escola.urls', 'escola'), namespace='escola')),
    path('api/estudantes/', include(('estudantes.urls', 'estudantes'), namespace='estudantes')),
    path('api/professores/', include(('professores.urls', 'professores'), namespace='professores')),
    path('api/atividades/', include(('atividades.urls', 'atividades'), namespace='atividades')),
    path('api/eventos/', include(('eventos.urls', 'eventos'), namespace='eventos')),
    path('api/mapeamento/', include(('placement.urls', 'placement'), namespace='placement')),

    # DOTS endpoints
    path('api/dots/', include(('estudantes.dots_urls', 'dots'), namespace='dots')),
]

# Configuração para servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Handlers de erro personalizados
handler404 = custom_404_view
handler500 = custom_500_view
