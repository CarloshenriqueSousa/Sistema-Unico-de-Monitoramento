<template>
  <div class="ai-question-bank bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Banco de Questões com IA</h3>
          <p class="text-white/70 text-sm">Gere questões personalizadas automaticamente</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <!-- Configuration Panel -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Topic Selection -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Tópico das Questões
            </label>
            <select 
              v-model="topic" 
              class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#0f1e3f] transition-all"
            >
              <option v-for="t in topics" :key="t.value" :value="t.value">
                {{ t.label }}
              </option>
            </select>
          </div>

          <!-- Difficulty Selection -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Nível de Dificuldade
            </label>
            <div class="grid grid-cols-3 gap-2">
              <button 
                v-for="diff in difficulties" 
                :key="diff.value"
                @click="difficulty = diff.value"
                class="py-2.5 rounded-lg font-medium text-sm transition-all"
                :class="difficulty === diff.value 
                  ? 'bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white shadow-md' 
                  : 'bg-[#e1d4c2]/30 text-[#1f1d20] hover:bg-[#e1d4c2]'"
              >
                {{ diff.label }}
              </button>
            </div>
          </div>

          <!-- Question Count Slider -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Quantidade de Questões
            </label>
            <div class="flex items-center gap-4">
              <input 
                type="range" 
                v-model="questionCount" 
                min="1" 
                max="20" 
                class="flex-1 h-2 bg-[#e1d4c2] rounded-lg appearance-none cursor-pointer accent-[#2d531a]"
              >
              <div class="w-12 h-10 rounded-lg bg-[#2d531a]/10 flex items-center justify-center">
                <span class="text-lg font-bold text-[#2d531a]">{{ questionCount }}</span>
              </div>
            </div>
          </div>

          <!-- Generate Button -->
          <button 
            @click="generateQuestions" 
            :disabled="loading"
            class="w-full py-4 rounded-xl bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white font-semibold shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            <template v-if="!loading">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Gerar Questões
            </template>
            <template v-else>
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Gerando...
            </template>
          </button>
        </div>

        <!-- Stats Panel -->
        <div class="space-y-4">
          <div class="p-5 bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl border border-[#e1d4c2]">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm text-[#1f1d20]/60">Total Geradas</span>
              <svg class="w-5 h-5 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <p class="text-3xl font-bold text-[#2d531a]">{{ questions.length }}</p>
          </div>

          <div class="p-5 bg-[#e1d4c2]/30 rounded-xl">
            <h4 class="text-sm font-semibold text-[#1f1d20] mb-3">Tópico Selecionado</h4>
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-[#2d531a] animate-pulse"></div>
              <p class="text-sm text-[#1f1d20]/70">{{ topics.find(t => t.value === topic)?.label }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Questions List -->
      <div v-if="questions.length > 0" class="space-y-3">
        <div class="flex items-center justify-between mb-4">
          <h4 class="text-lg font-bold text-[#1f1d20]">Questões Geradas</h4>
          <button class="px-4 py-2 rounded-lg bg-[#e1d4c2] hover:bg-[#2d531a] text-[#1f1d20] hover:text-white font-medium transition-all text-sm">
            Exportar Tudo
          </button>
        </div>

        <TransitionGroup name="list">
          <div 
            v-for="(question, idx) in questions" 
            :key="idx"
            class="question-item group bg-[#e1d4c2]/20 hover:bg-[#e1d4c2]/40 border border-[#e1d4c2] rounded-xl p-5 transition-all duration-300"
          >
            <div class="flex items-start gap-4">
              <!-- Question Number -->
              <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#0f1e3f] to-[#2d531a] flex items-center justify-center flex-shrink-0">
                <span class="text-white font-bold">{{ idx + 1 }}</span>
              </div>

              <!-- Question Content -->
              <div class="flex-1 min-w-0">
                <div class="text-[#1f1d20] mb-3 leading-relaxed" v-html="formatQuestion(question)"></div>
                
                <!-- Actions -->
                <div class="flex items-center gap-2">
                  <button class="px-3 py-1.5 rounded-lg bg-white border border-[#e1d4c2] hover:bg-[#e1d4c2] text-[#1f1d20] font-medium transition-all text-xs flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Editar
                  </button>
                  <button class="px-3 py-1.5 rounded-lg bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white font-medium transition-all text-xs flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Adicionar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading" class="py-12 text-center">
        <div class="w-20 h-20 mx-auto mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
          <svg class="w-10 h-10 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-[#1f1d20] font-medium mb-2">Nenhuma questão gerada ainda</p>
        <p class="text-sm text-[#1f1d20]/60">Configure e clique em "Gerar Questões" para começar</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const topics = ref([
  { value: 'enem-math', label: 'Matemática (ENEM)' },
  { value: 'bio-vestibular', label: 'Biologia (Vestibular)' },
  { value: 'physics-modern', label: 'Física Moderna' },
  { value: 'literature-br', label: 'Literatura Brasileira' },
  { value: 'chemistry', label: 'Química' },
  { value: 'history', label: 'História' },
  { value: 'other', label: 'Outros Tópicos' }
]);

const difficulties = ref([
  { value: 'easy', label: 'Fácil' },
  { value: 'medium', label: 'Médio' },
  { value: 'hard', label: 'Difícil' }
]);

const topic = ref('enem-math');
const difficulty = ref('medium');
const questionCount = ref(5);
const questions = ref<string[]>([]);
const loading = ref(false);

const generateQuestions = async () => {
  loading.value = true;
  questions.value = [];
  
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  const sampleQuestions = [
    'Calcule o valor de x na equação: 2x + 5 = 15',
    'Determine a área de um triângulo com base 10cm e altura 8cm',
    'Resolva o sistema de equações: x + y = 10 e x - y = 2',
    'Qual é o perímetro de um retângulo com lados 5cm e 12cm?',
    'Encontre as raízes da equação quadrática: x² - 5x + 6 = 0'
  ];
  
  questions.value = sampleQuestions.slice(0, questionCount.value);
  loading.value = false;
};

const formatQuestion = (text: string) => {
  return text
    .replace(/x²/g, '<sup>2</sup>')
    .replace(/(\d+)([a-z]+)/g, '$1<span class="text-[#2d531a]">$2</span>');
};
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.question-item {
  transition: all 0.3s ease;
}

.question-item:hover {
  transform: translateX(4px);
}
</style>