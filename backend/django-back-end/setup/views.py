from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time
import os
from datetime import datetime

def health_check(request):
    """
    Endpoint de health check melhorado que verifica:
    - Status da aplicação
    - Conexão com banco de dados
    - Cache (se configurado)
    - Informações do ambiente
    """
    health_data = {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production",
    }
    
    # Verifica conexão com banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_data["database"] = "connected"
    except Exception as e:
        health_data["database"] = f"error: {str(e)}"
        health_data["status"] = "error"
    
    # Verifica cache (se configurado)
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        health_data["cache"] = "connected" if cache_result == 'ok' else "error"
    except Exception as e:
        health_data["cache"] = f"error: {str(e)}"
    
    # Informações do sistema
    health_data["system"] = {
        "debug": settings.DEBUG,
        "database_engine": settings.DATABASES['default']['ENGINE'],
        "installed_apps_count": len(settings.INSTALLED_APPS),
        "timezone": str(settings.TIME_ZONE),
    }
    
    # Status HTTP baseado na saúde geral
    status_code = 200 if health_data["status"] == "ok" else 503
    
    return JsonResponse(health_data, status=status_code)

def api_info(request):
    """
    Endpoint que retorna informações sobre a API
    """
    return JsonResponse({
        "name": "S.U.M API",
        "version": "1.0.0",
        "description": "Sistema Unificado de Mapeamento - API",
        "endpoints": {
            "health": "/api/health/",
            "auth": "/api/auth/",
            "escola": "/api/escola/",
            "estudantes": "/api/estudantes/",
            "professores": "/api/professores/",
            "atividades": "/api/atividades/",
            "eventos": "/api/eventos/",
            "mapeamento": "/api/mapeamento/",
        },
        "documentation": "/api/docs/",
        "admin": "/admin/",
    })

def custom_admin_view(request):
    """
    View personalizada para o painel administrativo
    """
    return render(request, 'admin/custom_admin.html')

def api_documentation_view(request):
    """
    View para a documentação da API
    """
    return render(request, 'api/documentation.html')

def system_status_view(request):
    """
    View para o status do sistema
    """
    return render(request, 'status/system_status.html')

def custom_404_view(request, exception=None):
    """
    View personalizada para erro 404
    """
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    """
    View personalizada para erro 500
    """
    return render(request, 'errors/500.html', status=500)

def generic_error_view(request, exception=None):
    """
    View genérica para outros erros
    """
    return render(request, 'errors/generic_error.html', status=500)