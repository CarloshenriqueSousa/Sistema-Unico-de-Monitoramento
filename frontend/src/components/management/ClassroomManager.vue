<template>
  <div class="classroom-manager bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-bold text-white">Gerenciador de Salas</h3>
            <p class="text-white/70 text-sm">Organize alunos e grupos</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button 
            @click="showMap = !showMap"
            class="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition-all flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMap" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
            {{ showMap ? 'Ver Lista' : 'Ver Mapa' }}
          </button>
          <button 
            @click="saveClassroom"
            :disabled="saving"
            class="px-4 py-2 rounded-lg bg-white text-[#2d531a] hover:bg-white/90 font-medium transition-all flex items-center gap-2"
          >
            <div v-if="saving" class="w-4 h-4 border-2 border-[#2d531a] border-t-transparent rounded-full animate-spin"></div>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            Salvar
          </button>
        </div>
      </div>
    </div>

    <div class="p-6">
      <!-- View Toggle -->
      <div v-if="showMap" class="mb-6">
        <div class="flex items-center gap-3 mb-4">
          <button 
            v-for="view in views" 
            :key="view.id"
            @click="activeView = view.id"
            class="px-4 py-2.5 rounded-xl font-medium text-sm transition-all"
            :class="activeView === view.id 
              ? 'bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white shadow-md' 
              : 'bg-[#e1d4c2]/30 text-[#1f1d20] hover:bg-[#e1d4c2]'"
          >
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            {{ view.label }}
          </button>
        </div>

        <!-- Classroom Visualization -->
        <div class="bg-[#e1d4c2]/10 rounded-xl p-8 min-h-[500px] border-2 border-dashed border-[#e1d4c2]">
          <div class="text-center py-20">
            <div class="w-20 h-20 mx-auto mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
              <svg class="w-10 h-10 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <p class="text-[#1f1d20] font-medium mb-2">Visualização {{ activeView === '3d' ? '3D' : '2D' }}</p>
            <p class="text-sm text-[#1f1d20]/60">Mapa da sala será renderizado aqui</p>
          </div>
        </div>
      </div>

      <!-- Student List View -->
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="student in students" 
            :key="student.id"
            @click="toggleStudentSelection(student)"
            class="student-card group relative bg-white border-2 rounded-xl p-4 cursor-pointer transition-all"
            :class="isSelected(student) ? 'border-[#2d531a] bg-[#e1d4c2]/20' : 'border-[#e1d4c2] hover:border-[#2d531a]/50'"
          >
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center text-white font-bold">
                {{ getInitials(student.nome) }}
              </div>
              <div class="flex-1">
                <h4 class="font-semibold text-[#1f1d20]">{{ student.nome }}</h4>
                <div class="flex gap-2 mt-1">
                  <span class="text-xs px-2 py-0.5 rounded-full bg-[#2d531a]/10 text-[#2d531a]">
                    H: {{ student.skills.humanas }}%
                  </span>
                  <span class="text-xs px-2 py-0.5 rounded-full bg-[#0f1e3f]/10 text-[#0f1e3f]">
                    E: {{ student.skills.exatas }}%
                  </span>
                </div>
              </div>
              <div v-if="isSelected(student)" class="absolute top-2 right-2">
                <svg class="w-5 h-5 text-[#2d531a]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Group Management Section -->
      <div v-if="selectedStudents.length > 0" class="mt-8 p-6 bg-[#e1d4c2]/20 rounded-xl border border-[#e1d4c2]">
        <h4 class="text-lg font-bold text-[#1f1d20] mb-4">
          Alunos Selecionados ({{ selectedStudents.length }})
        </h4>
        <div class="flex flex-wrap gap-2 mb-4">
          <div 
            v-for="student in selectedStudents" 
            :key="student.id"
            class="inline-flex items-center gap-2 px-3 py-2 bg-white rounded-lg border border-[#e1d4c2]"
          >
            <span class="text-sm font-medium text-[#1f1d20]">{{ student.nome.split(' ')[0] }}</span>
            <button 
              @click="toggleStudentSelection(student)"
              class="text-[#1f1d20]/40 hover:text-red-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <button 
          @click="createGroup"
          class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-medium hover:shadow-lg transition-all"
        >
          Criar Grupo com Selecionados
        </button>
      </div>

      <!-- Recommendations -->
      <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="p-5 bg-white border border-[#e1d4c2] rounded-xl">
          <h4 class="font-bold text-[#1f1d20] mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-[#2d531a]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
            </svg>
            Dados da Turma
          </h4>
          <div class="space-y-2 text-sm text-[#1f1d20]/70">
            <div class="flex justify-between">
              <span>Total de Alunos</span>
              <span class="font-semibold text-[#2d531a]">{{ students.length }}</span>
            </div>
            <div class="flex justify-between">
              <span>Grupos Criados</span>
              <span class="font-semibold text-[#0f1e3f]">{{ groups.length }}</span>
            </div>
            <div class="flex justify-between">
              <span>Selecionados</span>
              <span class="font-semibold text-[#2d531a]">{{ selectedStudents.length }}</span>
            </div>
          </div>
        </div>

        <div class="p-5 bg-[#2d531a]/5 border border-[#2d531a]/20 rounded-xl">
          <h4 class="font-bold text-[#1f1d20] mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-[#2d531a]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
            </svg>
            Recomendações
          </h4>
          <ul class="space-y-2 text-sm text-[#1f1d20]/70">
            <li v-for="(rec, i) in recommendations" :key="i" class="flex items-start gap-2">
              <span class="text-[#2d531a] mt-0.5">•</span>
              <span>{{ rec }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Student {
  id: string;
  nome: string;
  skills: {
    humanas: number;
    exatas: number;
    linguagens: number;
  };
}

const showMap = ref(false);
const activeView = ref('3d');
const saving = ref(false);
const selectedStudents = ref<Student[]>([]);

const views = [
  { id: '3d', label: 'Visão 3D' },
  { id: '2d', label: 'Visão Grade' }
];

// Mock data
const students = ref<Student[]>([
  { id: '1', nome: 'João Silva', skills: { humanas: 85, exatas: 78, linguagens: 90 } },
  { id: '2', nome: 'Maria Santos', skills: { humanas: 92, exatas: 88, linguagens: 85 } },
  { id: '3', nome: 'Pedro Costa', skills: { humanas: 75, exatas: 95, linguagens: 80 } },
  { id: '4', nome: 'Ana Lima', skills: { humanas: 88, exatas: 72, linguagens: 92 } }
]);

const groups = ref([]);

const recommendations = computed(() => [
  'Posicionar alunos com dificuldades visuais nas primeiras fileiras',
  'Combinar alunos com habilidades complementares',
  'Criar grupos de 4-6 alunos para atividades colaborativas'
]);

const getInitials = (name: string) => {
  const parts = name.split(' ');
  return parts.length >= 2 ? `${parts[0][0]}${parts[1][0]}` : name.substring(0, 2);
};

const isSelected = (student: Student) => {
  return selectedStudents.value.some(s => s.id === student.id);
};

const toggleStudentSelection = (student: Student) => {
  const index = selectedStudents.value.findIndex(s => s.id === student.id);
  if (index >= 0) {
    selectedStudents.value.splice(index, 1);
  } else {
    selectedStudents.value.push(student);
  }
};

const createGroup = () => {
  console.log('Creating group with:', selectedStudents.value);
  selectedStudents.value = [];
};

const saveClassroom = () => {
  saving.value = true;
  setTimeout(() => {
    saving.value = false;
    console.log('Classroom saved');
  }, 1000);
};
</script>