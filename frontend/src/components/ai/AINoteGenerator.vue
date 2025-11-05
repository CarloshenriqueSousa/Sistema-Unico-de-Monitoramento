<template>
  <div class="ai-note-generator bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Gerador de Anotações com IA</h3>
          <p class="text-white/70 text-sm">Crie resumos e anotações estruturadas</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- Topic Input -->
      <div class="mb-5">
        <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
          Tópico para Anotações
        </label>
        <textarea 
          v-model="topic" 
          rows="3"
          placeholder="Ex: Revolução Industrial, Teorema de Pitágoras, Ciclo de Krebs..."
          class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all resize-none"
        ></textarea>
      </div>

      <!-- Configuration Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
        <div>
          <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
            Estilo
          </label>
          <select 
            v-model="style" 
            class="w-full px-4 py-2.5 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] transition-all"
          >
            <option>Resumo</option>
            <option>Mapa Mental</option>
            <option>Linha do Tempo</option>
            <option>Diagrama</option>
            <option>Flashcards</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
            Nível
          </label>
          <select 
            v-model="level" 
            class="w-full px-4 py-2.5 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] transition-all"
          >
            <option>Básico</option>
            <option>Intermediário</option>
            <option>Avançado</option>
            <option>Profissional</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
            Formato
          </label>
          <select 
            v-model="format" 
            class="w-full px-4 py-2.5 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-[#2d531a] transition-all"
          >
            <option>Texto Corrido</option>
            <option>Bullet Points</option>
            <option>Tabela</option>
            <option>Esquema</option>
          </select>
        </div>
      </div>

      <!-- Generate Button -->
      <button 
        @click="generateNote" 
        :disabled="loading || !topic.trim()"
        class="w-full py-4 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-semibold shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 mb-6"
      >
        <template v-if="!loading">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          Gerar Anotações
        </template>
        <template v-else>
          <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          Gerando...
        </template>
      </button>

      <!-- Notes Display Area -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 translate-y-4"
        leave-active-class="transition-all duration-200"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="note" 
          class="note-result bg-[#e1d4c2]/20 border border-[#e1d4c2] rounded-xl p-5"
        >
          <!-- Note Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h4 class="font-bold text-[#2d531a]">Anotações sobre {{ topic }}</h4>
                <p class="text-xs text-[#1f1d20]/50">{{ style }} • {{ level }}</p>
              </div>
            </div>
            <span class="px-3 py-1 rounded-full bg-[#2d531a]/10 text-[#2d531a] text-xs font-medium">
              {{ format }}
            </span>
          </div>

          <!-- Note Content -->
          <div 
            class="note-content text-[#1f1d20] leading-relaxed mb-4 max-h-[400px] overflow-y-auto pr-2" 
            v-html="formattedNote"
          ></div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-2 pt-3 border-t border-[#e1d4c2]">
            <button 
              @click="copyNote"
              class="px-4 py-2 rounded-lg bg-white border border-[#e1d4c2] hover:bg-[#e1d4c2] text-[#1f1d20] font-medium transition-all text-sm flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copiar
            </button>
            <button 
              @click="saveNote"
              class="px-4 py-2 rounded-lg bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-medium transition-all text-sm flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              Salvar
            </button>
          </div>
        </div>
      </Transition>

      <!-- Empty State -->
      <div v-if="!note && !loading" class="mt-6 p-8 bg-[#e1d4c2]/10 rounded-xl text-center">
        <div class="w-16 h-16 mx-auto mb-3 rounded-xl bg-[#e1d4c2] flex items-center justify-center">
          <svg class="w-8 h-8 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p class="text-sm text-[#1f1d20]/60">Suas anotações geradas aparecerão aqui</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const topic = ref('');
const style = ref('Resumo');
const level = ref('Intermediário');
const format = ref('Bullet Points');
const note = ref('');
const loading = ref(false);

const generateNote = async () => {
  if (!topic.value.trim()) return;
  
  loading.value = true;
  note.value = '';
  
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  note.value = `
## Introdução ##
${topic.value} é um tema fundamental que apresenta diversos conceitos importantes para compreensão.

## Pontos Principais ##
- **Conceito 1**: Primeira ideia central sobre o tema abordado
- **Conceito 2**: Segunda ideia essencial para entendimento completo
- **Conceito 3**: Terceira consideração importante no contexto

[!TIP] Dica importante: Revise estes pontos regularmente para fixação do conteúdo.

## Exemplos Práticos ##
- Exemplo 1: Aplicação real do conceito
- Exemplo 2: Situação cotidiana relacionada
- Exemplo 3: Caso prático de uso

[!WARNING] Atenção: Alguns pontos requerem aprofundamento adicional.

## Conclusão ##
Compreender **${topic.value}** é essencial para avançar nos estudos desta área.
  `;
  
  loading.value = false;
};

const formattedNote = computed(() => {
  return note.value
    .replace(/## (.+?) ##/g, '<h3 class="text-lg font-bold text-[#2d531a] mt-5 mb-3 pb-2 border-b-2 border-[#e1d4c2]">$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-[#2d531a] font-semibold">$1</strong>')
    .replace(/\[!TIP\]/g, '<div class="bg-[#2d531a]/10 border-l-4 border-[#2d531a] p-4 my-4 rounded-r-lg"><div class="flex items-start gap-2"><svg class="w-5 h-5 text-[#2d531a] flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg><div><strong class="text-[#2d531a] font-semibold">Dica:</strong>')
    .replace(/\[!WARNING\]/g, '<div class="bg-amber-50 border-l-4 border-amber-500 p-4 my-4 rounded-r-lg"><div class="flex items-start gap-2"><svg class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg><div><strong class="text-amber-700 font-semibold">Atenção:</strong>')
    .replace(/- (.+)/g, '<li class="ml-5 mb-2 list-disc">$1</li>')
    .replace(/\n/g, '<br>');
});

const copyNote = () => {
  const plainText = note.value.replace(/##|#|\*\*|\[!TIP\]|\[!WARNING\]/g, '');
  navigator.clipboard.writeText(plainText);
  console.log('Note copied!');
};

const saveNote = () => {
  console.log('Note saved!');
};
</script>

<style scoped>
.note-content :deep(h3) {
  @apply text-[#2d531a] font-bold text-lg mt-5 mb-3 pb-2 border-b-2 border-[#e1d4c2];
}

.note-content :deep(strong) {
  @apply text-[#2d531a] font-semibold;
}

.note-content :deep(li) {
  @apply text-[#1f1d20]/80 mb-2;
}

.note-content :deep(div) {
  @apply mb-3;
}

/* Custom scrollbar */
.note-content::-webkit-scrollbar {
  width: 6px;
}

.note-content::-webkit-scrollbar-track {
  background: #e1d4c2;
  border-radius: 3px;
}

.note-content::-webkit-scrollbar-thumb {
  background: #2d531a;
  border-radius: 3px;
}

.note-content::-webkit-scrollbar-thumb:hover {
  background: #0f1e3f;
}
</style>