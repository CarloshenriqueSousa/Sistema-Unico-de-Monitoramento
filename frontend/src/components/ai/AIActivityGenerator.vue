<template>
  <div class="ai-activity-generator bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Gerador de Atividades com IA</h3>
          <p class="text-white/70 text-sm">Crie atividades personalizadas automaticamente</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Prompt Input -->
      <div class="mb-5">
        <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
          Descrição da Atividade
        </label>
        <textarea 
          v-model="prompt" 
          rows="4"
          placeholder="Ex: Atividade sobre Revolução Industrial para o 8º ano com 5 questões dissertativas..."
          class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all resize-none"
        ></textarea>
      </div>

      <!-- Configuration Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
        <div>
          <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
            Nível de Ensino
          </label>
          <select 
            v-model="level" 
            class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all"
          >
            <option>Fundamental I</option>
            <option>Fundamental II</option>
            <option>Ensino Médio</option>
            <option>Pré-vestibular</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
            Formato
          </label>
          <select 
            v-model="format" 
            class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all"
          >
            <option>Lista de Exercícios</option>
            <option>Projeto</option>
            <option>Atividade em Grupo</option>
            <option>Avaliação</option>
            <option>Pesquisa</option>
          </select>
        </div>
      </div>

      <!-- Generate Button -->
      <button 
        @click="generateActivity" 
        :disabled="loading || !prompt.trim()"
        class="w-full py-4 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-semibold shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 mb-6"
      >
        <template v-if="!loading">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Gerar Atividade com IA
        </template>
        <template v-else>
          <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          Gerando...
        </template>
      </button>

      <!-- Preview Area -->
      <div class="preview-area min-h-[300px] bg-[#e1d4c2]/20 border-2 border-dashed border-[#e1d4c2] rounded-xl overflow-hidden">
        <!-- Loading State -->
        <div v-if="loading" class="h-[300px] flex flex-col items-center justify-center">
          <div class="w-16 h-16 mb-4">
            <div class="w-full h-full rounded-full border-4 border-[#2d531a] border-t-transparent animate-spin"></div>
          </div>
          <p class="text-[#1f1d20] font-medium mb-1">Gerando atividade...</p>
          <p class="text-sm text-[#1f1d20]/60">Isso pode levar alguns segundos</p>
        </div>

        <!-- Content -->
        <div v-else-if="activity" class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-bold text-[#2d531a]">Atividade Gerada</h4>
            <div class="flex items-center gap-2">
              <button 
                @click="downloadPDF"
                class="px-3 py-2 rounded-lg bg-[#e1d4c2] hover:bg-[#2d531a] text-[#1f1d20] hover:text-white font-medium transition-all text-sm flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                PDF
              </button>
              <button 
                @click="assignToClass"
                class="px-3 py-2 rounded-lg bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-medium transition-all text-sm flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Atribuir
              </button>
            </div>
          </div>
          <div class="activity-content prose max-w-none" v-html="activity"></div>
        </div>

        <!-- Empty State -->
        <div v-else class="h-[300px] flex flex-col items-center justify-center text-center p-8">
          <div class="w-20 h-20 mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
            <svg class="w-10 h-10 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p class="text-[#1f1d20] font-medium mb-2">Pré-visualização da Atividade</p>
          <p class="text-sm text-[#1f1d20]/60">Configure os campos e gere uma atividade com IA</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const prompt = ref('');
const level = ref('Fundamental II');
const format = ref('Lista de Exercícios');
const activity = ref('');
const loading = ref(false);

const generateActivity = async () => {
  if (!prompt.value.trim()) return;
  
  loading.value = true;
  activity.value = '';
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 2500));
  
  activity.value = `
    <div class="space-y-4">
      <div class="p-4 bg-white rounded-lg border border-[#e1d4c2]">
        <h3 class="text-lg font-bold text-[#2d531a] mb-2">Objetivos de Aprendizagem</h3>
        <ul class="list-disc list-inside space-y-1 text-sm text-[#1f1d20]/80">
          <li>Compreender os conceitos fundamentais do tema proposto</li>
          <li>Desenvolver habilidades de análise crítica</li>
          <li>Aplicar conhecimentos em contextos práticos</li>
        </ul>
      </div>
      
      <div class="p-4 bg-white rounded-lg border border-[#e1d4c2]">
        <h3 class="text-lg font-bold text-[#2d531a] mb-3">Atividades</h3>
        <div class="space-y-3">
          <div>
            <p class="font-semibold text-[#1f1d20] mb-1">1. Questão dissertativa</p>
            <p class="text-sm text-[#1f1d20]/70">Explique com suas palavras os principais conceitos abordados.</p>
          </div>
          <div>
            <p class="font-semibold text-[#1f1d20] mb-1">2. Análise prática</p>
            <p class="text-sm text-[#1f1d20]/70">Apresente exemplos práticos relacionados ao tema estudado.</p>
          </div>
          <div>
            <p class="font-semibold text-[#1f1d20] mb-1">3. Reflexão crítica</p>
            <p class="text-sm text-[#1f1d20]/70">Desenvolva uma análise crítica sobre a relevância do tema.</p>
          </div>
        </div>
      </div>
    </div>
  `;
  
  loading.value = false;
};

const downloadPDF = () => {
  console.log('Downloading PDF...');
};

const assignToClass = () => {
  console.log('Assigning to class...');
};
</script>

<style scoped>
.activity-content :deep(h3) {
  @apply text-[#2d531a] font-bold mb-2;
}

.activity-content :deep(ul) {
  @apply space-y-1;
}

.activity-content :deep(li) {
  @apply text-[#1f1d20]/80;
}
</style>