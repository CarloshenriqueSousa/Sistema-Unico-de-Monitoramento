<template>
  <div 
    class="achievement-item group relative bg-white border border-[#e1d4c2] rounded-xl p-5 transition-all duration-300 hover:shadow-lg hover:border-[#2d531a] overflow-hidden"
  >
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5">
      <div class="absolute inset-0 bg-gradient-to-br from-[#2d531a] to-[#0f1e3f]"></div>
    </div>

    <div class="relative flex items-start gap-4">
      <!-- Icon Container -->
      <div 
        class="flex-shrink-0 w-14 h-14 rounded-xl bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center transform transition-transform group-hover:scale-110 group-hover:rotate-6"
      >
        <svg class="w-7 h-7 text-[#e1d4c2]" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      </div>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-[#1f1d20] text-lg mb-1 truncate">
          {{ achievement.title }}
        </h3>
        <p class="text-sm text-[#1f1d20]/60 line-clamp-2 mb-3">
          {{ achievement.description }}
        </p>

        <!-- Footer -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="inline-flex items-center px-3 py-1 rounded-full bg-[#2d531a]/10 text-[#2d531a] text-xs font-medium">
              <svg class="w-3.5 h-3.5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
              </svg>
              +{{ achievement.points }} pts
            </span>
          </div>
          <span class="text-xs text-[#1f1d20]/40">
            {{ achievement.date }}
          </span>
        </div>
      </div>
    </div>

    <!-- Hover Effect Line -->
    <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] transform scale-x-0 transition-transform group-hover:scale-x-100"></div>
  </div>
</template>

<script setup lang="ts">
interface Achievement {
  title: string;
  description: string;
  points: number;
  date: string;
}

defineProps<{
  achievement: Achievement;
}>();
</script>