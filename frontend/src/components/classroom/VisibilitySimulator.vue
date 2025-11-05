<template>
  <div class="visibility-simulator bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-600 to-purple-800 px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Simulador de Visão</h3>
          <p class="text-white/70 text-sm">Simule diferentes condições visuais</p>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Controls Panel -->
        <div class="space-y-5">
          <!-- Student Selection -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Perspectiva do Aluno
            </label>
            <select 
              v-model="selectedStudent" 
              class="w-full px-4 py-3 bg-white border border-[#e1d4c2] rounded-xl text-[#1f1d20] focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
            >
              <option value="">Selecione um aluno</option>
              <option 
                v-for="student in students" 
                :key="student.id" 
                :value="student.id"
              >
                {{ student.name }} {{ student.visionIssues ? '⚠️' : '' }}
              </option>
            </select>
          </div>

          <!-- Simulation Type -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Tipo de Deficiência
            </label>
            <div class="space-y-2">
              <button 
                v-for="sim in simulationTypes" 
                :key="sim.value"
                @click="simulationType = sim.value"
                class="w-full py-3 px-4 rounded-lg font-medium text-sm transition-all flex items-center gap-3"
                :class="simulationType === sim.value 
                  ? 'bg-purple-500 text-white shadow-md' 
                  : 'bg-[#e1d4c2]/30 text-[#1f1d20] hover:bg-[#e1d4c2]'"
              >
                <component :is="sim.icon" class="w-5 h-5" />
                <span>{{ sim.label }}</span>
              </button>
            </div>
          </div>

          <!-- Intensity Slider -->
          <div>
            <label class="block text-sm font-semibold text-[#1f1d20] mb-2">
              Intensidade: {{ intensity }}%
            </label>
            <input 
              type="range" 
              min="0" 
              max="100" 
              v-model.number="intensity" 
              class="w-full h-2 bg-[#e1d4c2] rounded-lg appearance-none cursor-pointer accent-purple-500"
            >
            <div class="flex justify-between text-xs text-[#1f1d20]/50 mt-1">
              <span>Leve</span>
              <span>Moderado</span>
              <span>Grave</span>
            </div>
          </div>

          <!-- Options -->
          <div class="space-y-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                v-model="showLabels" 
                class="w-4 h-4 rounded border-[#e1d4c2] text-purple-500 focus:ring-purple-500"
              >
              <span class="text-sm text-[#1f1d20]">Mostrar nomes</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                v-model="showGrid" 
                class="w-4 h-4 rounded border-[#e1d4c2] text-purple-500 focus:ring-purple-500"
              >
              <span class="text-sm text-[#1f1d20]">Mostrar grade</span>
            </label>
          </div>

          <!-- Apply Button -->
          <button 
            @click="applySimulation"
            :disabled="!selectedStudent"
            class="w-full py-3 px-4 rounded-lg bg-gradient-to-r from-purple-600 to-purple-800 text-white font-semibold transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Aplicar Simulação
          </button>
        </div>

        <!-- Visualization Area -->
        <div class="lg:col-span-3">
          <div 
            class="simulation-view relative bg-[#1f1d20]/5 rounded-xl p-8 min-h-[600px] border-2 border-dashed border-[#e1d4c2] overflow-hidden"
            :class="simulationClasses"
          >
            <!-- Simulation Overlay -->
            <div 
              v-if="isSimulating"
              class="simulation-overlay absolute inset-0 pointer-events-none z-10"
              :style="overlayStyle"
            ></div>

            <!-- Classroom View -->
            <div class="classroom-mockup relative h-full">
              <!-- Board -->
              <div class="absolute top-4 left-1/2 -translate-x-1/2 w-3/4 h-16 bg-[#1f1d20] rounded-lg flex items-center justify-center">
                <span class="text-white font-semibold" :style="textStyle">QUADRO</span>
              </div>

              <!-- Sample Content -->
              <div class="absolute top-28 left-1/2 -translate-x-1/2 w-2/3 space-y-4">
                <div class="p-4 bg-white rounded-lg border border-[#e1d4c2]" :style="contentStyle">
                  <h4 class="font-bold text-[#2d531a] mb-2" :style="textStyle">Conteúdo da Aula</h4>
                  <p class="text-sm text-[#1f1d20]/80" :style="textStyle">
                    Este é um exemplo de como o conteúdo aparece para o aluno selecionado.
                  </p>
                </div>

                <div class="grid grid-cols-3 gap-3">
                  <div 
                    v-for="i in 6" 
                    :key="i"
                    class="p-3 bg-[#e1d4c2]/30 rounded-lg text-center"
                    :style="contentStyle"
                  >
                    <div class="w-8 h-8 rounded-full mx-auto mb-2" :class="`bg-${['red', 'blue', 'green', 'yellow', 'purple', 'pink'][i-1]}-500`"></div>
                    <span class="text-xs text-[#1f1d20]" :style="textStyle">Item {{ i }}</span>
                  </div>
                </div>
              </div>

              <!-- Student Position Indicator -->
              <div 
                v-if="selectedStudent"
                class="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-2 bg-white px-4 py-2 rounded-full border border-purple-500 shadow-lg"
              >
                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
                <span class="text-sm font-medium text-[#1f1d20]">Visão do Aluno</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Explanation Panel -->
      <div class="mt-6 p-5 bg-purple-50 border border-purple-200 rounded-xl">
        <div class="flex items-start gap-3">
          <div class="w-10 h-10 rounded-lg bg-purple-500 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h4 class="font-bold text-purple-900 mb-2">{{ currentExplanation.title }}</h4>
            <p class="text-sm text-purple-800 leading-relaxed">{{ currentExplanation.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Student {
  id: string;
  name: string;
  visionIssues?: boolean;
}

const props = defineProps<{
  classroomId: string;
}>();

const selectedStudent = ref('');
const simulationType = ref('myopia');
const intensity = ref(60);
const showLabels = ref(true);
const showGrid = ref(false);
const isSimulating = ref(false);

// Lista de alunos será carregada via props ou API
const students = ref<Student[]>([]);

const simulationTypes = [
  { value: 'myopia', label: 'Miopia', icon: 'svg' },
  { value: 'astigmatism', label: 'Astigmatismo', icon: 'svg' },
  { value: 'glaucoma', label: 'Glaucoma', icon: 'svg' },
  { value: 'colorBlindness', label: 'Daltonismo', icon: 'svg' }
];

const explanations = {
  myopia: {
    title: 'Miopia',
    description: 'Dificuldade em enxergar objetos distantes com clareza. O aluno pode ter problemas para ler o quadro ou ver apresentações do fundo da sala. Recomenda-se sentar nas primeiras fileiras.'
  },
  astigmatism: {
    title: 'Astigmatismo',
    description: 'Visão distorcida ou desfocada em todas as distâncias. O aluno pode ter dificuldade para focar em textos e imagens, causando fadiga visual e dores de cabeça.'
  },
  glaucoma: {
    title: 'Glaucoma',
    description: 'Perda progressiva da visão periférica (visão lateral). O aluno pode ter dificuldade em perceber objetos e pessoas ao seu redor, necessitando de um campo de visão livre.'
  },
  colorBlindness: {
    title: 'Daltonismo',
    description: 'Dificuldade em distinguir certas cores, especialmente vermelho e verde. O aluno pode ter problemas com materiais coloridos, gráficos e sinalizações que dependem de cores.'
  }
};

const currentExplanation = computed(() => {
  return explanations[simulationType.value as keyof typeof explanations] || explanations.myopia;
});

const simulationClasses = computed(() => {
  if (!isSimulating.value) return '';
  
  const classes = [];
  
  switch (simulationType.value) {
    case 'myopia':
      classes.push('blur-effect');
      break;
    case 'astigmatism':
      classes.push('distortion-effect');
      break;
    case 'glaucoma':
      classes.push('vignette-effect');
      break;
    case 'colorBlindness':
      classes.push('color-filter-effect');
      break;
  }
  
  if (intensity.value > 70) {
    classes.push('high-intensity');
  }
  
  return classes.join(' ');
});

const overlayStyle = computed(() => {
  const styles: any = {};
  
  if (simulationType.value === 'myopia') {
    styles.backdropFilter = `blur(${intensity.value / 10}px)`;
  } else if (simulationType.value === 'glaucoma') {
    styles.background = `radial-gradient(circle, transparent ${100 - intensity.value}%, rgba(0,0,0,0.8) 100%)`;
  } else if (simulationType.value === 'colorBlindness') {
    styles.filter = `grayscale(${intensity.value}%) hue-rotate(${intensity.value}deg)`;
  }
  
  return styles;
});

const contentStyle = computed(() => {
  if (!isSimulating.value) return {};
  
  const styles: any = {};
  
  if (simulationType.value === 'astigmatism') {
    styles.filter = `blur(${intensity.value / 30}px)`;
    styles.transform = `skew(${intensity.value / 50}deg)`;
  }
  
  return styles;
});

const textStyle = computed(() => {
  if (!isSimulating.value || !showLabels.value) return {};
  
  const styles: any = {};
  
  if (simulationType.value === 'myopia') {
    styles.filter = `blur(${intensity.value / 15}px)`;
  }
  
  return styles;
});

const applySimulation = () => {
  isSimulating.value = true;
  console.log('Applying simulation:', {
    student: selectedStudent.value,
    type: simulationType.value,
    intensity: intensity.value
  });
};
</script>

<style scoped>
.simulation-view {
  transition: all 0.3s ease;
}

.blur-effect {
  filter: blur(2px);
}

.vignette-effect::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, transparent 50%, rgba(0,0,0,0.8) 100%);
  pointer-events: none;
}

.color-filter-effect {
  filter: saturate(0.3) hue-rotate(30deg);
}

.distortion-effect {
  animation: distort 3s ease-in-out infinite;
}

@keyframes distort {
  0%, 100% { transform: skew(0deg); }
  50% { transform: skew(1deg); }
}

.high-intensity {
  opacity: 0.7;
}
</style>