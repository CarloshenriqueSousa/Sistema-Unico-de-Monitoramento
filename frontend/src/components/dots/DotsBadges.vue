<template>
  <div class="dots-badges bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-6">
    <h2 class="text-2xl font-bold text-[#1f1d20] mb-6 flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
        <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      </div>
      Minhas Conquistas
    </h2>

    <div class="grid grid-cols-2 gap-4 mb-6">
      <div 
        v-for="(badge, index) in badges" 
        :key="index"
        class="badge-card group relative aspect-square rounded-2xl overflow-hidden border-2 border-[#e1d4c2] hover:border-[#2d531a] transition-all duration-300 hover:shadow-xl hover:-translate-y-2 cursor-pointer"
      >
        <!-- Background Gradient -->
        <div class="absolute inset-0 bg-gradient-to-br from-[#2d531a]/10 to-[#0f1e3f]/10 group-hover:from-[#2d531a]/20 group-hover:to-[#0f1e3f]/20 transition-all"></div>

        <!-- Content -->
        <div class="relative h-full flex flex-col items-center justify-center p-4 text-center">
          <!-- Icon Circle -->
          <div class="w-16 h-16 mb-3 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-12 transition-all shadow-lg">
            <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>

          <!-- Badge Name -->
          <span class="font-semibold text-[#1f1d20] text-sm leading-tight">
            {{ badge }}
          </span>
        </div>

        <!-- Shine Effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
      </div>
    </div>

    <button class="w-full py-3 rounded-xl bg-[#e1d4c2] hover:bg-gradient-to-r hover:from-[#2d531a] hover:to-[#0f1e3f] text-[#1f1d20] hover:text-white font-medium transition-all">
      Ver Todas as Conquistas
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  badges: string[];
}>();
</script>