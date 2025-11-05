<template>
  <div class="ai-assistant bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Assistente Virtual</h3>
          <p class="text-white/70 text-sm">Tire suas dúvidas com IA</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Query Input -->
      <div class="mb-5">
        <div class="relative">
          <textarea 
            v-model="query" 
            @keyup.enter.ctrl="askAI"
            rows="4"
            maxlength="500"
            placeholder="Como posso te ajudar hoje? (Ctrl+Enter para enviar)"
            class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#0f1e3f] focus:border-transparent transition-all resize-none"
          ></textarea>
          <div class="absolute right-3 bottom-3 text-xs text-[#1f1d20]/40">
            {{ query.length }}/500
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <button 
        @click="askAI" 
        :disabled="loading || !query.trim()"
        class="w-full py-4 rounded-xl bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white font-semibold shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 mb-6"
      >
        <template v-if="!loading">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
          Enviar Pergunta
        </template>
        <template v-else>
          <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          Processando...
        </template>
      </button>

      <!-- Response Area -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 translate-y-4"
        leave-active-class="transition-all duration-200"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="response" 
          class="response-container bg-[#e1d4c2]/20 border border-[#e1d4c2] rounded-xl p-5"
        >
          <!-- Response Header -->
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#0f1e3f] to-[#2d531a] flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h4 class="font-bold text-[#0f1e3f]">Resposta do Assistente</h4>
              <p class="text-xs text-[#1f1d20]/50">Gerado com IA</p>
            </div>
          </div>

          <!-- Response Content -->
          <div 
            class="ai-response text-[#1f1d20]/90 leading-relaxed mb-4" 
            v-html="formattedResponse"
          ></div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-2 pt-3 border-t border-[#e1d4c2]">
            <button 
              @click="copyResponse"
              class="px-4 py-2 rounded-lg bg-white border border-[#e1d4c2] hover:bg-[#e1d4c2] text-[#1f1d20] font-medium transition-all text-sm flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copiar
            </button>
            <button 
              @click="saveResponse"
              class="px-4 py-2 rounded-lg bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white font-medium transition-all text-sm flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              Salvar
            </button>
          </div>
        </div>
      </Transition>

      <!-- Suggestions (when no response) -->
      <div v-if="!response && !loading" class="mt-6">
        <p class="text-sm font-semibold text-[#1f1d20] mb-3">Sugestões de perguntas:</p>
        <div class="space-y-2">
          <button 
            v-for="(suggestion, idx) in suggestions" 
            :key="idx"
            @click="query = suggestion"
            class="w-full text-left px-4 py-3 bg-[#e1d4c2]/30 hover:bg-[#e1d4c2] rounded-lg text-sm text-[#1f1d20] transition-all"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const query = ref('');
const response = ref('');
const loading = ref(false);

const suggestions = [
  'Como criar uma aula dinâmica sobre matemática?',
  'Quais metodologias ativas posso usar?',
  'Dicas para avaliação formativa',
  'Como engajar alunos do ensino fundamental?'
];

const askAI = async () => {
  if (!query.value.trim() || loading.value) return;
  
  loading.value = true;
  response.value = '';
  
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  const tempResponse = `Com base na sua pergunta sobre "${query.value}", posso te ajudar da seguinte forma:\n\n**Principais pontos:**\n\n1. Utilize metodologias ativas que coloquem o aluno no centro do processo de aprendizagem\n2. Incorpore recursos digitais e tecnológicos quando apropriado\n3. Promova a colaboração e o trabalho em equipe\n4. Adapte o conteúdo à realidade dos estudantes\n\n*Essas são apenas algumas sugestões iniciais. Posso detalhar mais qualquer um desses pontos!*`;
  
  typeText(tempResponse);
  
  loading.value = false;
};

const typeText = (text: string) => {
  let i = 0;
  const speed = 20;
  
  const typing = () => {
    if (i < text.length) {
      response.value += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    }
  };
  
  typing();
};

const formattedResponse = computed(() => {
  return response.value
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-[#0f1e3f] font-semibold">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em class="text-[#2d531a]">$1</em>')
    .replace(/\n/g, '<br>');
});

const copyResponse = () => {
  navigator.clipboard.writeText(response.value);
  console.log('Response copied!');
};

const saveResponse = () => {
  console.log('Response saved!');
};
</script>

<style scoped>
.ai-response :deep(strong) {
  @apply text-[#0f1e3f] font-semibold;
}

.ai-response :deep(em) {
  @apply text-[#2d531a] not-italic;
}
</style>