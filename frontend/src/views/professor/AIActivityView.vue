<template>
  <div class="ai-activity-view">
    <GlassCard>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Gerador de Atividades com IA</h2>
        <div class="flex space-x-3">
          <button class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-history mr-2"></i>Histórico
          </button>
          <button class="bg-purple-600 hover:bg-purple-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-save mr-2"></i>Salvar
          </button>
        </div>
      </div>
      
      <AIActivityGenerator />
    </GlassCard>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <GlassCard v-for="activity in generatedActivities" :key="activity.id">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-xl font-bold">{{ activity.title }}</h3>
            <p class="text-gray-400">{{ activity.subject }} - {{ activity.duration }} minutos</p>
          </div>
          <span class="bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full text-xs">
            IA Gerada
          </span>
        </div>
        
        <div class="prose prose-invert max-w-none mb-4" v-html="activity.content"></div>
        
        <div class="flex space-x-3">
          <button class="bg-emerald-600 hover:bg-emerald-500 px-4 py-2 rounded-lg transition-colors flex-1">
            <i class="fas fa-check mr-2"></i>Aprovar
          </button>
          <button class="bg-rose-600 hover:bg-rose-500 px-4 py-2 rounded-lg transition-colors flex-1">
            <i class="fas fa-times mr-2"></i>Rejeitar
          </button>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@shared/GlassCard.vue';
import AIActivityGenerator from '@components/ai/AIActivityGenerator.vue';

export default defineComponent({
  name: 'AIActivityView',
  components: {
    GlassCard,
    AIActivityGenerator
  },
  setup() {
    const generatedActivities = ref([
      {
        id: 1,
        title: 'Atividade de Álgebra Linear',
        subject: 'Matemática',
        duration: 45,
        content: `
          <h4>Objetivos de Aprendizagem:</h4>
          <ul>
            <li>Compreender conceitos básicos de vetores e matrizes</li>
            <li>Resolver sistemas de equações lineares</li>
          </ul>
          
          <h4>Descrição:</h4>
          <p>Resolver os exercícios propostos aplicando os conceitos...</p>
          
          <h4>Critérios de Avaliação:</h4>
          <ul>
            <li>Precisão nos cálculos</li>
            <li>Clareza na resolução</li>
          </ul>
        `
      },
      {
        id: 2,
        title: 'Interpretação de Texto Literário',
        subject: 'Língua Portuguesa',
        duration: 30,
        content: `
          <h4>Objetivos de Aprendizagem:</h4>
          <ul>
            <li>Analisar elementos narrativos</li>
            <li>Identificar figuras de linguagem</li>
          </ul>
          
          <h4>Descrição:</h4>
          <p>Leia o texto e responda as questões analíticas...</p>
        `
      }
    ]);
    
    return {
      generatedActivities
    };
  }
});
</script>