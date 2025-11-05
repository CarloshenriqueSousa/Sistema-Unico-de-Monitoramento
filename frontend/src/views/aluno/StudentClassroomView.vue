<template>
  <div class="student-classroom-view min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white px-6 py-4 shadow-lg">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold">Mapeamento da Sala - {{ turma?.nome || 'Turma' }}</h1>
          <p class="text-white/70 text-sm" v-if="mapeamento?.atualizado_em">
            Atualizado em: {{ formatDate(mapeamento.atualizado_em) }}
          </p>
        </div>
        <button
          @click="$router.back()"
          class="p-2 rounded-lg hover:bg-white/10 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="text-center">
          <div class="w-16 h-16 border-4 border-[#2d531a] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-gray-700 font-medium">Carregando mapeamento...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <svg class="w-12 h-12 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-red-700 font-medium">{{ error }}</p>
        <button
          @click="carregarDados"
          class="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
        >
          Tentar Novamente
        </button>
      </div>

      <!-- No Mapeamento State -->
      <div v-else-if="!mapeamento" class="bg-white rounded-xl shadow-md p-12 text-center border border-gray-200">
        <svg class="w-24 h-24 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Nenhum mapeamento disponível</h3>
        <p class="text-gray-600 mb-6">Sua turma ainda não possui um mapeamento de sala configurado.</p>
      </div>

      <!-- Mapeamento Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Sidebar com Legenda e Info -->
        <aside class="lg:col-span-1 space-y-4">
          <!-- Sua Posição -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Sua Posição</h3>
            <div v-if="suaPosicao" class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white font-bold">
                  {{ getInitials(suaPosicao.estudante?.usuario?.nome || '') }}
                </div>
                <div class="flex-1">
                  <p class="font-semibold text-gray-800">{{ suaPosicao.estudante?.usuario?.nome || 'Você' }}</p>
                  <p class="text-sm text-gray-600">
                    Linha {{ suaPosicao.linha + 1 }}, Coluna {{ suaPosicao.coluna + 1 }}
                  </p>
                  <p v-if="suaPosicao.numero_grupo" class="text-xs text-amber-600 mt-1">
                    Grupo {{ suaPosicao.numero_grupo }}
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4 text-gray-500 text-sm">
              Posição não definida
            </div>
          </div>

          <!-- Legenda -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Legenda</h3>
            <div class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 border-2 border-amber-300"></div>
                <span class="text-sm text-gray-700">Você</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] border-2 border-white"></div>
                <span class="text-sm text-gray-700">Colegas</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-purple-500 border-2 border-white"></div>
                <span class="text-sm text-gray-700">Dificuldade Visual</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-amber-500 border-2 border-white"></div>
                <span class="text-sm text-gray-700">Líderes</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-12 h-8 rounded-lg bg-[#d97706] border-2 border-white"></div>
                <span class="text-sm text-gray-700">Professor</span>
              </div>
            </div>
          </div>

          <!-- Estatísticas -->
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Estatísticas</h3>
            <div class="space-y-3 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Total de Alunos:</span>
                <span class="font-bold text-gray-800">{{ posicoes.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Grupos:</span>
                <span class="font-bold text-gray-800">{{ totalGrupos }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Capacidade:</span>
                <span class="font-bold text-gray-800">{{ capacidadeTotal }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Ocupação:</span>
                <span class="font-bold" :class="taxaOcupacao >= 80 ? 'text-green-600' : 'text-amber-600'">
                  {{ Math.round(taxaOcupacao) }}%
                </span>
              </div>
            </div>
          </div>
        </aside>

        <!-- Canvas de Visualização -->
        <main class="lg:col-span-3">
          <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
            <ClassroomMapCanvas
              :config="mapeamento"
              :positions="posicoes"
              :objects="mapeamento.objetos_sala || []"
              :editable="false"
              :highlight-student="seuId"
              :mode="'student'"
            />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { classroomApi } from '@/services/classroomApi'
import ClassroomMapCanvas from '@/components/classroom/ClassroomMapCanvas.vue'
import type { MapeamentoConfig, PosicaoAluno, AlunoMapeamentoResponse } from '@/types/classroom'

const router = useRouter()

const loading = ref(true)
const error = ref<string | null>(null)
const mapeamento = ref<MapeamentoConfig | null>(null)
const posicoes = ref<PosicaoAluno[]>([])
const suaPosicao = ref<PosicaoAluno | null>(null)
const seuId = ref<number | null>(null)
const turma = ref<any>(null)

const capacidadeTotal = computed(() => {
  if (!mapeamento.value) return 0
  const linhas = mapeamento.value.fileiras_verticais || 5
  const colunas = mapeamento.value.fileiras_horizontais || 6
  const alunosPorGrupo = mapeamento.value.alunos_por_grupo || 1
  return linhas * colunas * alunosPorGrupo
})

const taxaOcupacao = computed(() => {
  if (capacidadeTotal.value === 0) return 0
  return (posicoes.value.length / capacidadeTotal.value) * 100
})

const totalGrupos = computed(() => {
  const grupos = new Set(posicoes.value.map(p => p.numero_grupo).filter(g => g !== null))
  return grupos.size
})

const carregarDados = async () => {
  loading.value = true
  error.value = null
  
  try {
    const data: AlunoMapeamentoResponse = await classroomApi.getMapeamentoAluno()
    
    mapeamento.value = data.mapeamento
    posicoes.value = data.posicoes
    suaPosicao.value = data.sua_posicao
    seuId.value = data.seu_id
    turma.value = data.mapeamento.turma
  } catch (e: any) {
    error.value = e.response?.data?.error || e.message || 'Erro ao carregar mapeamento'
    console.error('Erro ao carregar mapeamento:', e)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getInitials = (nome: string) => {
  if (!nome) return ''
  return nome.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

onMounted(() => {
  carregarDados()
})
</script>

<style scoped>
/* Estilos específicos para visualização do aluno */
</style>

