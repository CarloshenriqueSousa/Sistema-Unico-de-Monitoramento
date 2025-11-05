<template>
  <div 
    class="activity-item group relative bg-white border border-[#e1d4c2] rounded-xl p-4 transition-all duration-300 hover:shadow-md hover:border-[#2d531a] cursor-pointer"
  >
    <div class="flex items-start justify-between gap-4">
      <!-- Content -->
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-[#1f1d20] mb-1 truncate">
          {{ activity.title }}
        </h3>
        <p class="text-sm text-[#1f1d20]/60 truncate">
          {{ activity.subject }}
        </p>
      </div>

      <!-- Due Date Badge -->
      <span class="flex-shrink-0 inline-flex items-center px-3 py-1 rounded-full bg-[#e1d4c2] text-[#1f1d20] text-xs font-medium">
        {{ activity.dueDate }}
      </span>
    </div>

    <!-- Status -->
    <div class="mt-3 flex items-center gap-2">
      <span class="text-xs text-[#1f1d20]/50 font-medium">Status:</span>
      <span 
        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
        :class="statusClass"
      >
        <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDotClass"></span>
        {{ statusText }}
      </span>
    </div>

    <!-- Hover Indicator -->
    <div class="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
      <svg class="w-5 h-5 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Activity {
  title: string;
  subject: string;
  dueDate: string;
  status: 'pending' | 'completed' | 'late';
}

const props = defineProps<{
  activity: Activity;
}>();

const statusText = computed(() => ({
  pending: 'Pendente',
  completed: 'Concluída',
  late: 'Atrasada'
}[props.activity.status]));

const statusClass = computed(() => ({
  pending: 'bg-[#2d531a]/10 text-[#2d531a]',
  completed: 'bg-[#2d531a]/10 text-[#2d531a]',
  late: 'bg-red-50 text-red-600'
}[props.activity.status]));

const statusDotClass = computed(() => ({
  pending: 'bg-[#2d531a]',
  completed: 'bg-[#2d531a]',
  late: 'bg-red-500 animate-pulse'
}[props.activity.status]));
</script>