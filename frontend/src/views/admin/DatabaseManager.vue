<template>
  <div class="database-manager-view bg-gradient-to-br from-gray-900 to-black min-h-screen text-white py-10">
    <div class="container mx-auto px-4">
      <GlassCard class="max-w-3xl mx-auto">
        <h2 class="text-2xl font-bold mb-6 text-center">Gerenciador de Banco de Dados</h2>
        <div class="flex justify-between items-center mb-6">
          <button @click="backupDatabase" class="bg-emerald-600 hover:bg-emerald-500 px-4 py-2 rounded-lg font-bold flex items-center" :disabled="loading">
            <span v-if="loading && action === 'backup'" class="loader mr-2"></span>
            Backup
          </button>
          <button @click="restoreDatabase" class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg font-bold flex items-center" :disabled="loading">
            <span v-if="loading && action === 'restore'" class="loader mr-2"></span>
            Restaurar
          </button>
          <button @click="clearDatabase" class="bg-red-600 hover:bg-red-500 px-4 py-2 rounded-lg font-bold flex items-center" :disabled="loading">
            <span v-if="loading && action === 'clear'" class="loader mr-2"></span>
            Limpar
          </button>
        </div>
        <div v-if="success" class="text-emerald-400 text-sm mb-4 text-center">{{ success }}</div>
        <div v-if="apiError" class="text-red-400 text-sm mb-4 text-center">{{ apiError }}</div>
        <div class="bg-gray-800 rounded-lg p-4">
          <h3 class="font-bold mb-2">Status do Banco</h3>
          <ul class="space-y-2">
            <li><span class="font-semibold">Último Backup:</span> {{ status.lastBackup }}</li>
            <li><span class="font-semibold">Registros:</span> {{ status.records }}</li>
            <li><span class="font-semibold">Integridade:</span> <span :class="status.integrity ? 'text-emerald-400' : 'text-red-400'">{{ status.integrity ? 'OK' : 'Falha' }}</span></li>
          </ul>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';

interface DBStatus {
  lastBackup: string;
  records: number;
  integrity: boolean;
}

export default {
  name: 'DatabaseManager',
  components: { GlassCard },
  setup() {
    const loading = ref(false);
    const action = ref('');
    const success = ref('');
    const apiError = ref('');
    const status = ref<DBStatus>({
      lastBackup: '2023-10-01 14:32',
      records: 12456,
      integrity: true
    });

    async function backupDatabase() {
      loading.value = true;
      action.value = 'backup';
      success.value = '';
      apiError.value = '';
      try {
        await new Promise(resolve => setTimeout(resolve, 1200));
        status.value.lastBackup = new Date().toISOString().replace('T', ' ').slice(0, 16);
        success.value = 'Backup realizado com sucesso!';
      } catch (err: any) {
        apiError.value = err.message || 'Erro ao realizar backup.';
      } finally {
        loading.value = false;
        action.value = '';
      }
    }

    async function restoreDatabase() {
      loading.value = true;
      action.value = 'restore';
      success.value = '';
      apiError.value = '';
      try {
        await new Promise(resolve => setTimeout(resolve, 1500));
        status.value.integrity = true;
        success.value = 'Banco restaurado com sucesso!';
      } catch (err: any) {
        apiError.value = err.message || 'Erro ao restaurar banco.';
      } finally {
        loading.value = false;
        action.value = '';
      }
    }

    async function clearDatabase() {
      loading.value = true;
      action.value = 'clear';
      success.value = '';
      apiError.value = '';
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        status.value.records = 0;
        status.value.integrity = true;
        success.value = 'Banco limpo com sucesso!';
      } catch (err: any) {
        apiError.value = err.message || 'Erro ao limpar banco.';
      } finally {
        loading.value = false;
        action.value = '';
      }
    }

    return { loading, action, success, apiError, status, backupDatabase, restoreDatabase, clearDatabase };
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