<template>
  <div class="system-config-view bg-gradient-to-br from-gray-900 to-black min-h-screen text-white py-10">
    <div class="container mx-auto px-4">
      <GlassCard class="max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold mb-6 text-center">Configurações do Sistema</h2>
        <form @submit.prevent="saveConfig" class="space-y-6">
          <div>
            <label class="block mb-2 font-semibold">Nome da Escola</label>
            <input v-model="config.schoolName" class="bg-gray-800 rounded-lg px-3 py-2 w-full" />
          </div>
          <div>
            <label class="block mb-2 font-semibold">Ano Letivo</label>
            <input v-model="config.schoolYear" class="bg-gray-800 rounded-lg px-3 py-2 w-full" type="number" min="2000" max="2100" />
          </div>
          <div>
            <label class="block mb-2 font-semibold">Tema</label>
            <select v-model="config.theme" class="bg-gray-800 rounded-lg px-3 py-2 w-full">
              <option value="dark">Escuro</option>
              <option value="light">Claro</option>
              <option value="auto">Automático</option>
            </select>
          </div>
          <div>
            <label class="block mb-2 font-semibold">Notificações</label>
            <input type="checkbox" v-model="config.notifications" class="mr-2" />
            <span>Ativar notificações globais</span>
          </div>
          <button
            class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg w-full font-bold flex items-center justify-center"
            :disabled="loading"
          >
            <span v-if="loading" class="loader mr-2"></span>
            Salvar Configurações
          </button>
          <p v-if="success" class="text-emerald-400 text-sm mt-2 text-center">Configurações salvas com sucesso!</p>
          <p v-if="apiError" class="text-red-400 text-sm mt-2 text-center">{{ apiError }}</p>
        </form>
      </GlassCard>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';

interface Config {
  schoolName: string;
  schoolYear: number;
  theme: string;
  notifications: boolean;
}

export default {
  name: 'SystemConfigView',
  components: { GlassCard },
  setup() {
    const config = ref<Config>({
      schoolName: 'Escola Modelo',
      schoolYear: new Date().getFullYear(),
      theme: 'dark',
      notifications: true
    });
    const loading = ref(false);
    const success = ref(false);
    const apiError = ref('');

    async function saveConfig() {
      apiError.value = '';
      success.value = false;
      loading.value = true;
      try {
        // Simulação de chamada à API
        await new Promise(resolve => setTimeout(resolve, 1200));
        success.value = true;
      } catch (err: any) {
        apiError.value = err.message || 'Erro ao salvar configurações.';
      } finally {
        loading.value = false;
      }
    }

    return { config, loading, success, apiError, saveConfig };
  }
};
</script>

<style scoped>
.loader {
  border: 2px solid #22d3ee;
  border-top: 2px solid transparent;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 0.7s linear infinite;
  display: inline-block;
  vertical-align: middle;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>