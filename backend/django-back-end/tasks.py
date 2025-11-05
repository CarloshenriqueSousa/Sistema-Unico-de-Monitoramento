# placement/tasks.py
from celery import shared_task
from .services import gerar_novo_mapeamento

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def task_gerar_mapeamento(self, turma_id, escola_id, nome, linhas, colunas):
    try:
        turma = Turma.objects.get(id=turma_id)
        escola = Escola.objects.get(id=escola_id)
        gerar_novo_mapeamento(turma, escola, nome, linhas, colunas)
    except Exception as exc:
        self.retry(exc=exc)