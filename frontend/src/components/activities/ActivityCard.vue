<template>
  <div 
    class="activity-card group relative bg-white border border-[#e1d4c2] rounded-2xl p-6 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer"
    @click="$emit('open')"
  >
    <!-- Background Gradient -->
    <div class="absolute inset-0 bg-gradient-to-br from-[#e1d4c2]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>

    <!-- Priority Badge -->
    <div v-if="priority === 'high'" class="absolute top-4 right-4">
      <span class="inline-flex items-center px-3 py-1 rounded-full bg-red-500 text-white text-xs font-bold animate-pulse">
        URGENTE
      </span>
    </div>

    <!-- Status Indicator -->
    <div class="absolute top-6 left-6 w-2 h-2 rounded-full" :class="statusIndicatorClass"></div>

    <div class="relative">
      <!-- Header -->
      <div class="mb-4">
        <div class="flex items-start justify-between mb-2">
          <h4 class="text-xl font-bold text-[#1f1d20] pr-8">
            {{ title }}
          </h4>
        </div>
        
        <!-- Deadline -->
        <div class="flex items-center text-sm text-[#1f1d20]/60">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          {{ deadline }}
        </div>
      </div>

      <!-- Status Badge -->
      <div class="mb-4">
        <span class="inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium" :class="statusBadgeClass">
          <span class="w-1.5 h-1.5 rounded-full mr-2" :class="statusDotClass"></span>
          {{ statusText }}
        </span>
      </div>

      <!-- Progress Bar -->
      <div class="mb-5">
        <div class="flex items-center justify-between mb-2 text-xs">
          <span class="text-[#1f1d20]/60 font-medium">Progresso</span>
          <span class="text-[#1f1d20] font-bold">{{ progress }}%</span>
        </div>
        <div class="h-2 bg-[#e1d4c2] rounded-full overflow-hidden">
          <div 
            class="h-full rounded-full transition-all duration-500 ease-out"
            :class="progressBarClass"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between">
        <!-- Participants -->
        <div class="flex -space-x-2">
          <div 
            v-for="(participant, idx) in participants.slice(0, 3)" 
            :key="idx"
            class="w-8 h-8 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] border-2 border-white flex items-center justify-center text-xs text-white font-semibold"
            :title="participant.name"
          >
            {{ participant.initials }}
          </div>
          <div 
            v-if="participants.length > 3"
            class="w-8 h-8 rounded-full bg-[#e1d4c2] border-2 border-white flex items-center justify-center text-xs text-[#1f1d20] font-semibold"
          >
            +{{ participants.length - 3 }}
          </div>
        </div>

        <!-- Action Button -->
        <button 
          class="px-4 py-2 rounded-lg bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white text-sm font-medium transition-all hover:shadow-lg hover:scale-105"
        >
          Abrir
        </button>
      </div>
    </div>

    <!-- Hover Border Effect -->
    <div class="absolute inset-0 rounded-2xl border-2 border-[#2d531a] opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Participant {
  id: string;
  name: string;
  initials: string;
}

const props = withDefaults(defineProps<{
  title: string;
  deadline: string;
  status?: 'pending' | 'in_progress' | 'completed' | 'late';
  priority?: 'low' | 'medium' | 'high';
  progress?: number;
  participants?: Participant[];
}>(), {
  status: 'pending',
  priority: 'medium',
  progress: 0,
  participants: () => []
});

defineEmits<{
  open: [];
}>();

const statusIndicatorClass = computed(() => ({
  pending: 'bg-[#2d531a]',
  in_progress: 'bg-[#0f1e3f]',
  completed: 'bg-[#2d531a]',
  late: 'bg-red-500'
}[props.status]));

const statusBadgeClass = computed(() => ({
  pending: 'bg-[#2d531a]/10 text-[#2d531a]',
  in_progress: 'bg-[#0f1e3f]/10 text-[#0f1e3f]',
  completed: 'bg-[#2d531a]/10 text-[#2d531a]',
  late: 'bg-red-50 text-red-600'
}[props.status]));

const statusDotClass = computed(() => ({
  pending: 'bg-[#2d531a]',
  in_progress: 'bg-[#0f1e3f] animate-pulse',
  completed: 'bg-[#2d531a]',
  late: 'bg-red-500 animate-pulse'
}[props.status]));

const progressBarClass = computed(() => ({
  pending: 'bg-[#2d531a]',
  in_progress: 'bg-[#0f1e3f]',
  completed: 'bg-[#2d531a]',
  late: 'bg-red-500'
}[props.status]));

const statusText = computed(() => ({
  pending: 'Pendente',
  in_progress: 'Em Progresso',
  completed: 'Concluído',
  late: 'Atrasado'
}[props.status]));
</script>