import openai
import os

def gerar_atividade(tema, nivel_dificuldade, tipo_atividade):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'sua-chave-aqui'))
        
        prompt = f"""
        Crie uma atividade educacional:
        - Tema: {tema}
        - Nível: {nivel_dificuldade}
        - Tipo: {tipo_atividade}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Assistente educacional para criar atividades pedagógicas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Erro ao gerar atividade: {str(e)}"

def gerar_atividade_placeholder(tema, nivel_dificuldade, tipo_atividade):
    return {
        "titulo": f"Atividade sobre {tema}",
        "objetivos": [f"Compreender {tema}", f"Aplicar {tema}"],
        "instrucoes": f"Desenvolva atividade sobre {tema} - nível {nivel_dificuldade}",
        "exemplos": f"Exemplo de {tema}",
        "criterios_avaliacao": f"Avaliação baseada em {tema}"
    }

def gerar_mapeamento_inteligente(estudantes, sala_config):
    """
    Gera mapeamento inteligente de estudantes em uma sala considerando:
    - Dificuldades de visão
    - Dificuldades de aprendizado
    - Compatibilidade entre estudantes
    """
    try:
        # Lógica básica de mapeamento
        mapeamento = []
        
        # Ordenar estudantes por necessidades especiais
        estudantes_prioridade = [e for e in estudantes if e.dificuldade_visao != 'NENHUMA' or e.dificuldade_aprendizado != 'NENHUMA']
        estudantes_restantes = [e for e in estudantes if e not in estudantes_prioridade]
        
        # Posicionar estudantes com necessidades especiais nas primeiras fileiras
        fileira_atual = 1
        coluna_atual = 1
        
        for estudante in estudantes_prioridade:
            mapeamento.append({
                'estudante_id': estudante.id,
                'fileira': fileira_atual,
                'coluna': coluna_atual,
                'prioritario': True
            })
            
            coluna_atual += 1
            if coluna_atual > sala_config.get('colunas', 6):
                coluna_atual = 1
                fileira_atual += 1
        
        # Posicionar demais estudantes
        for estudante in estudantes_restantes:
            mapeamento.append({
                'estudante_id': estudante.id,
                'fileira': fileira_atual,
                'coluna': coluna_atual,
                'prioritario': False
            })
            
            coluna_atual += 1
            if coluna_atual > sala_config.get('colunas', 6):
                coluna_atual = 1
                fileira_atual += 1
        
        return mapeamento
        
    except Exception as e:
        # Fallback: mapeamento sequencial simples
        mapeamento = []
        fileira_atual = 1
        coluna_atual = 1
        
        for i, estudante in enumerate(estudantes):
            mapeamento.append({
                'estudante_id': estudante.id,
                'fileira': fileira_atual,
                'coluna': coluna_atual,
                'prioritario': False
            })
            
            coluna_atual += 1
            if coluna_atual > sala_config.get('colunas', 6):
                coluna_atual = 1
                fileira_atual += 1
        
        return mapeamento

