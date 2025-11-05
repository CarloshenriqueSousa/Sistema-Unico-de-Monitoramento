# core/health_views.py
"""
Views para monitoramento de saúde do sistema
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import psutil
import time
from datetime import datetime


def health_check(request):
    """
    Endpoint de health check básico
    """
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'S.U.M Backend'
    })


def detailed_health(request):
    """
    Endpoint de health check detalhado com todas as conexões
    """
    health_data = {
        'timestamp': datetime.now().isoformat(),
        'service': 'S.U.M Backend',
        'version': '2.0',
        'checks': {}
    }
    
    # 1. Verificar banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data['checks']['database'] = {
                'status': 'healthy',
                'response_time': '< 1ms',
                'engine': settings.DATABASES['default']['ENGINE']
            }
    except Exception as e:
        health_data['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # 2. Verificar cache
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        health_data['checks']['cache'] = {
            'status': 'healthy' if cache_result == 'ok' else 'unhealthy',
            'backend': getattr(settings, 'CACHES', {}).get('default', {}).get('BACKEND', 'unknown')
        }
    except Exception as e:
        health_data['checks']['cache'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # 3. Verificar sistema
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data['checks']['system'] = {
            'status': 'healthy',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_free_gb': round(disk.free / (1024**3), 2)
        }
    except Exception as e:
        health_data['checks']['system'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # 4. Verificar configurações
    health_data['checks']['configuration'] = {
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'cors_origins': getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
        'database_name': settings.DATABASES['default']['NAME']
    }
    
    # Status geral
    all_healthy = all(
        check.get('status') == 'healthy' 
        for check in health_data['checks'].values() 
        if isinstance(check, dict) and 'status' in check
    )
    
    health_data['status'] = 'healthy' if all_healthy else 'degraded'
    
    return JsonResponse(health_data, status=200 if all_healthy else 503)


def system_metrics(request):
    """
    Endpoint para métricas detalhadas do sistema
    """
    try:
        # Informações do sistema
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        # Processos Python
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if 'python' in proc.info['name'].lower():
                    python_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime.total_seconds(),
            'uptime_human': str(uptime).split('.')[0],
            'boot_time': boot_time.isoformat(),
            'cpu': {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=1),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            'memory': {
                'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'percent': psutil.virtual_memory().percent,
                'used_gb': round(psutil.virtual_memory().used / (1024**3), 2)
            },
            'disk': {
                'total_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                'free_gb': round(psutil.disk_usage('/').free / (1024**3), 2),
                'percent': psutil.disk_usage('/').percent,
                'used_gb': round(psutil.disk_usage('/').used / (1024**3), 2)
            },
            'network': {
                'connections': len(psutil.net_connections()),
                'interfaces': len(psutil.net_if_addrs())
            },
            'python_processes': python_processes[:10]  # Top 10
        }
        
        return JsonResponse(metrics)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)
