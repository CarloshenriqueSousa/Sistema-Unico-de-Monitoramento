<template>
  <div class="dots-profile min-h-screen bg-gradient-to-br from-[#e1d4c2] via-white to-[#e1d4c2] p-6 overflow-hidden">
    <!-- Decorative Background Pattern -->
    <div class="absolute inset-0 opacity-5">
      <div class="absolute inset-0" style="background-image: radial-gradient(circle, #2d531a 1px, transparent 1px); background-size: 50px 50px;"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
        <div>
          <h1 class="text-4xl md:text-5xl font-bold text-[#1f1d20] mb-2">
            {{ userName }}
          </h1>
          <p class="text-lg text-[#2d531a] font-medium">Perfil DOTS - Desenvolvimento Técnico Social</p>
        </div>

        <!-- Avatar Circle -->
        <div class="relative w-32 h-32">
          <div class="absolute inset-0 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] animate-pulse"></div>
          <div class="absolute inset-2 rounded-full bg-white flex items-center justify-center">
            <div class="w-20 h-20 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] flex items-center justify-center text-white font-bold text-2xl">
              {{ getInitials(userName) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-3 mb-8">
        <button 
          @click="shareProfile"
          class="px-6 py-3 rounded-xl bg-white border-2 border-[#e1d4c2] hover:border-[#2d531a] text-[#1f1d20] font-medium transition-all hover:shadow-lg flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
          Compartilhar
        </button>
        <button 
          @click="updateProfile"
          class="px-6 py-3 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-medium transition-all hover:shadow-lg flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Atualizar Perfil
        </button>
      </div>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Timeline Column -->
        <div class="lg:col-span-1">
          <DotsTimeline :events="events" />
        </div>

        <!-- Badges Column -->
        <div class="lg:col-span-1">
          <DotsBadges :badges="badges" />
        </div>

        <!-- Cards Column -->
        <div class="lg:col-span-1 space-y-6">
          <DotsAcademicCard :data="academicData" />
          <DotsSocialCard :data="socialData" />
          <DotsTechnicalCard :data="technicalData" />
        </div>
      </div>

      <!-- Overall Progress -->
      <div class="bg-white rounded-2xl shadow-lg border border-[#e1d4c2] p-8">
        <h2 class="text-2xl font-bold text-[#1f1d20] mb-6">Progresso Geral</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Academic Progress -->
          <div class="text-center">
            <div class="relative w-40 h-40 mx-auto mb-4">
              <svg class="w-full h-full transform -rotate-90">
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="#e1d4c2"
                  stroke-width="12"
                  fill="none"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="url(#academicGradient)"
                  stroke-width="12"
                  fill="none"
                  :stroke-dasharray="`${(academicProgress / 100) * 440} 440`"
                  class="transition-all duration-1000"
                />
                <defs>
                  <linearGradient id="academicGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#2d531a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#0f1e3f;stop-opacity:1" />
                  </linearGradient>
                </defs>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-3xl font-bold text-[#2d531a]">{{ Math.round(academicProgress) }}%</span>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-[#1f1d20] mb-1">Acadêmico</h3>
            <p class="text-sm text-[#1f1d20]/60">Desempenho escolar</p>
          </div>

          <!-- Social Progress -->
          <div class="text-center">
            <div class="relative w-40 h-40 mx-auto mb-4">
              <svg class="w-full h-full transform -rotate-90">
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="#e1d4c2"
                  stroke-width="12"
                  fill="none"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="url(#socialGradient)"
                  stroke-width="12"
                  fill="none"
                  :stroke-dasharray="`${(socialProgress / 100) * 440} 440`"
                  class="transition-all duration-1000"
                />
                <defs>
                  <linearGradient id="socialGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#2d531a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#0f1e3f;stop-opacity:1" />
                  </linearGradient>
                </defs>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-3xl font-bold text-[#2d531a]">{{ Math.round(socialProgress) }}%</span>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-[#1f1d20] mb-1">Social</h3>
            <p class="text-sm text-[#1f1d20]/60">Interação e colaboração</p>
          </div>

          <!-- Technical Progress -->
          <div class="text-center">
            <div class="relative w-40 h-40 mx-auto mb-4">
              <svg class="w-full h-full transform -rotate-90">
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="#e1d4c2"
                  stroke-width="12"
                  fill="none"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  stroke="url(#technicalGradient)"
                  stroke-width="12"
                  fill="none"
                  :stroke-dasharray="`${(technicalProgress / 100) * 440} 440`"
                  class="transition-all duration-1000"
                />
                <defs>
                  <linearGradient id="technicalGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#2d531a;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#0f1e3f;stop-opacity:1" />
                  </linearGradient>
                </defs>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-3xl font-bold text-[#2d531a]">{{ Math.round(technicalProgress) }}%</span>
              </div>
            </div>
            <h3 class="text-lg font-semibold text-[#1f1d20] mb-1">Técnico</h3>
            <p class="text-sm text-[#1f1d20]/60">Habilidades práticas</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import DotsTimeline from '@/dots/DotsTimeline.vue';
import DotsBadges from '@/dots/DotsBadges.vue';
import DotsAcademicCard from '@/dots/DotsAcademicCard.vue';
import DotsSocialCard from '@/dots/DotsSocialCard.vue';
import DotsTechnicalCard from '@/dots/DotsTechnicalCard.vue';

const userName = ref('João Silva');

const events = ref([
  { date: '2024-01-15', description: 'Concluiu projeto de Ciências com nota máxima' },
  { date: '2024-02-20', description: 'Liderou equipe vencedora do torneio de matemática' },
  { date: '2024-03-10', description: 'Publicou artigo sobre inteligência artificial' },
  { date: '2024-04-05', description: 'Organizou evento de tecnologia na escola' }
]);

const badges = ref([
  'Líder Nato',
  'Mestre em Matemática',
  'Leitor Ávido',
  'Inovador Tecnológico',
  'Colaborador Exemplar',
  'Pensador Crítico'
]);

const academicData = ref({
  grades: 8.5,
  books: 12,
  subjects: [
    { name: 'Matemática', grade: 9.2 },
    { name: 'Português', grade: 8.7 },
    { name: 'Ciências', grade: 9.5 },
    { name: 'História', grade: 8.0 }
  ]
});

const socialData = ref({
  projects: 5,
  games: 8,
  collaborations: 12,
  events: 4
});

const technicalData = ref({
  skills: ['Vue.js', 'Python', 'IA', 'Django', 'Three.js'],
  projects: 7,
  certifications: 3
});

const academicProgress = computed(() => Math.min(academicData.value.grades * 10, 100));
const socialProgress = computed(() => Math.min(socialData.value.projects * 10 + socialData.value.collaborations * 3, 100));
const technicalProgress = computed(() => Math.min(technicalData.value.projects * 10 + technicalData.value.certifications * 15, 100));

const getInitials = (name: string) => {
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

const updateProfile = () => {
  console.log('Updating profile...');
};

const shareProfile = () => {
  console.log('Sharing profile...');
};
</script>