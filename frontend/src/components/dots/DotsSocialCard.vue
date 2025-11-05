<template>
  <div class="dots-social-card bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-6">
    <h2 class="text-xl font-bold text-[#1f1d20] mb-4 flex items-center gap-2">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      Atividades Sociais
    </h2>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-3 text-center border border-[#e1d4c2]">
        <div class="text-2xl font-bold text-[#2d531a] mb-1">{{ data.projects }}</div>
        <div class="text-xs text-[#1f1d20]/60">Projetos</div>
      </div>
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-3 text-center border border-[#e1d4c2]">
        <div class="text-2xl font-bold text-[#2d531a] mb-1">{{ data.games }}</div>
        <div class="text-xs text-[#1f1d20]/60">Jogos</div>
      </div>
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-3 text-center border border-[#e1d4c2]">
        <div class="text-2xl font-bold text-[#0f1e3f] mb-1">{{ data.collaborations }}</div>
        <div class="text-xs text-[#1f1d20]/60">Colaborações</div>
      </div>
      <div class="stat-card bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 rounded-xl p-3 text-center border border-[#e1d4c2]">
        <div class="text-2xl font-bold text-[#0f1e3f] mb-1">{{ data.events }}</div>
        <div class="text-xs text-[#1f1d20]/60">Eventos</div>
      </div>
    </div>

    <!-- Network Visualization -->
    <div class="social-network relative h-40 mb-4 bg-[#e1d4c2]/20 rounded-xl flex items-center justify-center overflow-hidden">
      <div class="relative w-32 h-32">
        <!-- Center Node -->
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center text-white font-bold text-xs shadow-lg">
          Você
        </div>

        <!-- Surrounding Nodes -->
        <div 
          v-for="(node, i) in networkNodes" 
          :key="i"
          class="absolute w-8 h-8 rounded-full bg-[#e1d4c2] border-2 border-[#2d531a] flex items-center justify-center transform hover:scale-110 transition-transform"
          :style="{
            top: `${50 + Math.sin((i * 2 * Math.PI) / networkNodes.length) * 40}%`,
            left: `${50 + Math.cos((i * 2 * Math.PI) / networkNodes.length) * 40}%`,
            transform: 'translate(-50%, -50%)'
          }"
        >
          <div class="w-2 h-2 rounded-full bg-[#2d531a]"></div>
        </div>

        <!-- Connection Lines -->
        <svg class="absolute inset-0 w-full h-full pointer-events-none">
          <line 
            v-for="(node, i) in networkNodes" 
            :key="`line-${i}`"
            x1="50%" 
            y1="50%" 
            :x2="`${50 + Math.cos((i * 2 * Math.PI) / networkNodes.length) * 40}%`"
            :y2="`${50 + Math.sin((i * 2 * Math.PI) / networkNodes.length) * 40}%`"
            stroke="#2d531a" 
            stroke-width="1" 
            opacity="0.3"
          />
        </svg>
      </div>
    </div>

    <button class="w-full py-2.5 rounded-xl bg-[#e1d4c2] hover:bg-gradient-to-r hover:from-[#2d531a] hover:to-[#0f1e3f] text-[#1f1d20] hover:text-white font-medium transition-all text-sm">
      Explorar Atividades
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface SocialData {
  projects: number;
  games: number;
  collaborations: number;
  events: number;
}

defineProps<{
  data: SocialData;
}>();

const networkNodes = ref([1, 2, 3, 4, 5, 6]);
</script>