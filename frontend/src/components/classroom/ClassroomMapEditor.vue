<template>
  <div class="classroom-map-editor bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Editor de Mapa da Sala</h3>
          <p class="text-white/70 text-sm">Posicione alunos no mapa interativo</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Control Panel -->
        <div class="space-y-5">
          <!-- Available Students -->
          <div>
            <h4 class="font-semibold text-[#1f1d20] mb-3 flex items-center justify-between">
              <span>Alunos Disponíveis</span>
              <span class="text-xs px-2 py-1 rounded-full bg-[#2d531a]/10 text-[#2d531a]">
                {{ availableStudents.length }}
              </span>
            </h4>
            <div class="space-y-2 max-h-[400px] overflow-y-auto pr-2">
              <div 
                v-for="student in availableStudents" 
                :key="student.id"
                draggable="true"
                @dragstart="startDrag($event, student)"
                class="student-card bg-[#e1d4c2]/30 hover:bg-[#e1d4c2] border border-[#e1d4c2] p-3 rounded-lg flex items-center gap-3 cursor-move transition-all"
              >
                <div 
                  class="w-3 h-3 rounded-full flex-shrink-0"
                  :class="student.visionIssues ? 'bg-purple-500' : 'bg-[#2d531a]'"
                ></div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-[#1f1d20] truncate">{{ student.name }}</p>
                  <p v-if="student.visionIssues" class="text-xs text-purple-600">Dificuldade visual</p>
                </div>
                <svg class="w-4 h-4 text-[#1f1d20]/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div>
            <h4 class="font-semibold text-[#1f1d20] mb-3">Ações Rápidas</h4>
            <div class="space-y-2">
              <button 
                @click="autoArrange"
                class="w-full py-2.5 px-4 rounded-lg bg-[#e1d4c2]/30 hover:bg-[#e1d4c2] text-[#1f1d20] font-medium transition-all text-sm flex items-center justify-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Auto-organizar
              </button>
              <button 
                @click="clearAll"
                class="w-full py-2.5 px-4 rounded-lg bg-[#e1d4c2]/30 hover:bg-[#e1d4c2] text-[#1f1d20] font-medium transition-all text-sm flex items-center justify-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Limpar Tudo
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="space-y-2 pt-4 border-t border-[#e1d4c2]">
            <button 
              @click="$emit('toggle-edit', false)"
              class="w-full py-2.5 px-4 rounded-lg bg-[#e1d4c2] hover:bg-[#e1d4c2]/70 text-[#1f1d20] font-medium transition-all"
            >
              Cancelar
            </button>
            <button 
              @click="saveLayout"
              class="w-full py-2.5 px-4 rounded-lg bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] text-white font-semibold transition-all hover:shadow-lg"
            >
              Salvar Layout
            </button>
          </div>
        </div>

        <!-- Map Area -->
        <div class="lg:col-span-3">
          <div 
            class="map-area relative bg-[#e1d4c2]/10 rounded-xl p-8 min-h-[700px] border-2 border-dashed border-[#e1d4c2]"
            @drop="dropOnMap($event)"
            @dragover.prevent
          >
            <!-- Board -->
            <div class="absolute top-4 left-1/2 -translate-x-1/2 w-3/4 h-14 bg-[#1f1d20] rounded-lg flex items-center justify-center z-10">
              <span class="text-white font-semibold">QUADRO</span>
            </div>

            <!-- Positioned Students -->
            <div 
              v-for="(student, index) in positionedStudents" 
              :key="student.id"
              class="positioned-student absolute w-20 h-20 rounded-full border-4 border-white shadow-lg cursor-move transition-all"
              :class="{
                'bg-gradient-to-br from-[#2d531a] to-[#0f1e3f]': !student.visionIssues,
                'bg-gradient-to-br from-purple-500 to-purple-700': student.visionIssues,
                'ring-4 ring-amber-400': selectedStudentId === student.id
              }"
              :style="{
                left: `${student.position.x}px`,
                top: `${student.position.y}px`,
                transform: 'translate(-50%, -50%)'
              }"
              draggable="true"
              @dragstart="startDragPositioned($event, student, index)"
              @click="selectStudent(student.id)"
            >
              <div class="w-full h-full flex items-center justify-center text-white font-bold text-xs text-center p-2">
                {{ student.name.split(' ')[0] }}
              </div>

              <!-- Remove Button -->
              <button 
                @click.stop="removeStudent(index)"
                class="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-red-500 hover:bg-red-600 text-white flex items-center justify-center transition-all z-20"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <!-- Vision Issue Indicator -->
              <div v-if="student.visionIssues" class="absolute -bottom-1 left-1/2 -translate-x-1/2">
                <div class="w-4 h-4 rounded-full bg-purple-500 border-2 border-white flex items-center justify-center">
                  <svg class="w-2.5 h-2.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="positionedStudents.length === 0" class="absolute inset-0 flex items-center justify-center text-center p-8">
              <div>
                <svg class="w-16 h-16 mx-auto mb-4 text-[#1f1d20]/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <p class="text-[#1f1d20] font-medium mb-2">Nenhum aluno posicionado</p>
                <p class="text-sm text-[#1f1d20]/60">Arraste os alunos da lista para o mapa</p>
              </div>
            </div>

            <!-- Stats -->
            <div class="absolute bottom-4 right-4 bg-white border border-[#e1d4c2] rounded-lg p-3 shadow-md">
              <div class="space-y-1 text-sm">
                <div class="flex items-center gap-3">
                  <span class="text-[#1f1d20]/60">Posicionados:</span>
                  <span class="font-bold text-[#2d531a]">{{ positionedStudents.length }}</span>
                </div>
                <div class="flex items-center gap-3">
                  <span class="text-[#1f1d20]/60">Disponíveis:</span>
                  <span class="font-bold text-[#0f1e3f]">{{ availableStudents.length }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Student {
  id: string;
  name: string;
  visionIssues?: boolean;
  position: { x: number; y: number };
}

const props = defineProps<{
  classroomId: string;
}>();

const emit = defineEmits<{
  'toggle-edit': [value: boolean];
  'position-change': [studentId: string, position: { x: number; y: number; z: number }];
}>();

// Lista de alunos será carregada via props ou API
const allStudents = ref<Student[]>([]);

const positionedStudents = ref<Student[]>([]);
const selectedStudentId = ref<string | null>(null);

const availableStudents = computed(() => {
  const positionedIds = new Set(positionedStudents.value.map(s => s.id));
  return allStudents.value.filter(s => !positionedIds.has(s.id));
});

let draggedStudent: Student | null = null;
let draggedIndex = -1;

const startDrag = (event: DragEvent, student: Student) => {
  draggedStudent = { ...student };
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'copy';
  }
};

const startDragPositioned = (event: DragEvent, student: Student, index: number) => {
  draggedStudent = student;
  draggedIndex = index;
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move';
  }
};

const dropOnMap = (event: DragEvent) => {
  event.preventDefault();
  if (!draggedStudent) return;

  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  if (draggedIndex >= 0) {
    // Moving existing student
    positionedStudents.value[draggedIndex].position = { x, y };
  } else {
    // Adding new student
    positionedStudents.value.push({
      ...draggedStudent,
      position: { x, y }
    });
  }

  draggedStudent = null;
  draggedIndex = -1;
};

const removeStudent = (index: number) => {
  positionedStudents.value.splice(index, 1);
  selectedStudentId.value = null;
};

const selectStudent = (studentId: string) => {
  selectedStudentId.value = studentId;
};

const autoArrange = () => {
  // Simple grid arrangement
  const startX = 150;
  const startY = 150;
  const spacingX = 120;
  const spacingY = 120;
  const cols = 5;

  availableStudents.value.forEach((student, index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    
    positionedStudents.value.push({
      ...student,
      position: {
        x: startX + col * spacingX,
        y: startY + row * spacingY
      }
    });
  });
};

const clearAll = () => {
  positionedStudents.value = [];
  selectedStudentId.value = null;
};

const saveLayout = async () => {
  const layout = positionedStudents.value.map(s => ({
    studentId: s.id,
    position: s.position
  }));
  
  // Emitir evento para salvar via API
  emit('save-layout', layout);
  emit('toggle-edit', false);
};
</script>

<style scoped>
.map-area {
  background-image: 
    radial-gradient(circle, rgba(45, 83, 26, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
}

.student-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.15);
}

.positioned-student {
  transition: all 0.2s ease;
  will-change: transform;
}

.positioned-student:hover {
  transform: translate(-50%, -50%) scale(1.1);
  z-index: 50;
}

/* Custom scrollbar */
.space-y-2::-webkit-scrollbar {
  width: 6px;
}

.space-y-2::-webkit-scrollbar-track {
  background: #e1d4c2;
  border-radius: 3px;
}

.space-y-2::-webkit-scrollbar-thumb {
  background: #2d531a;
  border-radius: 3px;
}

.space-y-2::-webkit-scrollbar-thumb:hover {
  background: #0f1e3f;
}
</style>