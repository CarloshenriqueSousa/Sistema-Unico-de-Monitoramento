<template>
  <div class="ai-notes-view">
    <GlassCard>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Gerador de Anotações com IA</h2>
        <div class="flex space-x-3">
          <select v-model="complexity" class="bg-gray-800 rounded-lg px-3 py-2">
            <option value="basic">Básico</option>
            <option value="intermediate">Intermediário</option>
            <option value="advanced">Avançado</option>
          </select>
          <button class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-magic mr-2"></i>Otimizar
          </button>
        </div>
      </div>
      
      <AINoteGenerator />
    </GlassCard>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <GlassCard v-for="note in generatedNotes" :key="note.id">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-xl font-bold">{{ note.title }}</h3>
            <p class="text-gray-400">{{ note.subject }} - {{ note.pages }} páginas</p>
          </div>
          <span class="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-xs">
            IA Gerada
          </span>
        </div>
        
        <div class="prose prose-invert max-w-none mb-4" v-html="note.content"></div>
        
        <div class="flex space-x-3">
          <button class="bg-emerald-600 hover:bg-emerald-500 px-4 py-2 rounded-lg transition-colors flex-1">
            <i class="fas fa-download mr-2"></i>Exportar
          </button>
          <button class="bg-amber-500 hover:bg-amber-400 px-4 py-2 rounded-lg transition-colors flex-1">
            <i class="fas fa-edit mr-2"></i>Editar
          </button>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';
import AINoteGenerator from '@/components/ai/AINoteGenerator.vue';

export default defineComponent({
  name: 'AINotesView',
  components: {
    GlassCard,
    AINoteGenerator
  },
  setup() {
    const complexity = ref('intermediate');
    
    const generatedNotes = ref([
      {
        id: 1,
        title: 'Revolução Industrial',
        subject: 'História',
        pages: 3,
        content: `
          <h3>Contexto Histórico</h3>
          <p>A Revolução Industrial iniciou-se na Inglaterra no século XVIII...</p>
          
          <h3>Principais Inovações</h3>
          <ul>
            <li>Máquina a vapor</li>
            <li>Teares mecânicos</li>
          </ul>
        `
      },
      {
        id: 2,
        title: 'Fotossíntese',
        subject: 'Biologia',
        pages: 2,
        content: `
          <h3>Processo Biológico</h3>
          <p>Fotossíntese é o processo pelo qual plantas convertem luz solar em energia...</p>
          
          <h3>Fórmula Química</h3>
          <p>6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂</p>
        `
      }
    ]);
    
    return {
      complexity,
      generatedNotes
    };
  }
});
</script>