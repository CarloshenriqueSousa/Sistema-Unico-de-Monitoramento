<template>
  <div class="dashboard-escola">
    <GlassCard>
      <h2 class="text-2xl font-bold mb-2">Dashboard da Escola</h2>
      <p class="text-gray-400 mb-6">Visão geral de turmas, professores e alunos</p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard>
          <h3 class="font-bold mb-2">Turmas</h3>
          <p class="text-3xl font-bold text-cyan-400">12</p>
        </GlassCard>
        <GlassCard>
          <h3 class="font-bold mb-2">Professores</h3>
          <p class="text-3xl font-bold text-amber-400">8</p>
        </GlassCard>
        <GlassCard>
          <h3 class="font-bold mb-2">Alunos</h3>
          <p class="text-3xl font-bold text-purple-400">240</p>
        </GlassCard>
      </div>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GlassCard from '@shared/GlassCard.vue';

export default defineComponent({
  name: 'DashboardEscola',
  components: { GlassCard }
});
</script>