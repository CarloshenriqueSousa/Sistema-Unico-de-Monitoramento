<template>
  <div class="classroom-grid-editor bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-bold text-white">Editor de Grade da Sala</h3>
            <p class="text-white/70 text-sm">Configure o layout e organização</p>
          </div>
        </div>

        <button 
          @click="$emit('close')"
          class="p-2 rounded-lg hover:bg-white/10 transition-colors"
        >
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Configuration Panel -->
        <div class="space-y-5">
          <!-- Grid Dimensions -->
          <div>
            <h4 class="font-semibold text-[#1f1d20] mb-3">Dimensões da Grade</h4>
            <div class="space-y-3">
              <div>
                <label class="block text-sm text-[#1f1d20]/60 mb-2">
                  Linhas: {{ gridRows }}
                </label>
                <input 
                  type="range" 
                  v-model.number="gridRows" 
                  min="3" 
                  max="10" 
                  class="w-full h-2 bg-[#e1d4c2] rounded-lg appearance-none cursor-pointer accent-[#2d531a]"
                >
              </div>
              <div>
                <label class="block text-sm text-[#1f1d20]/60 mb-2">
                  Colunas: {{ gridCols }}
                </label>
                <input 
                  type="range" 
                  v-model.number="gridCols" 
                  min="3" 
                  max="10" 
                  class="w-full h-2 bg-[#e1d4c2] rounded-lg appearance-none cursor-pointer accent-[#2d531a]"
                >
              </div>
            </div>
          </div>

          <!-- Spacing -->
          <div>
            <h4 class="font-semibold text-[#1f1d20] mb-3">Espaçamento</h4>
            <div>
              <label class="block text-sm text-[#1f1d20]/60 mb-2">
                Entre carteiras: {{ spacing }}px
              </label>
              <input 
                type="range" 
                v-model.number="spacing" 
                min="50" 
                max="150" 
                step="10"
                class="w-full h-2 bg-[#e1d4c2] rounded-lg appearance-none cursor-pointer accent-[#0f1e3f]"
              >
            </div>
          </div>

          <!-- Layout Presets -->
          <div>
            <h4 class="font-semibold text-[#1f1d20] mb-3">Layouts Pré-definidos</h4>
            <div class="space-y-2">
              <button 
                v-for="preset in layoutPresets" 
                :key="preset.value"
                @click="applyPreset(preset.value)"
                class="w-full py-2.5 px-4 rounded-lg font-medium text-sm transition-all flex items-center gap-2 bg-[#e1d4c2]/30 hover:bg-[#e1d4c2] text-[#1f1d20]"
              >
                <component :is="preset.icon" class="w-5 h-5" />
                {{ preset.label }}
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="space-y-2 pt-4 border-t border-[#e1d4c2]">
            <button 
              @click="resetGrid"
              class="w-full py-2.5 px-4 rounded-lg bg-[#e1d4c2] hover:bg-[#e1d4c2]/70 text-[#1f1d20] font-medium transition-all"
            >
              Resetar
            </button>
            <button 
              @click="saveGrid"
              class="w-full py-2.5 px-4 rounded-lg bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-semibold transition-all hover:shadow-lg"
            >
              Salvar Grade
            </button>
          </div>
        </div>

        <!-- Grid Preview -->
        <div class="lg:col-span-3">
          <div class="grid-preview bg-[#e1d4c2]/10 rounded-xl p-8 min-h-[600px] border-2 border-dashed border-[#e1d4c2] relative overflow-auto">
            <!-- Board Indicator -->
            <div class="absolute top-4 left-1/2 -translate-x-1/2 px-4 py-2 bg-[#1f1d20] text-white text-sm rounded-lg">
              Quadro
            </div>

            <!-- Grid -->
            <div 
              class="grid-container relative mx-auto"
              :style="{
                marginTop: '80px',
                display: 'grid',
                gridTemplateColumns: `repeat(${gridCols}, ${cellSize}px)`,
                gridTemplateRows: `repeat(${gridRows}, ${cellSize}px)`,
                gap: `${spacing}px`
              }"
            >
              <div 
                v-for="(cell, index) in totalCells" 
                :key="index"
                class="grid-cell bg-white border-2 rounded-lg transition-all cursor-pointer hover:shadow-md"
                :class="{
                  'border-[#2d531a] bg-[#2d531a]/5': cell.occupied,
                  'border-[#e1d4c2]': !cell.occupied
                }"
                @click="toggleCell(index)"
              >
                <div class="w-full h-full flex items-center justify-center">
                  <div v-if="cell.occupied" class="text-center">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#2d531a] to-[#0f1e3f] mx-auto mb-1"></div>
                    <span class="text-xs text-[#1f1d20]/60">{{ index + 1 }}</span>
                  </div>
                  <div v-else class="text-xs text-[#1f1d20]/30">
                    {{ index + 1 }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Stats -->
            <div class="absolute bottom-4 left-4 bg-white border border-[#e1d4c2] rounded-lg p-3 shadow-md">
              <div class="space-y-1 text-sm">
                <div class="flex items-center justify-between gap-4">
                  <span class="text-[#1f1d20]/60">Total de posições:</span>
                  <span class="font-bold text-[#2d531a]">{{ gridRows * gridCols }}</span>
                </div>
                <div class="flex items-center justify-between gap-4">
                  <span class="text-[#1f1d20]/60">Ocupadas:</span>
                  <span class="font-bold text-[#0f1e3f]">{{ occupiedCount }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface GridCell {
  occupied: boolean;
}

defineEmits<{
  close: [];
}>();

const gridRows = ref(5);
const gridCols = ref(6);
const spacing = ref(80);
const cellSize = 80;

const layoutPresets = [
  { value: 'traditional', label: 'Tradicional (Fileiras)', icon: 'svg' },
  { value: 'groups', label: 'Grupos', icon: 'svg' },
  { value: 'ushaped', label: 'Formato U', icon: 'svg' },
  { value: 'circle', label: 'Círculo', icon: 'svg' }
];

// Initialize grid cells
const cells = ref<GridCell[]>([]);
const initializeCells = () => {
  const total = gridRows.value * gridCols.value;
  cells.value = Array.from({ length: total }, () => ({ occupied: false }));
};
initializeCells();

const totalCells = computed(() => {
  const total = gridRows.value * gridCols.value;
  if (cells.value.length !== total) {
    initializeCells();
  }
  return cells.value;
});

const occupiedCount = computed(() => {
  return cells.value.filter(c => c.occupied).length;
});

const toggleCell = (index: number) => {
  cells.value[index].occupied = !cells.value[index].occupied;
};

const applyPreset = (preset: string) => {
  cells.value.forEach(c => c.occupied = false);
  
  switch (preset) {
    case 'traditional':
      // Fill all cells
      cells.value.forEach(c => c.occupied = true);
      break;
      
    case 'groups':
      // Groups of 4-6
      gridRows.value = 4;
      gridCols.value = 6;
      spacing.value = 100;
      break;
      
    case 'ushaped':
      // U-shaped arrangement
      const total = gridRows.value * gridCols.value;
      cells.value.forEach((c, i) => {
        const row = Math.floor(i / gridCols.value);
        const col = i % gridCols.value;
        // Outer rows and columns
        c.occupied = row === 0 || row === gridRows.value - 1 || col === 0 || col === gridCols.value - 1;
      });
      break;
      
    case 'circle':
      spacing.value = 120;
      break;
  }
};

const resetGrid = () => {
  gridRows.value = 5;
  gridCols.value = 6;
  spacing.value = 80;
  initializeCells();
};

const saveGrid = () => {
  const config = {
    rows: gridRows.value,
    cols: gridCols.value,
    spacing: spacing.value,
    cells: cells.value.map((c, i) => ({
      index: i,
      occupied: c.occupied
    }))
  };
  console.log('Saving grid configuration:', config);
  // API call here
};
</script>

<style scoped>
.grid-cell {
  transition: all 0.2s ease;
  aspect-ratio: 1;
}

.grid-cell:hover {
  transform: scale(1.05);
  z-index: 10;
}

.grid-preview {
  background-image: 
    linear-gradient(rgba(225, 212, 194, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(225, 212, 194, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}
</style>