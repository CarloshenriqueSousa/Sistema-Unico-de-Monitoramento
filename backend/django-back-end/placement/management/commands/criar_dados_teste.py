# placement/management/commands/criar_dados_teste.py
"""
Comando Django para criar dados de teste no banco SQLite
Uso: python manage.py criar_dados_teste
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import User
from escola.models import Escola, Turma
from estudantes.models import Estudante
from placement.models import MapeamentoSala, PosicaoAluno, TemplatesSala
from django.utils import timezone
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria dados de teste para o sistema de mapeamento (SQLite)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Criando dados de teste...'))
        
        # Limpar dados existentes (opcional - comentar se quiser manter)
        # self.limpar_dados()
        
        # 1. Criar Usuários
        self.stdout.write('📝 Criando usuários...')
        escola_user = self.criar_usuario('escola', 'Escola Teste', 'escola@teste.com', 'escola123', 'escola')
        professor_user = self.criar_usuario('prof', 'Professor Teste', 'prof@teste.com', 'prof123', 'professor')
        alunos_users = self.criar_alunos()
        
        # 2. Criar Escola
        self.stdout.write('🏫 Criando escola...')
        escola = self.criar_escola(escola_user)
        
        # 3. Criar Turma
        self.stdout.write('👥 Criando turma...')
        turma = self.criar_turma(escola)
        
        # 4. Criar Estudantes
        self.stdout.write('🎓 Criando estudantes...')
        estudantes = self.criar_estudantes(alunos_users, turma)
        
        # 5. Criar Templates de Sala
        self.stdout.write('📐 Criando templates de sala...')
        self.criar_templates()
        
        # 6. Criar Mapeamento de Teste
        self.stdout.write('🗺️  Criando mapeamento de teste...')
        mapeamento = self.criar_mapeamento(turma, escola)
        
        # 7. Posicionar alguns alunos
        self.stdout.write('📍 Posicionando alunos...')
        self.posicionar_alunos(mapeamento, estudantes)
        
        self.stdout.write(self.style.SUCCESS('✅ Dados de teste criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Resumo:'))
        self.stdout.write(self.style.SUCCESS(f'   - Usuários criados: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Estudantes criados: {Estudante.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Mapeamentos criados: {MapeamentoSala.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Templates criados: {TemplatesSala.objects.count()}'))
        
        self.stdout.write(self.style.WARNING('\n🔑 Credenciais de teste:'))
        self.stdout.write(self.style.WARNING(f'   Escola: escola / escola123'))
        self.stdout.write(self.style.WARNING(f'   Professor: prof / prof123'))
        self.stdout.write(self.style.WARNING(f'   Alunos: aluno1, aluno2, etc. / senha123'))

    def criar_usuario(self, identifier, nome, email, password, user_type='escola'):
        user, created = User.objects.get_or_create(
            identifier=identifier,
            defaults={
                'nome': nome,
                'email': email,
                'user_type': user_type,
                'is_active': True
            }
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f'   ✓ Usuário {identifier} criado')
        else:
            self.stdout.write(f'   - Usuário {identifier} já existe')
        return user

    def criar_alunos(self):
        alunos_users = []
        nomes_alunos = [
            'João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Lima', 'Carlos Souza',
            'Julia Oliveira', 'Lucas Pereira', 'Fernanda Alves', 'Rafael Martins', 'Mariana Rocha',
            'Gabriel Ferreira', 'Isabela Gomes', 'Bruno Rodrigues', 'Camila Barbosa', 'Diego Araujo',
            'Larissa Dias', 'Felipe Monteiro', 'Beatriz Cardoso', 'Thiago Ribeiro', 'Carolina Nunes'
        ]
        
        for i, nome in enumerate(nomes_alunos, 1):
            identifier = f'aluno{i}'
            email = f'aluno{i}@teste.com'
            user, created = User.objects.get_or_create(
                identifier=identifier,
                defaults={
                    'nome': nome,
                    'email': email,
                    'user_type': 'aluno',
                    'is_active': True
                }
            )
            if created:
                user.set_password('senha123')
                user.save()
            alunos_users.append(user)
        
        return alunos_users

    def criar_escola(self, usuario):
        escola, created = Escola.objects.get_or_create(
            usuario=usuario,
            defaults={
                'cnpj': '12345678000190',
                'nome': 'Escola Estadual Teste',
                'endereco': 'Rua Teste, 123 - São Paulo, SP'
            }
        )
        return escola

    def criar_turma(self, escola):
        turma, created = Turma.objects.get_or_create(
            escola=escola,
            nome='3º Ano A',
            defaults={
                'ano': 3,
                'capacidade': 30
            }
        )
        return turma

    def criar_estudantes(self, usuarios_alunos, turma):
        estudantes = []
        dificuldades_aprendizado = ['NENHUMA', 'LEVE', 'MODERADA', 'SEVERA']
        dificuldades_visao = ['NENHUMA', 'BAIXA', 'MEDIA', 'ALTA']
        alturas = ['BAIXA', 'MEDIA', 'ALTA']
        
        for i, usuario in enumerate(usuarios_alunos):
            # Alguns alunos terão dificuldades
            dificuldade_aprendizado = random.choice(dificuldades_aprendizado) if i < 5 else 'NENHUMA'
            dificuldade_visao = random.choice(dificuldades_visao) if i < 3 else 'NENHUMA'
            altura = random.choice(alturas)
            eh_lider = i < 4  # Primeiros 4 são líderes
            
            # Médias acadêmicas simuladas
            media_humanas = round(random.uniform(6.0, 10.0), 2)
            media_linguagens = round(random.uniform(6.0, 10.0), 2)
            media_exatas = round(random.uniform(6.0, 10.0), 2)
            
            estudante, created = Estudante.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'turma': turma,
                    'dificuldade_aprendizado': dificuldade_aprendizado,
                    'dificuldade_visao': dificuldade_visao,
                    'altura': altura,
                    'eh_lider': eh_lider,
                    'media_humanas': media_humanas,
                    'media_linguagens': media_linguagens,
                    'media_exatas': media_exatas,
                    'cargo_lideranca': 'Líder de Grupo' if eh_lider else None,
                    'data_nomeacao_lider': timezone.now() if eh_lider else None
                }
            )
            if not created:
                # Atualizar dados existentes
                estudante.dificuldade_aprendizado = dificuldade_aprendizado
                estudante.dificuldade_visao = dificuldade_visao
                estudante.altura = altura
                estudante.eh_lider = eh_lider
                estudante.media_humanas = media_humanas
                estudante.media_linguagens = media_linguagens
                estudante.media_exatas = media_exatas
                estudante.save()
            estudantes.append(estudante)
        
        return estudantes

    def criar_templates(self):
        templates_data = [
            {
                'nome': 'Sala Tradicional',
                'tipo_sala': 'NORMAL',
                'descricao': 'Layout clássico em fileiras - Ideal para aulas expositivas',
                'config': {
                    'fileiras_verticais': 5,
                    'fileiras_horizontais': 6,
                    'alunos_por_grupo': 1,
                    'tipo_sala': 'NORMAL',
                    'layout_config': {
                        'espacamento_horizontal': 60,
                        'espacamento_vertical': 80,
                        'largura_assento': 40,
                        'altura_assento': 40
                    },
                    'objetos_sala': [
                        {
                            'id': 'quadro_1',
                            'tipo': 'quadro',
                            'x': 300,
                            'y': 20,
                            'width': 400,
                            'height': 200,
                            'rotacao': 0,
                            'label': 'Quadro',
                            'cor': '#1e293b'
                        },
                        {
                            'id': 'mesa_prof_1',
                            'tipo': 'mesa_professor',
                            'x': 450,
                            'y': 240,
                            'width': 100,
                            'height': 60,
                            'rotacao': 0,
                            'label': 'Professor',
                            'cor': '#d97706'
                        }
                    ],
                    'cor_fundo': '#f5f5f5',
                    'mostrar_grade': True,
                    'mostrar_numeros': True
                }
            },
            {
                'nome': 'Laboratório de Informática',
                'tipo_sala': 'LABORATORIO',
                'descricao': 'Duplas com computadores - Perfeito para aulas práticas',
                'config': {
                    'fileiras_verticais': 4,
                    'fileiras_horizontais': 6,
                    'alunos_por_grupo': 2,
                    'tipo_sala': 'LABORATORIO',
                    'layout_config': {
                        'espacamento_horizontal': 80,
                        'espacamento_vertical': 90,
                        'largura_assento': 45,
                        'altura_assento': 40
                    },
                    'objetos_sala': [
                        {
                            'id': 'quadro_1',
                            'tipo': 'quadro',
                            'x': 350,
                            'y': 20,
                            'width': 300,
                            'height': 150,
                            'rotacao': 0,
                            'label': 'Quadro',
                            'cor': '#1e293b'
                        }
                    ],
                    'cor_fundo': '#fafafa',
                    'mostrar_grade': True,
                    'mostrar_numeros': True
                }
            },
            {
                'nome': 'Sala de Leitura',
                'tipo_sala': 'BIBLIOTECA',
                'descricao': 'Grupos de 4 - Ideal para trabalhos colaborativos',
                'config': {
                    'fileiras_verticais': 3,
                    'fileiras_horizontais': 4,
                    'alunos_por_grupo': 4,
                    'tipo_sala': 'BIBLIOTECA',
                    'layout_config': {
                        'espacamento_horizontal': 100,
                        'espacamento_vertical': 100,
                        'largura_assento': 40,
                        'altura_assento': 40
                    },
                    'objetos_sala': [
                        {
                            'id': 'estante_1',
                            'tipo': 'estante',
                            'x': 50,
                            'y': 100,
                            'width': 80,
                            'height': 400,
                            'rotacao': 0,
                            'label': 'Livros',
                            'cor': '#78350f'
                        },
                        {
                            'id': 'mesa_prof',
                            'tipo': 'mesa_professor',
                            'x': 550,
                            'y': 50,
                            'width': 100,
                            'height': 60,
                            'rotacao': 0,
                            'label': 'Professor',
                            'cor': '#d97706'
                        }
                    ],
                    'cor_fundo': '#fef3c7',
                    'mostrar_grade': False,
                    'mostrar_numeros': False
                }
            },
            {
                'nome': 'Auditório',
                'tipo_sala': 'AUDITORIO',
                'descricao': 'Formato teatro - Para palestras e apresentações',
                'config': {
                    'fileiras_verticais': 8,
                    'fileiras_horizontais': 10,
                    'alunos_por_grupo': 1,
                    'tipo_sala': 'AUDITORIO',
                    'layout_config': {
                        'espacamento_horizontal': 50,
                        'espacamento_vertical': 60,
                        'largura_assento': 35,
                        'altura_assento': 35
                    },
                    'objetos_sala': [
                        {
                            'id': 'palco',
                            'tipo': 'custom',
                            'x': 200,
                            'y': 20,
                            'width': 800,
                            'height': 150,
                            'rotacao': 0,
                            'label': 'Palco',
                            'cor': '#78350f'
                        }
                    ],
                    'cor_fundo': '#1e293b',
                    'mostrar_grade': False,
                    'mostrar_numeros': True
                }
            }
        ]
        
        for template_data in templates_data:
            template, created = TemplatesSala.objects.get_or_create(
                nome=template_data['nome'],
                defaults={
                    'tipo_sala': template_data['tipo_sala'],
                    'descricao': template_data['descricao'],
                    'config': template_data['config'],
                    'publico': True
                }
            )
            if created:
                self.stdout.write(f'   ✓ Template {template.nome} criado')

    def criar_mapeamento(self, turma, escola):
        mapeamento, created = MapeamentoSala.objects.get_or_create(
            nome='Mapeamento Teste',
            turma=turma,
            defaults={
                'escola': escola,
                'fileiras_verticais': 5,
                'fileiras_horizontais': 6,
                'alunos_por_grupo': 1,
                'tipo_sala': 'NORMAL',
                'layout_config': {
                    'espacamento_horizontal': 60,
                    'espacamento_vertical': 80,
                    'largura_assento': 40,
                    'altura_assento': 40
                },
                'objetos_sala': [
                    {
                        'id': 'quadro_1',
                        'tipo': 'quadro',
                        'x': 300,
                        'y': 20,
                        'width': 400,
                        'height': 200,
                        'rotacao': 0,
                        'label': 'Quadro',
                        'cor': '#1e293b'
                    },
                    {
                        'id': 'mesa_prof_1',
                        'tipo': 'mesa_professor',
                        'x': 450,
                        'y': 240,
                        'width': 100,
                        'height': 60,
                        'rotacao': 0,
                        'label': 'Professor',
                        'cor': '#d97706'
                    }
                ],
                'cor_fundo': '#f5f5f5',
                'mostrar_grade': True,
                'mostrar_numeros': True,
                'ativo': True,
                'criterios_ia': {
                    'considerar_dificuldades': True,
                    'considerar_notas': False,
                    'considerar_altura': True,
                    'considerar_lideranca': True
                }
            }
        )
        return mapeamento

    def posicionar_alunos(self, mapeamento, estudantes):
        # Limpar posições existentes para este mapeamento
        PosicaoAluno.objects.filter(mapeamento=mapeamento).delete()
        
        # Posicionar alguns alunos de exemplo (primeiros 15)
        linhas = mapeamento.fileiras_verticais or 5
        colunas = mapeamento.fileiras_horizontais or 6
        
        alunos_posicionar = estudantes[:15]  # Posicionar 15 alunos
        
        for i, estudante in enumerate(alunos_posicionar):
            linha = i // colunas
            coluna = i % colunas
            
            # Garantir que não excede limites
            if linha >= linhas:
                continue
            
            # Calcular grupo
            alunos_por_grupo = mapeamento.alunos_por_grupo or 1
            numero_grupo = i // alunos_por_grupo if alunos_por_grupo > 1 else None
            posicao_no_grupo = i % alunos_por_grupo if alunos_por_grupo > 1 else 0
            
            PosicaoAluno.objects.create(
                mapeamento=mapeamento,
                estudante=estudante,
                linha=linha,
                coluna=coluna,
                numero_grupo=numero_grupo,
                posicao_no_grupo=posicao_no_grupo,
                eh_lider=estudante.eh_lider
            )
        
        self.stdout.write(f'   ✓ {len(alunos_posicionar)} alunos posicionados')

