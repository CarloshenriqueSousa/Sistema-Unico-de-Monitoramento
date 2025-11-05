<template>
  <div class="dots-technical-card bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-6">
    <h2 class="text-xl font-bold text-[#1f1d20] mb-4 flex items-center gap-2">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
      </div>
      Habilidades Técnicas
    </h2>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-4 text-center border border-[#e1d4c2] hover:border-[#2d531a] transition-all">
        <div class="text-3xl font-bold text-[#2d531a] mb-1">{{ data.projects }}</div>
        <div class="text-xs text-[#1f1d20]/60">Projetos</div>
      </div>
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-4 text-center border border-[#e1d4c2] hover:border-[#0f1e3f] transition-all">
        <div class="text-3xl font-bold text-[#0f1e3f] mb-1">{{ data.certifications }}</div>
        <div class="text-xs text-[#1f1d20]/60">Certificados</div>
      </div>
    </div>

    <!-- Skills Tags -->
    <div class="mb-4">
      <h3 class="text-sm font-semibold text-[#1f1d20] mb-3">Tecnologias</h3>
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="(skill, index) in data.skills" 
          :key="index"
          class="skill-badge px-3 py-1.5 rounded-full bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white text-xs font-medium transform hover:scale-110 transition-all cursor-pointer shadow-sm"
        >
          {{ skill }}
        </span>
      </div>
    </div>

    <!-- Skill Level Pyramid -->
    <div class="pyramid-visualization mb-4">
      <div class="relative h-32 flex items-end justify-center">
        <div class="flex items-end gap-1">
          <div class="w-12 h-8 bg-[#2d531a]/20 rounded-t" title="Básico"></div>
          <div class="w-12 h-16 bg-[#2d531a]/40 rounded-t" title="Intermediário"></div>
          <div class="w-12 h-24 bg-[#2d531a]/60 rounded-t" title="Avançado"></div>
          <div class="w-12 h-32 bg-gradient-to-t from-[#2d531a] to-[#0f1e3f] rounded-t" title="Expert"></div>
        </div>
        
        <!-- Labels -->
        <div class="absolute bottom-0 left-0 right-0 flex justify-center gap-1 -mb-6">
          <span class="text-xs text-[#1f1d20]/40 w-12 text-center">Básico</span>
          <span class="text-xs text-[#1f1d20]/40 w-12 text-center">Inter.</span>
          <span class="text-xs text-[#1f1d20]/40 w-12 text-center">Avanç.</span>
          <span class="text-xs text-[#1f1d20]/60 w-12 text-center font-semibold">Expert</span>
        </div>
      </div>
    </div>

    <button class="w-full py-2.5 rounded-xl bg-[#e1d4c2] hover:bg-gradient-to-r hover:from-[#2d531a] hover:to-[#0f1e3f] text-[#1f1d20] hover:text-white font-medium transition-all text-sm mt-6">
      Ver Todas as Habilidades
    </button>
  </div>
</template>

<script setup lang="ts">
interface TechnicalData {
  skills: string[];
  projects: number;
  certifications: number;
}

defineProps<{
  data: TechnicalData;
}>();
</script>