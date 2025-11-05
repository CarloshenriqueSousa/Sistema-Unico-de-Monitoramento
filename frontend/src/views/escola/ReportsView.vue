<template>
  <div class="reports-view">
    <GlassCard>
      <h2 class="text-2xl font-bold mb-4">Relatórios</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassCard>
          <h3 class="font-bold mb-2">Desempenho por Turma</h3>
          <InteractiveChart />
        </GlassCard>
        <GlassCard>
          <h3 class="font-bold mb-2">Frequência dos Alunos</h3>
          <InteractiveChart />
        </GlassCard>
      </div>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GlassCard from '@shared/GlassCard.vue';
import InteractiveChart from '@shared/InteractiveChart.vue';

export default defineComponent({
  name: 'ReportsView',
  components: { GlassCard, InteractiveChart }
});
</script>