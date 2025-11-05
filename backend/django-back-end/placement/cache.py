# placement/cache.py
"""
Sistema de cache para otimizar performance do mapeamento
"""
from django.core.cache import cache
from typing import Any, Optional, Dict, List
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class CacheMapeamento:
    """
    Sistema de cache para operações de mapeamento
    """
    
    # Tempos de cache em segundos
    CACHE_TIMEOUT_PADRAO = 300  # 5 minutos
    CACHE_TIMEOUT_ANALISE = 600  # 10 minutos
    CACHE_TIMEOUT_IA = 1800  # 30 minutos
    
    @staticmethod
    def gerar_chave(*args, **kwargs) -> str:
        """
        Gera chave única para cache
        """
        data = f"{args}_{kwargs}"
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def get_analise_ia(mapeamento_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupera análise de IA do cache
        """
        chave = f"mapeamento_analise_{mapeamento_id}"
        return cache.get(chave)
    
    @staticmethod
    def set_analise_ia(mapeamento_id: int, dados: Dict[str, Any]) -> None:
        """
        Armazena análise de IA no cache
        """
        chave = f"mapeamento_analise_{mapeamento_id}"
        cache.set(chave, dados, CacheMapeamento.CACHE_TIMEOUT_IA)
        logger.debug(f"Análise de IA cacheada para mapeamento {mapeamento_id}")
    
    @staticmethod
    def get_layout_sugerido(mapeamento_id: int, criterios: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Recupera layout sugerido do cache
        """
        chave_data = f"{mapeamento_id}_{json.dumps(criterios, sort_keys=True)}"
        chave = f"mapeamento_layout_{CacheMapeamento.gerar_chave(chave_data)}"
        return cache.get(chave)
    
    @staticmethod
    def set_layout_sugerido(mapeamento_id: int, criterios: Dict[str, Any], layout: List[Dict[str, Any]]) -> None:
        """
        Armazena layout sugerido no cache
        """
        chave_data = f"{mapeamento_id}_{json.dumps(criterios, sort_keys=True)}"
        chave = f"mapeamento_layout_{CacheMapeamento.gerar_chave(chave_data)}"
        cache.set(chave, layout, CacheMapeamento.CACHE_TIMEOUT_IA)
    
    @staticmethod
    def invalidar_mapeamento(mapeamento_id: int) -> None:
        """
        Invalida todo cache relacionado a um mapeamento
        """
        keys_to_invalidate = [
            f"mapeamento_analise_{mapeamento_id}",
            f"mapeamento_layout_{mapeamento_id}",
            f"mapeamento_stats_{mapeamento_id}"
        ]
        
        for key in keys_to_invalidate:
            cache.delete(key)
        
        logger.info(f"Cache invalidado para mapeamento {mapeamento_id}")
    
    @staticmethod
    def get_estatisticas(mapeamento_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupera estatísticas do cache
        """
        chave = f"mapeamento_stats_{mapeamento_id}"
        return cache.get(chave)
    
    @staticmethod
    def set_estatisticas(mapeamento_id: int, stats: Dict[str, Any]) -> None:
        """
        Armazena estatísticas no cache
        """
        chave = f"mapeamento_stats_{mapeamento_id}"
        cache.set(chave, stats, CacheMapeamento.CACHE_TIMEOUT_PADRAO)
