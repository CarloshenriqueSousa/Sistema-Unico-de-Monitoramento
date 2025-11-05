<template>
  <div class="school-management-view">
    <GlassCard>
      <h2 class="text-2xl font-bold mb-4">Gestão Escolar</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassCard>
          <h3 class="font-bold mb-2">Configuração de Salas</h3>
          <router-link to="/escola/classroom-setup" class="text-cyan-400 hover:underline">Ir para Configuração</router-link>
        </GlassCard>
        <GlassCard>
          <h3 class="font-bold mb-2">Cadastro de Usuários</h3>
          <router-link to="/escola/user-registration" class="text-cyan-400 hover:underline">Ir para Cadastro</router-link>
        </GlassCard>
      </div>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GlassCard from '@shared/GlassCard.vue';

export default defineComponent({
  name: 'SchoolManagementView',
  components: { GlassCard }
});
</script>