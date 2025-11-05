<template>
  <div class="teacher-classroom-editor min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white px-6 py-4 shadow-lg">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button 
            @click="$router.back()"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold">{{ mapeamentoAtual?.nome || 'Novo Mapeamento' }}</h1>
            <p class="text-white/70 text-sm">{{ mapeamentoAtual?.turma?.nome || '' }}</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="organizarAutomatico"
            :disabled="loading"
            class="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Organizar Automaticamente
          </button>
          <button
            @click="salvarMapeamento"
            :disabled="loading"
            class="px-6 py-2 rounded-lg bg-white text-[#2d531a] font-semibold hover:bg-gray-100 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Salvar Mapeamento
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto p-6">
      <div class="grid grid-cols-12 gap-6">
        <!-- Sidebar de Configurações -->
        <aside class="col-span-12 lg:col-span-3 space-y-4">
          <!-- Configuração da Sala -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Configuração da Sala</h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nome do Mapeamento</label>
                <input
                  v-model="config.nome"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent"
                  placeholder="Ex: Mapeamento Semestre 1"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Sala</label>
                <select
                  v-model="config.tipo_sala"
                  @change="aplicarTemplate"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent"
                >
                  <option value="NORMAL">Sala Normal</option>
                  <option value="LABORATORIO">Laboratório</option>
                  <option value="BIBLIOTECA">Biblioteca</option>
                  <option value="AUDITORIO">Auditório</option>
                  <option value="CUSTOMIZADO">Customizado</option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Linhas</label>
                  <input
                    v-model.number="config.fileiras_verticais"
                    type="number"
                    min="1"
                    max="20"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Colunas</label>
                  <input
                    v-model.number="config.fileiras_horizontais"
                    type="number"
                    min="1"
                    max="20"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Alunos por Grupo</label>
                <input
                  v-model.number="config.alunos_por_grupo"
                  type="number"
                  min="1"
                  max="6"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent"
                />
                <p class="text-xs text-gray-500 mt-1">1 = Individual, 2 = Dupla, 3 = Trio, etc.</p>
              </div>

              <div class="flex items-center gap-2">
                <input
                  v-model="config.mostrar_grade"
                  type="checkbox"
                  id="mostrar-grade"
                  class="w-4 h-4 text-[#2d531a] rounded focus:ring-[#2d531a]"
                />
                <label for="mostrar-grade" class="text-sm text-gray-700">Mostrar Grade</label>
              </div>

              <div class="flex items-center gap-2">
                <input
                  v-model="config.mostrar_numeros"
                  type="checkbox"
                  id="mostrar-numeros"
                  class="w-4 h-4 text-[#2d531a] rounded focus:ring-[#2d531a]"
                />
                <label for="mostrar-numeros" class="text-sm text-gray-700">Mostrar Números</label>
              </div>
            </div>
          </div>

          <!-- Lista de Alunos -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-800">Alunos</h3>
              <span class="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                {{ estudantesDisponiveis.length }} disponíveis
              </span>
            </div>

            <input
              v-model="searchStudent"
              type="text"
              placeholder="Buscar aluno..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d531a] focus:border-transparent mb-3"
            />

            <div class="space-y-2 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              <div
                v-for="estudante in estudantesFiltrados"
                :key="estudante.id"
                draggable="true"
                @dragstart="onDragStart($event, estudante)"
                class="p-3 border border-gray-200 rounded-lg hover:border-[#2d531a] hover:bg-[#2d531a]/5 cursor-move transition-all flex items-center gap-3"
              >
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold text-sm flex-shrink-0"
                  :class="estudante.dificuldade_visao && estudante.dificuldade_visao !== 'NENHUMA' ? 'bg-purple-500' : 'bg-[#2d531a]'"
                >
                  {{ getInitials(estudante.usuario.nome) }}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-800 truncate">{{ estudante.usuario.nome }}</p>
                  <div class="flex items-center gap-2 mt-1">
                    <span v-if="estudante.dificuldade_visao && estudante.dificuldade_visao !== 'NENHUMA'" class="text-xs text-purple-600">
                      👁️ Visão
                    </span>
                    <span v-if="estudante.eh_lider" class="text-xs text-amber-600">
                      👑 Líder
                    </span>
                  </div>
                </div>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>

              <div v-if="estudantesFiltrados.length === 0" class="text-center py-8 text-gray-500 text-sm">
                Nenhum aluno encontrado
              </div>
            </div>
          </div>

          <!-- Objetos da Sala -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Objetos da Sala</h3>
            
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="obj in objetosDisponiveis"
                :key="obj.tipo"
                @click="adicionarObjeto(obj.tipo)"
                class="p-3 border border-gray-200 rounded-lg hover:border-[#2d531a] hover:bg-[#2d531a]/5 transition-all flex flex-col items-center gap-2"
              >
                <span class="text-2xl">{{ obj.icon }}</span>
                <span class="text-xs text-gray-700 text-center">{{ obj.label }}</span>
              </button>
            </div>
          </div>
        </aside>

        <!-- Área de Edição (Canvas) -->
        <main class="col-span-12 lg:col-span-9">
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <!-- Toolbar -->
            <div class="flex items-center justify-between mb-4 pb-4 border-b border-gray-200">
              <div class="flex items-center gap-3">
                <button
                  @click="currentTool = 'select'"
                  :class="['p-2 rounded-lg transition-colors', currentTool === 'select' ? 'bg-[#2d531a] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7 19l4-9m1 1l-9 4" />
                  </svg>
                </button>
                <button
                  @click="currentTool = 'move'"
                  :class="['p-2 rounded-lg transition-colors', currentTool === 'move' ? 'bg-[#2d531a] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200']"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                  </svg>
                </button>
              </div>

              <div class="flex items-center gap-3">
                <button
                  @click="zoom = Math.max(0.5, zoom - 0.1)"
                  class="p-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
                  </svg>
                </button>
                <span class="text-sm text-gray-700 min-w-[50px] text-center">{{ Math.round(zoom * 100) }}%</span>
                <button
                  @click="zoom = Math.min(2, zoom + 0.1)"
                  class="p-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7" />
                  </svg>
                </button>
                <button
                  @click="zoom = 1"
                  class="px-3 py-2 text-sm rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  Reset
                </button>
              </div>
            </div>

            <!-- Canvas -->
            <div
              ref="canvasWrapper"
              class="relative bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 overflow-hidden"
              :style="{ height: '700px' }"
              @drop.prevent="handleDrop"
              @dragover.prevent
            >
              <ClassroomMapCanvas
                :config="config"
                :positions="posicoes"
                :objects="objetos"
                :editable="true"
                :current-tool="currentTool"
                :zoom="zoom"
                @position-change="onPositionChange"
                @object-move="onObjectMove"
                @object-select="onObjectSelect"
                @drop="onDrop"
              />

              <!-- Stats -->
              <div class="absolute bottom-4 right-4 bg-white border border-gray-200 rounded-lg p-3 shadow-lg">
                <div class="space-y-1 text-sm">
                  <div class="flex items-center justify-between gap-4">
                    <span class="text-gray-600">Posicionados:</span>
                    <span class="font-bold text-[#2d531a]">{{ posicoes.length }}</span>
                  </div>
                  <div class="flex items-center justify-between gap-4">
                    <span class="text-gray-600">Disponíveis:</span>
                    <span class="font-bold text-[#0f1e3f]">{{ estudantesDisponiveis.length }}</span>
                  </div>
                  <div class="flex items-center justify-between gap-4">
                    <span class="text-gray-600">Ocupação:</span>
                    <span class="font-bold" :class="taxaOcupacao >= 80 ? 'text-green-600' : 'text-amber-600'">
                      {{ Math.round(taxaOcupacao) }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-[#2d531a] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-700 font-medium">Processando...</p>
      </div>
    </div>

    <!-- Error Toast -->
    <div
      v-if="error"
      class="fixed bottom-4 right-4 bg-red-500 text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 z-50"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
      <span>{{ error }}</span>
      <button @click="store.clearError()" class="ml-4 hover:bg-red-600 rounded p-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePlacementStore } from '@/store/placementStore'
import { classroomApi } from '@/services/classroomApi'
import ClassroomMapCanvas from '@/components/classroom/ClassroomMapCanvas.vue'
import type { Estudante, ObjetoSala, PosicaoAluno, TipoSala, TipoObjeto } from '@/types/classroom'

const route = useRoute()
const router = useRouter()
const store = usePlacementStore()

const uuid = route.params.uuid as string
const turmaId = route.query.turma_id as string

const config = ref({
  nome: '',
  tipo_sala: 'NORMAL' as TipoSala,
  fileiras_verticais: 5,
  fileiras_horizontais: 6,
  alunos_por_grupo: 1,
  mostrar_grade: true,
  mostrar_numeros: true,
  cor_fundo: '#f5f5f5'
})

const searchStudent = ref('')
const currentTool = ref<'select' | 'move'>('select')
const zoom = ref(1)
const selectedObject = ref<ObjetoSala | null>(null)
const canvasWrapper = ref<HTMLElement>()

const loading = computed(() => store.loading)
const error = computed(() => store.error)
const mapeamentoAtual = computed(() => store.mapeamentoAtual)
const posicoes = computed(() => store.posicoes)
const objetos = computed(() => store.objetos)
const estudantes = computed(() => store.estudantes)
const estudantesDisponiveis = computed(() => store.estudantesDisponiveis)
const taxaOcupacao = computed(() => store.taxaOcupacao)

const estudantesFiltrados = computed(() => {
  if (!searchStudent.value) return estudantesDisponiveis.value
  return estudantesDisponiveis.value.filter(e =>
    e.usuario.nome.toLowerCase().includes(searchStudent.value.toLowerCase())
  )
})

const objetosDisponiveis = [
  { tipo: 'cadeira_professor' as TipoObjeto, icon: '🪑', label: 'Cadeira Professor' },
  { tipo: 'mesa_professor' as TipoObjeto, icon: '🗄️', label: 'Mesa Professor' },
  { tipo: 'armario' as TipoObjeto, icon: '🚪', label: 'Armário' },
  { tipo: 'computador' as TipoObjeto, icon: '💻', label: 'Computador' },
  { tipo: 'estante' as TipoObjeto, icon: '📚', label: 'Estante' },
  { tipo: 'quadro' as TipoObjeto, icon: '⬛', label: 'Quadro' },
]

// Métodos
const getInitials = (nome: string) => {
  return nome.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const onDragStart = (event: DragEvent, estudante: Estudante) => {
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('student', JSON.stringify(estudante))
  }
}

const handleDrop = (event: DragEvent) => {
  // O drag-and-drop é tratado pelo componente ClassroomMapCanvas
  // Este método apenas recebe os eventos se necessário
}

const onDrop = (event: { linha: number; coluna: number; student: Estudante }) => {
  const alunosPorGrupo = config.value.alunos_por_grupo || 1
  
  // Calcula grupo
  let numero_grupo: number | null = null
  let posicao_no_grupo = 0
  
  if (alunosPorGrupo > 1) {
    const assentosPorLinha = config.value.fileiras_horizontais || 6
    const assentoIndex = event.linha * assentosPorLinha + event.coluna
    numero_grupo = Math.floor(assentoIndex / alunosPorGrupo)
    posicao_no_grupo = assentoIndex % alunosPorGrupo
  }
  
  store.adicionarPosicao({
    estudante_id: event.student.id,
    linha: event.linha,
    coluna: event.coluna,
    numero_grupo,
    posicao_no_grupo
  })
}

const adicionarObjeto = (tipo: TipoObjeto) => {
  const labels: Record<TipoObjeto, string> = {
    'cadeira_professor': 'Cadeira Professor',
    'mesa_professor': 'Mesa Professor',
    'armario': 'Armário',
    'computador': 'Computador',
    'estante': 'Estante',
    'quadro': 'Quadro',
    'custom': 'Objeto Customizado'
  }
  
  const cores: Record<TipoObjeto, string> = {
    'cadeira_professor': '#d97706',
    'mesa_professor': '#d97706',
    'armario': '#4b5563',
    'computador': '#1f2937',
    'estante': '#78350f',
    'quadro': '#1e293b',
    'custom': '#64748b'
  }
  
  const novoObjeto: ObjetoSala = {
    id: `obj_${Date.now()}`,
    tipo,
    x: 100,
    y: 100,
    width: tipo === 'quadro' ? 200 : 60,
    height: tipo === 'quadro' ? 120 : 60,
    rotacao: 0,
    label: labels[tipo] || tipo,
    cor: cores[tipo] || '#64748b'
  }
  
  store.adicionarObjeto(novoObjeto)
}

const aplicarTemplate = () => {
  const templates: Record<TipoSala, Partial<typeof config.value>> = {
    NORMAL: { fileiras_verticais: 5, fileiras_horizontais: 6, alunos_por_grupo: 1 },
    LABORATORIO: { fileiras_verticais: 4, fileiras_horizontais: 8, alunos_por_grupo: 2 },
    BIBLIOTECA: { fileiras_verticais: 3, fileiras_horizontais: 4, alunos_por_grupo: 4 },
    AUDITORIO: { fileiras_verticais: 8, fileiras_horizontais: 10, alunos_por_grupo: 1 },
    CUSTOMIZADO: {}
  }
  
  const template = templates[config.value.tipo_sala]
  if (template) {
    Object.assign(config.value, template)
  }
}

const onPositionChange = (posicao: PosicaoAluno) => {
  store.atualizarPosicao(posicao.estudante_id, posicao)
}

const onObjectMove = (id: string, x: number, y: number) => {
  store.atualizarObjeto(id, { x, y })
}

const onObjectSelect = (obj: ObjetoSala) => {
  selectedObject.value = obj
}

const salvarMapeamento = async () => {
  if (!mapeamentoAtual.value?.uuid) {
    // Criar novo
    const novoMapeamento = await store.criarMapeamento({
      ...config.value,
      turma_id: parseInt(turmaId || '0')
    })
    if (novoMapeamento?.uuid) {
      await store.salvarMapeamento()
      router.push({ name: 'professor-classroom-editor', params: { uuid: novoMapeamento.uuid } })
    }
  } else {
    // Atualizar existente
    await store.salvarMapeamento()
  }
}

const organizarAutomatico = async () => {
  if (!mapeamentoAtual.value?.uuid) return
  await store.organizarAutomatico()
}

onMounted(async () => {
  if (uuid && uuid !== 'novo') {
    await store.carregarMapeamento(uuid)
    if (store.mapeamentoAtual) {
      config.value = {
        nome: store.mapeamentoAtual.nome || '',
        tipo_sala: store.mapeamentoAtual.tipo_sala || 'NORMAL',
        fileiras_verticais: store.mapeamentoAtual.fileiras_verticais || 5,
        fileiras_horizontais: store.mapeamentoAtual.fileiras_horizontais || 6,
        alunos_por_grupo: store.mapeamentoAtual.alunos_por_grupo || 1,
        mostrar_grade: store.mapeamentoAtual.mostrar_grade ?? true,
        mostrar_numeros: store.mapeamentoAtual.mostrar_numeros ?? true,
        cor_fundo: store.mapeamentoAtual.cor_fundo || '#f5f5f5'
      }
    }
  }
  
  if (turmaId) {
    await store.carregarEstudantes(parseInt(turmaId))
  }
})

watch(() => store.mapeamentoAtual, (novo) => {
  if (novo) {
    config.value = {
      nome: novo.nome || '',
      tipo_sala: novo.tipo_sala || 'NORMAL',
      fileiras_verticais: novo.fileiras_verticais || 5,
      fileiras_horizontais: novo.fileiras_horizontais || 6,
      alunos_por_grupo: novo.alunos_por_grupo || 1,
      mostrar_grade: novo.mostrar_grade ?? true,
      mostrar_numeros: novo.mostrar_numeros ?? true,
      cor_fundo: novo.cor_fundo || '#f5f5f5'
    }
  }
}, { immediate: true })

// Editable é sempre true para o editor do professor
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #2d531a;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #1a3810;
}
</style>

