# 📊 RESUMO HIPERCOMPLEXO DO SISTEMA S.U.M - Sistema Único de Mapeamento

## 🎯 VISÃO GERAL DO SISTEMA

O **S.U.M (Sistema Único de Mapeamento)** é uma plataforma educacional completa desenvolvida com arquitetura moderna, contendo:
- **Backend:** Django 4.2+ com Django REST Framework
- **Frontend:** Vue.js 3 com Composition API e TypeScript
- **Banco de Dados:** PostgreSQL 15
- **Infraestrutura:** Docker Compose com Nginx como proxy reverso
- **Autenticação:** JWT (Simple JWT)
- **IA:** Integração OpenAI para geração de atividades e otimização de mapeamentos

---

## 🏗️ ARQUITETURA TÉCNICA

### Backend Django (`backend/django-back-end/`)

#### Módulos Principais:
1. **`core/`** - Autenticação e gestão de usuários
2. **`escola/`** - Gestão escolar e instituições
3. **`estudantes/`** - Gestão de estudantes e perfis
4. **`professores/`** - Gestão de professores e dashboards
5. **`atividades/`** - Sistema de atividades e avaliações
6. **`eventos/`** - Eventos escolares e calendário
7. **`placement/`** - **MÓDULO DE MAPEAMENTO** (foco principal)
8. **`agenda/`** - Sistema de agenda e horários
9. **`setup/`** - Configurações Django

### Frontend Vue.js (`frontend/src/`)

#### Estrutura:
- **`components/classroom/`** - **12 componentes especializados em mapeamento**
- **`views/`** - Páginas principais (Dashboard, Gestão, etc.)
- **`store/`** - Pinia stores (classroom, auth, ai, etc.)
- **`composables/`** - Composables Vue (useClassroom, useAI, useAuth)
- **`services/`** - Serviços de API e comunicação backend
- **`types/`** - Definições TypeScript

---

## 🗺️ SISTEMA DE MAPEAMENTO - VISÃO GERAL COMPLETA

### 📋 MODELO DE DADOS (Backend)

#### `MapeamentoSala` - Modelo Principal
```python
Campos Principais:
- uuid (PK): Identificador único UUID
- nome: Nome do mapeamento
- escola: ForeignKey para Escola
- turma: ForeignKey para Turma
- linhas: Número de linhas da sala (padrão: 4)
- colunas: Número de colunas da sala (padrão: 5)
- tipo_agrupamento: SOLO, DUPLA, TRIO, QUARTETO, CUSTOMIZADO
- numero_pessoas_grupo: Para agrupamentos customizados
- tem_armarios: Boolean
- posicao_armarios: JSON {x, y, width, height}
- posicao_mesa_professor: JSON {x, y}
- posicao_quadro: JSON {x, y, width, height}
- objetos_adicionais: JSON Array (estantes, computadores, etc.)
- usar_sistema_lideres: Boolean
- posicionamento_lideres: JSON
- usar_ia_automatica: Boolean
- criterios_ia: JSON (considerar_dificuldades, considerar_notas, etc.)
- modo_edicao: MANUAL, AUTOMATICO, HIBRIDO
```

#### `PosicaoAluno` - Posicionamento Individual
```python
Campos:
- mapeamento: ForeignKey para MapeamentoSala
- estudante: ForeignKey para Estudante
- linha: Integer (posição na grade)
- coluna: Integer (posição na grade)
- grupo: Integer (identificação de grupo)
- fixo: Boolean (não pode ser movido)
- eh_lider: Boolean (líder estrategicamente posicionado)
- observacoes: TextField
```

### 🔧 SERVIÇOS DE IA E OTIMIZAÇÃO

#### `IAMapeamentoSala` - Serviço de IA Principal
```python
Métodos Principais:
1. organizar_automaticamente() 
   - Retorna lista de posições sugeridas
   - Aplica critérios configuráveis

2. _organizar_por_dificuldades()
   - Cria pares heterogêneos (com/sem dificuldade)
   - Prioriza alunos com dificuldade visual na frente
   
3. _organizar_por_desempenho()
   - Distribui alunos por média acadêmica
   - Coloca melhores no centro, demais nas bordas

4. _organizar_por_altura()
   - Baixos na frente, altos atrás
   - Ordem: BAIXA -> MEDIA -> ALTA

5. _organizar_com_lideres()
   - Posiciona líderes estrategicamente
   - Primeira e última linha, laterais

6. _organizar_hibrido()
   - Combina múltiplos critérios
   - Sistema de scoring:
     * Dificuldade visual: +100 pontos
     * Dificuldade aprendizado: +50 pontos
     * Altura baixa: +30 pontos
     * Líder: +200 pontos
     * Média geral: + média
   - Ordena por score e posiciona inteligentemente

7. analisar_layout_otimo()
   - Analisa características dos alunos
   - Sugere melhor tipo de agrupamento
   - Identifica prioridades de posicionamento
```

#### `OtimizadorMapeamento` - Algoritmo Genético
```python
Funcionalidades:
- Otimização usando algoritmos genéticos
- Iterações configuráveis (padrão: 100)
- Cálculo de score de qualidade:
  * Penaliza alunos com dificuldade visual longe do quadro
  * Bonifica líderes em posições estratégicas
  * Penaliza extremos (muito perto/muito longe)
- Mutação de layouts para encontrar melhores combinações
```

#### `ValidacaoMapeamento` - Validações
```python
Validações Implementadas:
- Capacidade da sala vs número de alunos
- Conflitos de posicionamento
- Regras de distanciamento
- Validação de grupos
- Verificação de posições fixas
```

#### `EstatisticasMapeamento` - Análises
```python
Estatísticas Geradas:
- Taxa de ocupação da sala
- Distribuição por grupos
- Alunos com dificuldades posicionados
- Alunos líderes estrategicamente colocados
- Percentual de capacidade utilizada
```

### 🌐 API REST - Endpoints de Mapeamento

#### URLs Disponíveis (`/api/placement/`)
```
POST   /api/placement/gerar/
       - Gera novo mapeamento automaticamente
       - Body: {turma_id, nome, linhas, colunas}
       
GET    /api/placement/atual/<uuid:uuid>/
       - Obtém mapeamento atual
       
PATCH  /api/placement/mover/
       - Move aluno para nova posição
       - Body: {estudante_id, nova_linha, nova_coluna, novo_grupo?}
       
GET    /api/placement/historico/<int:turma_id>/
       - Histórico de mapeamentos da turma
       
PATCH  /api/placement/grupo/alterar/
       - Altera grupo de um aluno
       - Body: {estudante_id, novo_grupo}
```

#### Permissões:
- `IsProfessorOrPDTOrAdmin` - Apenas professores, coordenadores ou admins

### 🎨 COMPONENTES FRONTEND - Mapeamento de Sala

#### 1. `ClassroomMap2D.vue` (692 linhas)
```vue
Funcionalidades:
- Canvas 2D para visualização de sala
- Suporte a drag-and-drop de alunos
- Modos: SOLO, DUPLA, TRIO
- Grid configurável (linhas/colunas)
- Objetos adicionais (armários, computadores, etc.)
- Sistema de cores alternadas
- Números e bordas opcionais
- Área do professor configurável
- Snap-to-grid
- Seleção múltipla (box select)
- Legendas visuais
```

#### 2. `ClassroomGrid.vue` (548 linhas)
```vue
Funcionalidades:
- Grade interativa de assentos
- Visualização em grid
- Edição de posições
- Cores por grupo
- Indicação de ocupação
```

#### 3. `ClassroomGridEditor.vue` (295 linhas)
```vue
Funcionalidades:
- Editor visual de grade
- Controles de dimensão (linhas/colunas)
- Espaçamento configurável
- Layouts predefinidos
- Preview em tempo real
```

#### 4. `ClassroomMapEditor.vue` (347 linhas)
```vue
Funcionalidades:
- Editor completo de mapeamento
- Modos de edição (manual/automático/híbrido)
- Configurações avançadas
- Validação de layout
```

#### 5. `StudentPositioner.vue` (506 linhas)
```vue
Funcionalidades:
- Posicionador estratégico de alunos
- Modos 2D e 3D
- Filtros por características
- Visualização de informações do aluno
- Salvar posições
```

#### 6. `VisibilitySimulator.vue` (355 linhas)
```vue
Funcionalidades:
- Simulador de deficiências visuais
- Tipos de simulação: Miopia, Hipermetropia, Astigmatismo, Catarata
- Intensidade ajustável (0-100%)
- Perspectiva individual por aluno
- Visualização em tempo real
```

#### 7. `StudentCard.vue` (288 linhas)
```vue
Funcionalidades:
- Card individual de aluno
- Informações: nome, foto, características
- Indicadores visuais (dificuldades, líder, etc.)
- Ações rápidas
```

#### 8. `GroupManager.vue` (513 linhas)
```vue
Funcionalidades:
- Gerenciamento de grupos
- Criação/edição/exclusão
- Atribuição de alunos
- Cores e identificação
- Estatísticas por grupo
```

#### 9. `SeatEditor.vue` (554 linhas)
```vue
Funcionalidades:
- Editor de assentos individuais
- Propriedades: status, label, grupo
- Posicionamento preciso
- Validação de conflitos
```

#### 10. `MapConfig.vue` (153 linhas)
```vue
Funcionalidades:
- Configurações do mapeamento
- Parâmetros de sala
- Opções de IA
- Templates de layout
```

#### 11. `MapToolbar.vue` (52 linhas)
```vue
Funcionalidades:
- Barra de ferramentas
- Ações rápidas
- Zoom/pan
- Modos de visualização
```

#### 12. `MapMini.vue` (62 linhas)
```vue
Funcionalidades:
- Visualização mini do mapa
- Overview da sala
- Navegação rápida
```

### 📦 STORE PINIA - `classroom.ts`

#### Estado:
```typescript
interface ClassroomState {
  students: Student[]
  groups: Group[]
  activeClassroom: Classroom | null
  isLoading: boolean
  error: string | null
  lastUpdated: Date | null
}
```

#### Actions Principais:
```typescript
- loadClassroom(classroomId): Carrega dados da sala
- updateStudentPosition(studentId, position): Atualiza posição
- createGroup(groupData): Cria novo grupo
- updateGroup(groupId, groupData): Atualiza grupo
- deleteGroup(groupId): Remove grupo
- assignStudentToGroup(studentId, groupId): Atribui aluno
- removeStudentFromGroup(studentId): Remove aluno
- saveClassroomLayout(): Salva layout completo
```

#### Getters:
```typescript
- studentCount: Número total de alunos
- groupCount: Número de grupos
- hasVisionIssues: Quantidade com problemas visuais
- studentsWithoutGroup: Alunos sem grupo
- groupsWithStudents: Grupos com listas de alunos
```

### 🎣 COMPOSABLE - `useClassroom.ts`

#### Funcionalidades:
```typescript
- loadClassroom(): Carrega dados
- optimizePlacement(): Otimiza usando IA
- createGroups(activityType, groupSize): Cria grupos com IA
- updateStudentPosition(): Atualiza posição
- createGroup(), updateGroup(), deleteGroup()
- assignStudentToGroup(), removeStudentFromGroup()
- saveClassroomLayout(): Salva tudo
- getStudentById(), getGroupById()
```

#### Integração com IA:
```typescript
- Usa useAI() para gerar prompts
- Cria grupos baseados em atividade
- Otimiza posicionamento considerando:
  * Problemas de visão
  * Estilos de aprendizagem
  * Notas e habilidades
  * Dificuldades de aprendizado
```

---

## 🤖 INTEGRAÇÃO COM IA

### Backend (`placement/ia.py`)
- Integração OpenAI para geração inteligente
- Função: `gerar_mapeamento_inteligente(estudantes, sala_config)`

### Frontend (`composables/useAI.ts`)
- Composable para interação com IA
- Geração de atividades
- Otimização de mapeamentos
- Criação inteligente de grupos

---

## 📊 CARACTERÍSTICAS AVANÇADAS DO MAPEAMENTO

### 1. Sistema de Agrupamento
- **SOLO**: Assentos individuais
- **DUPLA**: Grupos de 2
- **TRIO**: Grupos de 3
- **QUARTETO**: Grupos de 4
- **CUSTOMIZADO**: Número configurável

### 2. Sistema de Líderes
- Identificação de líderes
- Posicionamento estratégico automático
- Distribuição inteligente

### 3. Consideração de Dificuldades
- **Visão**: MEDIA, ALTA → Prioridade nas primeiras fileiras
- **Aprendizado**: MODERADA, SEVERA → Pares heterogêneos
- **Altura**: BAIXA → Frente da sala

### 4. Modos de Edição
- **MANUAL**: Drag-and-drop livre
- **AUTOMATICO**: IA organiza tudo
- **HIBRIDO**: Combina manual + IA

### 5. Objetos Físicos na Sala
- Armários (posição configurável)
- Mesa do professor (posição configurável)
- Quadro (posição e dimensões)
- Objetos adicionais (estantes, computadores, etc.)

### 6. Templates de Layout
- **retangular**: 4x5 padrão
- **em_ferradura**: 3x6 com duplas
- **laboratorio**: 5x6 com trios
- **auditorio**: 6x8 individual

### 7. Histórico e Versionamento
- `simple_history` para histórico de mudanças
- Diferentes versões de mapeamentos
- Possibilidade de duplicar layouts

### 8. Validações Inteligentes
- Capacidade vs número de alunos
- Conflitos de posicionamento
- Validação de limites
- Posições fixas protegidas
- Verificação de grupos

### 9. Estatísticas e Análises
- Taxa de ocupação
- Distribuição por grupos
- Alunos com dificuldades posicionados
- Percentual de utilização
- Análise de layout ótimo

### 10. Simulador de Visão
- Simulação de deficiências visuais
- Múltiplos tipos (Miopia, Hipermetropia, etc.)
- Intensidade ajustável
- Perspectiva individual por aluno

---

## 🔐 SEGURANÇA E PERMISSÕES

### Níveis de Acesso:
1. **Admin**: Acesso total
2. **PDT (Coordenador)**: Gestão de turmas e mapeamentos
3. **Professor**: Criação e edição de mapeamentos próprios
4. **Aluno**: Visualização apenas

### Validações:
- Permissões por endpoint
- Validação de propriedade (professor só edita suas turmas)
- Autenticação JWT obrigatória

---

## 🗄️ BANCO DE DADOS

### PostgreSQL 15
- Encoding: UTF-8
- Locale: pt_BR.UTF-8
- Timezone: America/Sao_Paulo

### Estrutura Relacional:
```
Escola
  └── Turma
        └── Estudante
        └── MapeamentoSala
              └── PosicaoAluno (estudante + linha/coluna)
```

### Indexes:
- `turma` no MapeamentoSala
- `escola` no MapeamentoSala
- `mapeamento` no PosicaoAluno

### Unique Constraints:
- `(turma, nome)` no MapeamentoSala
- `(mapeamento, estudante)` no PosicaoAluno
- `(mapeamento, linha, coluna)` no PosicaoAluno

---

## 🚀 INFRAESTRUTURA DOCKER

### Serviços:
1. **PostgreSQL**: Banco de dados
2. **Backend Django**: API REST (Gunicorn)
3. **Frontend Vue.js**: Aplicação (Vite dev server)
4. **Nginx**: Proxy reverso e load balancing

### Portas:
- Frontend: `5173`
- Backend: `8000`
- Nginx: `80` (proxy)
- PostgreSQL: `5432`

---

## 📈 FLUXO DE TRABALHO TÍPICO

### 1. Criação de Mapeamento:
```
Professor → Seleciona Turma → Define Dimensões → 
Escolhe Tipo Agrupamento → Configura IA → 
Gera Automaticamente (ou Manual)
```

### 2. Edição Manual:
```
Abre Mapeamento → ClassroomMap2D → 
Drag-and-Drop Alunos → Valida → Salva
```

### 3. Otimização com IA:
```
Abre Mapeamento → Clica "Otimizar" → 
IA Analisa Características → 
Aplica Algoritmo → Mostra Resultado → 
Professor Aprova/Rejeita
```

### 4. Criação de Grupos:
```
Define Tipo Atividade → Define Tamanho Grupo → 
IA Analisa Alunos → Cria Grupos Equilibrados → 
Professor Ajusta → Salva
```

---

## 🎯 CASOS DE USO PRINCIPAIS

### 1. Mapeamento Automático por Dificuldades
- Sistema identifica alunos com problemas visuais
- Coloca nas primeiras fileiras automaticamente
- Cria pares heterogêneos para apoio

### 2. Organização por Desempenho
- Distribui alunos com notas altas/baixas
- Cria grupos equilibrados para atividades

### 3. Posicionamento Estratégico de Líderes
- Identifica líderes da turma
- Posiciona estrategicamente (laterais, frente/fundo)
- Facilita liderança em grupos

### 4. Simulação de Acessibilidade
- Professor testa visibilidade de diferentes posições
- Simula deficiências visuais
- Garante que todos vejam o quadro adequadamente

### 5. Otimização Contínua
- Sistema sugere melhorias no layout
- Aplica algoritmos genéticos
- Compara scores e otimiza

---

## 📝 TECNOLOGIAS E BIBLIOTECAS PRINCIPAIS

### Backend:
- Django 4.2+
- Django REST Framework
- Simple JWT
- Simple History (versionamento)
- PostgreSQL adapter (psycopg2)
- Gunicorn (WSGI server)

### Frontend:
- Vue.js 3 (Composition API)
- TypeScript
- Pinia (state management)
- Vue Router 4
- Axios (HTTP client)
- Tailwind CSS
- Vite (build tool)

### DevOps:
- Docker & Docker Compose
- Nginx (reverse proxy)
- PostgreSQL 15

---

## 🔮 FUNCIONALIDADES FUTURAS (Identificadas no Código)

### Já Implementadas mas Pode Expandir:
1. **3D Visualization** - Mencionado no StudentPositioner
2. **Templates Avançados** - Sistema básico implementado
3. **Analytics Avançados** - Estatísticas básicas funcionando
4. **Exportação** - Não identificado, mas seria útil
5. **Impressão** - Não identificado, mas seria útil

---

## ✅ ESTADO ATUAL DO SISTEMA

### ✅ Funcionalidades Completas:
- ✅ Modelo de dados robusto
- ✅ API REST completa
- ✅ Componentes frontend funcionais
- ✅ Integração com IA
- ✅ Sistema de agrupamento
- ✅ Simulador de visão
- ✅ Validações e segurança
- ✅ Histórico e versionamento
- ✅ Múltiplos algoritmos de IA
- ✅ Docker containerizado

### 🔄 Áreas para Melhoria (Observações):
1. **Documentação da API**: Faltam docs Swagger/OpenAPI
2. **Testes**: Não identificados testes unitários/integração
3. **Performance**: Pode precisar otimização para grandes turmas
4. **UI/UX**: Componentes funcionais mas podem ser refinados
5. **Exportação/Impressão**: Não implementado

---

## 📊 MÉTRICAS DO CÓDIGO

### Backend Placement:
- `models.py`: ~410 linhas
- `services.py`: ~560 linhas (lógica complexa de IA)
- `views.py`: ~70 linhas
- `serializers.py`: ~35 linhas
- `urls.py`: ~17 linhas

### Frontend Classroom:
- Total: **12 componentes**
- Linhas de código: **~4.000+ linhas**
- Componente maior: `ClassroomMap2D.vue` (692 linhas)

---

## 🎓 CONCLUSÃO

O sistema de mapeamento está **altamente desenvolvido e funcional**, com:
- ✅ Arquitetura sólida e escalável
- ✅ Integração robusta frontend/backend
- ✅ Múltiplos algoritmos de IA
- ✅ Interface rica e interativa
- ✅ Segurança e validações adequadas
- ✅ Suporte a casos de uso complexos

O sistema está **pronto para produção** com possíveis melhorias incrementais em documentação, testes e performance.

---

**Documento gerado automaticamente**  
**Última atualização:** Baseado na análise do código atual do repositório

