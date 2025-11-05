<template>
  <div class="classroom-setup-view">
    <GlassCard>
      <h2 class="text-2xl font-bold mb-4">Configuração de Salas</h2>
      <div class="flex space-x-4 mb-6">
        <input v-model="newClassroom" class="bg-gray-800 rounded-lg px-3 py-2" placeholder="Nome da sala" />
        <button @click="addClassroom" class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg">Adicionar</button>
      </div>
      <DynamicTable
        :headers="[{ label: 'Sala', key: 'name' }, { label: 'Ações', key: 'actions' }]"
        :items="classrooms"
      >
        <template #row="props">
          <td class="py-3 px-4">{{ props.item.name }}</td>
          <td class="py-3 px-4">
            <button @click="removeClassroom(props.item)" class="text-red-400 hover:text-red-300">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </template>
      </DynamicTable>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';
import DynamicTable from '@/shared/DynamicTable.vue';

export default defineComponent({
  name: 'ClassroomSetupView',
  components: { GlassCard, DynamicTable },
  setup() {
    const newClassroom = ref('');
    const classrooms = ref([{ name: '1A' }, { name: '2B' }]);
    function addClassroom() {
      if (newClassroom.value.trim()) {
        classrooms.value.push({ name: newClassroom.value });
        newClassroom.value = '';
      }
    }
    function removeClassroom(item: { name: string }) {
      classrooms.value = classrooms.value.filter(c => c.name !== item.name);
    }
    return { newClassroom, classrooms, addClassroom, removeClassroom };
  }
});
</script>