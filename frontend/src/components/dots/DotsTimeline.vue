<template>
  <div class="dots-timeline bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-6">
    <h2 class="text-2xl font-bold text-[#1f1d20] mb-6 flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center">
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      Linha do Tempo
    </h2>

    <div class="relative pl-8">
      <!-- Vertical Line -->
      <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-[#2d531a] to-[#0f1e3f] rounded-full"></div>

      <!-- Events -->
      <div 
        v-for="(event, index) in events" 
        :key="index"
        class="relative mb-8 last:mb-0 group"
      >
        <!-- Marker -->
        <div class="absolute -left-11 top-2 w-8 h-8 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center transform group-hover:scale-125 transition-transform shadow-lg">
          <div class="w-3 h-3 rounded-full bg-white"></div>
        </div>

        <!-- Event Card -->
        <div class="bg-[#e1d4c2]/20 hover:bg-[#e1d4c2]/40 border border-[#e1d4c2] rounded-xl p-4 transition-all duration-300 group-hover:shadow-lg group-hover:-translate-y-1">
          <div class="flex items-center gap-2 text-[#2d531a] font-semibold mb-2 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {{ event.date }}
          </div>
          <p class="text-[#1f1d20] leading-relaxed">{{ event.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Event {
  date: string;
  description: string;
}

defineProps<{
  events: Event[];
}>();
</script>