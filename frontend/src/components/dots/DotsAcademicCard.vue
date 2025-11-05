<template>
  <div class="dots-academic-card bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-6">
    <h2 class="text-xl font-bold text-[#1f1d20] mb-4 flex items-center gap-2">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M12 14l9-5-9-5-9 5 9 5z" />
          <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
        </svg>
      </div>
      Desempenho Acadêmico
    </h2>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-4 text-center border border-[#e1d4c2] hover:border-[#2d531a] transition-all">
        <div class="text-3xl font-bold text-[#2d531a] mb-1">{{ data.grades }}</div>
        <div class="text-xs text-[#1f1d20]/60">Nota Média</div>
      </div>
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-4 text-center border border-[#e1d4c2] hover:border-[#2d531a] transition-all">
        <div class="text-3xl font-bold text-[#0f1e3f] mb-1">{{ data.books }}</div>
        <div class="text-xs text-[#1f1d20]/60">Livros Lidos</div>
      </div>
    </div>

    <!-- Subjects Progress -->
    <div class="mb-4">
      <h3 class="text-sm font-semibold text-[#1f1d20] mb-3">Por Matéria</h3>
      <div class="space-y-3">
        <div 
          v-for="(subject, index) in data.subjects" 
          :key="index"
          class="subject-item"
        >
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm text-[#1f1d20]">{{ subject.name }}</span>
            <span class="text-sm font-bold text-[#2d531a]">{{ subject.grade }}</span>
          </div>
          <div class="w-full h-2 bg-[#e1d4c2] rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] rounded-full transition-all duration-1000 ease-out"
              :style="{ width: `${subject.grade * 10}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <button class="w-full py-2.5 rounded-xl bg-[#e1d4c2] hover:bg-gradient-to-r hover:from-[#2d531a] hover:to-[#0f1e3f] text-[#1f1d20] hover:text-white font-medium transition-all text-sm">
      Ver Detalhes
    </button>
  </div>
</template>

<script setup lang="ts">
interface AcademicData {
  grades: number;
  books: number;
  subjects: { name: string; grade: number }[];
}

defineProps<{
  data: AcademicData;
}>();
</script>