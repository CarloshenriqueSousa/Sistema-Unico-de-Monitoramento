<template>
  <div class="demo-classroom-mapping min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white py-16 px-6">
      <div class="max-w-7xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Sistema de Mapeamento de Sala</h1>
        <p class="text-xl text-white/80 mb-8">Organize sua sala de forma inteligente e visual</p>
        <div class="flex flex-wrap justify-center gap-4">
          <button
            @click="scrollToTemplates"
            class="px-6 py-3 bg-white text-[#2d531a] font-semibold rounded-lg hover:bg-gray-100 transition-colors shadow-lg"
          >
            Ver Templates
          </button>
          <button
            @click="scrollToDemo"
            class="px-6 py-3 bg-white/10 text-white font-semibold rounded-lg hover:bg-white/20 transition-colors border border-white/30"
          >
            Visualizar Demo
          </button>
        </div>
      </div>
    </div>

    <!-- Templates Grid -->
    <div ref="templatesSection" class="max-w-7xl mx-auto px-6 py-12">
      <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Templates Disponíveis</h2>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="text-center">
          <div class="w-16 h-16 border-4 border-[#2d531a] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-gray-700 font-medium">Carregando templates...</p>
        </div>
      </div>

      <!-- Templates Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="template in templates"
          :key="template.id"
          @click="loadTemplate(template)"
          class="bg-white rounded-xl shadow-md p-6 border border-gray-200 hover:shadow-lg hover:border-[#2d531a] cursor-pointer transition-all group"
        >
          <!-- Preview -->
          <div class="w-full h-48 bg-gray-100 rounded-lg mb-4 overflow-hidden flex items-center justify-center">
            <div class="text-6xl">{{ getTemplateIcon(template.tipo_sala) }}</div>
          </div>

          <!-- Info -->
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="px-2 py-1 text-xs font-semibold rounded-full bg-[#2d531a]/10 text-[#2d531a]">
                {{ template.tipo_sala }}
              </span>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2 group-hover:text-[#2d531a] transition-colors">
              {{ template.nome }}
            </h3>
            <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ template.descricao }}</p>
            <button class="w-full px-4 py-2 bg-[#2d531a] text-white rounded-lg hover:bg-[#1a3810] transition-colors font-semibold">
              Visualizar Template
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="templates.length === 0" class="col-span-full text-center py-12">
          <svg class="w-24 h-24 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Nenhum template disponível</h3>
          <p class="text-gray-600">Não há templates públicos no momento.</p>
        </div>
      </div>
    </div>

    <!-- Interactive Demo -->
    <div ref="demoSection" class="max-w-7xl mx-auto px-6 py-12">
      <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Visualização Interativa</h2>
      
      <div v-if="selectedTemplate" class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-2xl font-bold text-gray-800">{{ selectedTemplate.nome }}</h3>
            <p class="text-gray-600 mt-1">{{ selectedTemplate.descricao }}</p>
          </div>
          <button
            @click="selectedTemplate = null"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Fechar
          </button>
        </div>

        <div class="bg-gray-50 rounded-lg p-6 border-2 border-dashed border-gray-300">
          <ClassroomMapCanvas
            :config="selectedTemplate.config"
            :positions="demoPositions"
            :objects="selectedTemplate.config.objetos_sala || []"
            :editable="false"
            :mode="'demo'"
          />
        </div>
      </div>

      <div v-else class="bg-white rounded-xl shadow-md p-12 text-center border border-gray-200">
        <svg class="w-24 h-24 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7 19l4-9m1 1l-9 4" />
        </svg>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Nenhum template selecionado</h3>
        <p class="text-gray-600 mb-6">Selecione um template acima para visualizar a demonstração interativa.</p>
      </div>
    </div>

    <!-- Features Section -->
    <div class="bg-white py-12 px-6">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Recursos do Sistema</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-[#2d531a]/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">Mapeamento Visual</h3>
            <p class="text-gray-600">Visualize e organize a sala de forma interativa com drag-and-drop.</p>
          </div>

          <div class="text-center p-6">
            <div class="w-16 h-16 bg-[#2d531a]/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">Templates Prontos</h3>
            <p class="text-gray-600">Use templates pré-configurados para diferentes tipos de sala.</p>
          </div>

          <div class="text-center p-6">
            <div class="w-16 h-16 bg-[#2d531a]/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">Organização Inteligente</h3>
            <p class="text-gray-600">Organize alunos automaticamente com base em critérios educacionais.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { classroomApi } from '@/services/classroomApi'
import ClassroomMapCanvas from '@/components/classroom/ClassroomMapCanvas.vue'
import type { TemplateSala, PosicaoAluno } from '@/types/classroom'

const loading = ref(true)
const templates = ref<TemplateSala[]>([])
const selectedTemplate = ref<TemplateSala | null>(null)
const demoPositions = ref<PosicaoAluno[]>([])
const templatesSection = ref<HTMLElement>()
const demoSection = ref<HTMLElement>()

const carregarTemplates = async () => {
  loading.value = true
  try {
    templates.value = await classroomApi.getTemplates()
  } catch (e: any) {
    console.error('Erro ao carregar templates:', e)
  } finally {
    loading.value = false
  }
}

const loadTemplate = (template: TemplateSala) => {
  selectedTemplate.value = template
  // Gerar posições demo se houver no config
  if (template.config) {
    demoPositions.value = [] // Pode ser preenchido com posições de exemplo
  }
  scrollToDemo()
}

const scrollToTemplates = () => {
  templatesSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const scrollToDemo = () => {
  demoSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const getTemplateIcon = (tipo: string) => {
  const icons: Record<string, string> = {
    'NORMAL': '🏫',
    'LABORATORIO': '🔬',
    'BIBLIOTECA': '📚',
    'AUDITORIO': '🎭',
    'CUSTOMIZADO': '🛠️'
  }
  return icons[tipo] || '📐'
}

onMounted(() => {
  carregarTemplates()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

