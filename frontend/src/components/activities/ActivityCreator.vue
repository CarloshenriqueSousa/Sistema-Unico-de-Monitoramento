<template>
  <div class="activity-creator bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div>
          <h3 class="text-2xl font-bold text-white">Criador de Atividades</h3>
          <p class="text-white/70 text-sm">Crie atividades personalizadas com IA</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Configuration Panel -->
        <div class="space-y-5">
          <!-- Activity Type -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Tipo de Atividade
            </label>
            <select 
              v-model="activityType" 
              class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all"
            >
              <option value="exercise">Exercício</option>
              <option value="project">Projeto</option>
              <option value="test">Avaliação</option>
              <option value="reading">Leitura</option>
              <option value="research">Pesquisa</option>
            </select>
          </div>

          <!-- Topic -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Tema/Matéria
            </label>
            <input 
              v-model="activityTopic" 
              type="text"
              placeholder="Ex: Revolução Francesa, Álgebra Linear..."
              class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all"
            >
          </div>

          <!-- Difficulty Level -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-3">
              Nível de Dificuldade
            </label>
            <div class="grid grid-cols-4 gap-2">
              <button 
                v-for="level in difficultyLevels" 
                :key="level.value"
                @click="difficulty = level.value"
                class="py-2.5 px-3 rounded-lg font-medium text-sm transition-all"
                :class="difficulty === level.value 
                  ? 'bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white shadow-md' 
                  : 'bg-[#e1d4c2]/30 text-[#1f1d20] hover:bg-[#e1d4c2]'"
              >
                {{ level.label }}
              </button>
            </div>
          </div>

          <!-- Additional Details -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Detalhes Adicionais
            </label>
            <textarea 
              v-model="additionalDetails" 
              rows="4"
              placeholder="Descreva objetivos, contexto, competências..."
              class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all resize-none"
            ></textarea>
          </div>

          <!-- Generate Button -->
          <button 
            @click="generateActivity" 
            :disabled="isGenerating || !activityTopic"
            class="w-full py-4 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-semibold shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            <svg v-if="!isGenerating" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <div v-else class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            {{ isGenerating ? 'Gerando...' : 'Gerar Atividade com IA' }}
          </button>
        </div>

        <!-- Preview Panel -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-bold text-[#1f1d20]">Pré-visualização</h4>
            <button 
              @click="saveActivity" 
              :disabled="!activityContent"
              class="px-4 py-2 rounded-lg bg-[#e1d4c2] text-[#1f1d20] font-medium hover:bg-[#2d531a] hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Salvar
            </button>
          </div>

          <div class="preview-container h-[500px] bg-[#e1d4c2]/20 border-2 border-dashed border-[#e1d4c2] rounded-xl overflow-y-auto">
            <!-- Loading State -->
            <div v-if="isGenerating" class="h-full flex flex-col items-center justify-center p-8 text-center">
              <div class="w-16 h-16 mb-4">
                <div class="w-full h-full rounded-full border-4 border-[#2d531a] border-t-transparent animate-spin"></div>
              </div>
              <p class="text-[#1f1d20] font-medium mb-2">Gerando atividade com IA...</p>
              <p class="text-sm text-[#1f1d20]/60">Isso pode levar alguns segundos</p>
            </div>

            <!-- Content -->
            <div v-else-if="activityContent" class="p-6 prose prose-slate max-w-none">
              <div v-html="activityContent" class="activity-content"></div>
            </div>

            <!-- Empty State -->
            <div v-else class="h-full flex flex-col items-center justify-center p-8 text-center">
              <div class="w-20 h-20 mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
                <svg class="w-10 h-10 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p class="text-[#1f1d20]/60">Configure e gere uma atividade</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const activityType = ref('exercise');
const activityTopic = ref('');
const difficulty = ref('medium');
const additionalDetails = ref('');
const activityContent = ref('');
const isGenerating = ref(false);

const difficultyLevels = [
  { value: 'easy', label: 'Fácil' },
  { value: 'medium', label: 'Médio' },
  { value: 'hard', label: 'Difícil' },
  { value: 'advanced', label: 'Avançado' }
];

const generateActivity = async () => {
  if (!activityTopic.value) return;
  
  isGenerating.value = true;
  activityContent.value = '';
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2500));
  
  // Generated content
  activityContent.value = `
    <div class="space-y-6">
      <div>
        <h3 class="text-xl font-bold text-[#1f1d20] mb-2">Atividade: ${activityTopic.value}</h3>
        <p class="text-sm text-[#1f1d20]/60">Tipo: ${activityType.value} • Nível: ${difficulty}</p>
      </div>
      
      <div class="space-y-4">
        <div class="p-4 bg-white rounded-lg border border-[#e1d4c2]">
          <h4 class="font-bold text-[#1f1d20] mb-2">Objetivos de Aprendizagem</h4>
          <ul class="list-disc list-inside space-y-1 text-sm text-[#1f1d20]/70">
            <li>Compreender os conceitos fundamentais sobre ${activityTopic.value}</li>
            <li>Aplicar conhecimentos em situações práticas</li>
            <li>Desenvolver pensamento crítico sobre o tema</li>
          </ul>
        </div>
        
        <div class="p-4 bg-white rounded-lg border border-[#e1d4c2]">
          <h4 class="font-bold text-[#1f1d20] mb-3">Questões</h4>
          <div class="space-y-3">
            <div>
              <p class="font-medium text-[#1f1d20] mb-1">1. Explique os principais aspectos de ${activityTopic.value}.</p>
              <p class="text-sm text-[#1f1d20]/60">Resposta esperada: mínimo 5 linhas</p>
            </div>
            <div>
              <p class="font-medium text-[#1f1d20] mb-1">2. Como ${activityTopic.value} se aplica na prática?</p>
              <p class="text-sm text-[#1f1d20]/60">Resposta esperada: exemplos concretos</p>
            </div>
            <div>
              <p class="font-medium text-[#1f1d20] mb-1">3. Análise crítica sobre ${activityTopic.value}.</p>
              <p class="text-sm text-[#1f1d20]/60">Resposta esperada: argumentação fundamentada</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
  isGenerating.value = false;
};

const saveActivity = () => {
  console.log('Atividade salva:', activityContent.value);
  // Backend logic here
};
</script>

<style scoped>
.activity-content :deep(h3) {
  @apply text-xl font-bold text-[#1f1d20] mb-3;
}

.activity-content :deep(h4) {
  @apply text-lg font-semibold text-[#1f1d20] mb-2;
}

.activity-content :deep(p) {
  @apply text-[#1f1d20]/70 leading-relaxed;
}

.activity-content :deep(ul) {
  @apply space-y-2;
}

.activity-content :deep(li) {
  @apply text-[#1f1d20]/70;
}
</style>