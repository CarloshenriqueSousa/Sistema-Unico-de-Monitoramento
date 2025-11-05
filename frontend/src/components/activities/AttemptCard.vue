<template>
  <div class="attempt-card group relative bg-white border border-[#e1d4c2] rounded-xl p-5 transition-all duration-300 hover:shadow-md hover:border-[#2d531a] cursor-pointer">
    <!-- Header -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center text-white font-bold text-sm">
          #{{ attempt.id }}
        </div>
        <div>
          <h3 class="font-semibold text-[#1f1d20]">{{ attempt.studentName }}</h3>
          <p class="text-xs text-[#1f1d20]/50">Tentativa {{ attempt.id }}</p>
        </div>
      </div>

      <!-- Score Badge -->
      <div class="text-right">
        <div 
          class="inline-flex items-center px-3 py-1.5 rounded-lg font-bold text-lg"
          :class="scoreClass"
        >
          {{ attempt.score }}
        </div>
        <p class="text-xs text-[#1f1d20]/50 mt-1">Nota</p>
      </div>
    </div>

    <!-- Details -->
    <div class="space-y-2">
      <div class="flex items-center justify-between py-2 border-t border-[#e1d4c2]">
        <div class="flex items-center gap-2 text-sm text-[#1f1d20]/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>Data de Entrega</span>
        </div>
        <span class="text-sm font-medium text-[#1f1d20]">{{ attempt.date }}</span>
      </div>

      <div v-if="attempt.timeSpent" class="flex items-center justify-between py-2">
        <div class="flex items-center gap-2 text-sm text-[#1f1d20]/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Tempo Gasto</span>
        </div>
        <span class="text-sm font-medium text-[#1f1d20]">{{ attempt.timeSpent }}</span>
      </div>

      <div v-if="attempt.correctAnswers !== undefined" class="flex items-center justify-between py-2">
        <div class="flex items-center gap-2 text-sm text-[#1f1d20]/60">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Acertos</span>
        </div>
        <span class="text-sm font-medium text-[#1f1d20]">
          {{ attempt.correctAnswers }} / {{ attempt.totalQuestions }}
        </span>
      </div>
    </div>

    <!-- Action Button -->
    <button class="w-full mt-4 py-2.5 rounded-lg bg-[#e1d4c2] hover:bg-gradient-to-r hover:from-[#2d531a] hover:to-[#0f1e3f] text-[#1f1d20] hover:text-white font-medium transition-all flex items-center justify-center gap-2 group-hover:shadow-md">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
      Ver Detalhes
    </button>

    <!-- Hover Indicator -->
    <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
      <svg class="w-5 h-5 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Attempt {
  id: number;
  studentName: string;
  score: number;
  date: string;
  timeSpent?: string;
  correctAnswers?: number;
  totalQuestions?: number;
}

const props = defineProps<{
  attempt: Attempt;
}>();

const scoreClass = computed(() => {
  const score = props.attempt.score;
  if (score >= 9) return 'bg-[#2d531a]/10 text-[#2d531a]';
  if (score >= 7) return 'bg-[#0f1e3f]/10 text-[#0f1e3f]';
  if (score >= 5) return 'bg-yellow-50 text-yellow-700';
  return 'bg-red-50 text-red-600';
});
</script>