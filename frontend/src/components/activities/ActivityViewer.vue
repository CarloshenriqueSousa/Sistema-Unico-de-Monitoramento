<template>
  <div class="activity-viewer bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-white">Visualizador de Atividade</h3>
            <p class="text-white/70 text-sm">Modo de leitura otimizado</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button 
            @click="togglePresentationMode"
            class="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition-all flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
            </svg>
            {{ presentationMode ? 'Sair' : 'Apresentação' }}
          </button>
          
          <button 
            @click="downloadActivity"
            class="px-4 py-2 rounded-lg bg-white text-[#2d531a] hover:bg-white/90 font-medium transition-all flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Baixar
          </button>
        </div>
      </div>
    </div>

    <!-- Content Container -->
    <div 
      class="content-container relative transition-all duration-500"
      :class="presentationMode ? 'h-screen' : 'h-[70vh]'"
    >
      <div class="h-full overflow-y-auto p-8">
        <!-- Activity Content -->
        <div 
          v-if="activityContent" 
          v-html="activityContent" 
          class="activity-content max-w-4xl mx-auto"
          :class="{ 'presentation-text': presentationMode }"
        ></div>

        <!-- Empty State -->
        <div v-else class="h-full flex flex-col items-center justify-center text-center">
          <div class="w-24 h-24 mb-6 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
            <svg class="w-12 h-12 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p class="text-lg text-[#1f1d20] font-medium mb-2">Nenhum conteúdo para exibir</p>
          <p class="text-sm text-[#1f1d20]/60">Selecione uma atividade para visualizar</p>
        </div>
      </div>

      <!-- Presentation Controls -->
      <div v-if="presentationMode" class="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-3">
        <button 
          @click="prevSlide"
          class="w-12 h-12 rounded-full bg-white border-2 border-[#2d531a] hover:bg-[#2d531a] hover:text-white transition-all flex items-center justify-center"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div class="px-4 py-2 rounded-full bg-white border-2 border-[#e1d4c2] font-medium text-[#1f1d20]">
          Slide {{ currentSlide + 1 }}
        </div>
        
        <button 
          @click="nextSlide"
          class="w-12 h-12 rounded-full bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white hover:shadow-lg transition-all flex items-center justify-center"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  activityContent?: string;
}>();

const presentationMode = ref(false);
const currentSlide = ref(0);

const togglePresentationMode = () => {
  presentationMode.value = !presentationMode.value;
  if (!presentationMode.value) {
    currentSlide.value = 0;
  }
};

const nextSlide = () => {
  currentSlide.value++;
};

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--;
  }
};

const downloadActivity = () => {
  console.log('Downloading activity...');
  // Download logic here
};
</script>

<style scoped>
.activity-content :deep(h1) {
  @apply text-3xl font-bold text-[#1f1d20] mb-6 pb-3 border-b-2 border-[#e1d4c2];
}

.activity-content :deep(h2) {
  @apply text-2xl font-bold text-[#1f1d20] mb-5 mt-8;
}

.activity-content :deep(h3) {
  @apply text-xl font-bold text-[#2d531a] mb-4 mt-6;
}

.activity-content :deep(p) {
  @apply text-[#1f1d20]/80 leading-relaxed mb-4;
}

.activity-content :deep(ul) {
  @apply list-disc list-inside mb-4 space-y-2;
}

.activity-content :deep(ol) {
  @apply list-decimal list-inside mb-4 space-y-2;
}

.activity-content :deep(li) {
  @apply text-[#1f1d20]/80 leading-relaxed;
}

.activity-content :deep(strong) {
  @apply font-bold text-[#1f1d20];
}

.activity-content :deep(em) {
  @apply italic text-[#2d531a];
}

.activity-content :deep(code) {
  @apply px-2 py-1 bg-[#e1d4c2] rounded text-sm font-mono text-[#1f1d20];
}

.activity-content :deep(blockquote) {
  @apply border-l-4 border-[#2d531a] pl-4 italic text-[#1f1d20]/70 my-4;
}

.presentation-text :deep(*) {
  @apply text-xl leading-relaxed;
}

.presentation-text :deep(h1) {
  @apply text-5xl mb-12;
}

.presentation-text :deep(h2) {
  @apply text-4xl mb-10;
}

.presentation-text :deep(h3) {
  @apply text-3xl mb-8;
}
</style>