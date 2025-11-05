<template>
  <div class="student-analysis-view">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <GlassCard>
        <h3 class="text-xl font-bold mb-4">Habilidades da Turma</h3>
        <div class="h-64">
          <SkillRadar :items="skills" />
        </div>
      </GlassCard>
      
      <GlassCard>
        <h3 class="text-xl font-bold mb-4">Distribuição de Desempenho</h3>
        <div class="h-64">
          <InteractiveChart 
            type="doughnut"
            :data="performanceData"
          />
        </div>
      </GlassCard>
    </div>
    
    <GlassCard>
      <h3 class="text-xl font-bold mb-4">Recomendações de Agrupamento</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="(group, index) in recommendedGroups" :key="index" class="bg-gray-800/50 p-4 rounded-xl">
          <h4 class="font-bold text-cyan-400 mb-2">Grupo {{ index + 1 }}</h4>
          <ul class="space-y-1">
            <li v-for="student in group" :key="student" class="flex items-center">
              <div class="w-6 h-6 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center mr-2 text-xs">
                {{ student.charAt(0) }}
              </div>
              <span>{{ student }}</span>
            </li>
          </ul>
          <div class="mt-3 text-sm text-gray-400">
            <i class="fas fa-lightbulb mr-2 text-amber-400"></i>
            {{ groupRecommendations[index] }}
          </div>
        </div>
      </div>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@shared/GlassCard.vue';
import SkillRadar from '@/shared/SkillRadar.vue';
import InteractiveChart from '@/shared/InteractiveChart.vue';

export default defineComponent({
  name: 'StudentAnalysisView',
  components: {
    GlassCard,
    SkillRadar,
    InteractiveChart
  },
  setup() {
    const skills = ref([
      { label: 'Matemática', value: 85 },
      { label: 'Linguagens', value: 78 },
      { label: 'Ciências', value: 92 },
      { label: 'História', value: 76 },
      { label: 'Geografia', value: 88 }
    ]);
    
    const performanceData = ref({
      labels: ['Excelente', 'Bom', 'Médio', 'Insuficiente'],
      datasets: [{
        data: [8, 12, 6, 2],
        backgroundColor: [
          'rgba(46, 204, 113, 0.8)',
          'rgba(52, 152, 219, 0.8)',
          'rgba(241, 196, 15, 0.8)',
          'rgba(231, 76, 60, 0.8)'
        ],
        borderColor: [
          'rgba(46, 204, 113, 1)',
          'rgba(52, 152, 219, 1)',
          'rgba(241, 196, 15, 1)',
          'rgba(231, 76, 60, 1)'
        ],
        borderWidth: 1
      }]
    });
    
    const recommendedGroups = ref([
      ['João Silva', 'Maria Oliveira', 'Carlos Pereira'],
      ['Ana Costa', 'Pedro Santos', 'Juliana Lima'],
      ['Fernando Souza', 'Camila Almeida', 'Ricardo Gomes']
    ]);
    
    const groupRecommendations = ref([
      'Foco em projetos de matemática avançada',
      'Grupo para reforço em ciências',
      'Atividades interdisciplinares'
    ]);
    
    return {
      skills,
      performanceData,
      recommendedGroups,
      groupRecommendations
    };
  }
});
</script>