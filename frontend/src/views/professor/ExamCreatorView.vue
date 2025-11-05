<template>
  <div class="exam-creator-view">
    <GlassCard>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Criador de Provas</h2>
        <div class="flex space-x-3">
          <button class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-plus mr-2"></i>Nova Prova
          </button>
          <button class="bg-purple-600 hover:bg-purple-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-database mr-2"></i>Banco de Questões
          </button>
        </div>
      </div>
      
      <ExamCreator />
    </GlassCard>
    
    <GlassCard class="mt-6">
      <h3 class="text-xl font-bold mb-4">Provas Criadas</h3>
      <DynamicTable 
        :headers="headers"
        :items="exams"
        class="rounded-xl overflow-hidden"
      >
        <template #row="props">
          <td class="py-3 px-4 font-medium">{{ props.item.title }}</td>
          <td class="py-3 px-4">{{ props.item.subject }}</td>
          <td class="py-3 px-4">{{ props.item.duration }} min</td>
          <td class="py-3 px-4">
            <span :class="statusClass(props.item.status)">
              {{ props.item.status }}
            </span>
          </td>
          <td class="py-3 px-4">
            <div class="flex space-x-3">
              <button class="text-cyan-400 hover:text-cyan-300">
                <i class="fas fa-eye"></i>
              </button>
              <button class="text-amber-400 hover:text-amber-300">
                <i class="fas fa-edit"></i>
              </button>
              <button class="text-rose-500 hover:text-rose-400">
                <i class="fas fa-trash-alt"></i>
              </button>
              <button class="text-emerald-400 hover:text-emerald-300">
                <i class="fas fa-share-alt"></i>
              </button>
            </div>
          </td>
        </template>
      </DynamicTable>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';
import ExamCreator from '@components/activities/ExamCreator.vue';
import DynamicTable from '@/shared/DynamicTable.vue';

export default defineComponent({
  name: 'ExamCreatorView',
  components: {
    GlassCard,
    ExamCreator,
    DynamicTable
  },
  setup() {
    const headers = [
      { key: 'title', label: 'Título' },
      { key: 'subject', label: 'Matéria' },
      { key: 'duration', label: 'Duração' },
      { key: 'status', label: 'Status' },
      { key: 'actions', label: 'Ações' }
    ];

    const exams = ref([
      { id: 1, title: 'Prova de Matemática Básica', subject: 'Matemática', duration: 60, status: 'Publicada' },
      { id: 2, title: 'Avaliação de Literatura', subject: 'Português', duration: 45, status: 'Rascunho' },
      { id: 3, title: 'Teste de Ciências', subject: 'Ciências', duration: 30, status: 'Publicada' }
    ]);
    
    const statusClass = (status: 'Publicada' | 'Rascunho' | 'Arquivada') => {
      const classes: Record<'Publicada' | 'Rascunho' | 'Arquivada', string> = {
        'Publicada': 'bg-emerald-500/20 text-emerald-400',
        'Rascunho': 'bg-amber-500/20 text-amber-400',
        'Arquivada': 'bg-gray-500/20 text-gray-400'
      };
      return `px-3 py-1 rounded-full text-xs font-medium ${classes[status] ?? ''}`;
    };
    
    return {
      headers,
      exams,
      statusClass
    };
  }
});
</script>