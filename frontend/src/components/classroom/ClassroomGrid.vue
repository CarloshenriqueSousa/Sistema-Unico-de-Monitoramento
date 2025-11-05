<template>
  <div class="grid-editor">
    <div class="editor-background"></div>
    
    <div class="editor-header">
      <div class="header-content">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M3 6a3 3 0 013-3h2.25a3 3 0 013 3v2.25a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm9.75 0a3 3 0 013-3H18a3 3 0 013 3v2.25a3 3 0 01-3 3h-2.25a3 3 0 01-3-3V6zM3 15.75a3 3 0 013-3h2.25a3 3 0 013 3V18a3 3 0 01-3 3H6a3 3 0 01-3-3v-2.25zm9.75 0a3 3 0 013-3H18a3 3 0 013 3V18a3 3 0 01-3 3h-2.25a3 3 0 01-3-3v-2.25z" clip-rule="evenodd" />
          </svg>
        </div>
        <div>
          <h3 class="editor-title">Editor de Grade da Sala</h3>
          <p class="editor-subtitle">Configure o layout e organização</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button @click="resetGrid" class="action-btn secondary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 01-9.201 2.466l-.312-.311h2.433a.75.75 0 000-1.5H3.989a.75.75 0 00-.75.75v4.242a.75.75 0 001.5 0v-2.43l.31.31a7 7 0 0011.712-3.138.75.75 0 00-1.449-.39zm1.23-3.723a.75.75 0 00.219-.53V2.929a.75.75 0 00-1.5 0V5.36l-.31-.31A7 7 0 003.239 8.188a.75.75 0 101.448.389A5.5 5.5 0 0113.89 6.11l.311.31h-2.432a.75.75 0 000 1.5h4.243a.75.75 0 00.53-.219z" clip-rule="evenodd" />
          </svg>
          Resetar
        </button>
        
        <button @click="saveGrid" class="action-btn primary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
            <path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
          </svg>
          Salvar Grade
        </button>
      </div>
    </div>
    
    <div class="editor-content">
      <div class="controls-panel">
        <div class="control-section">
          <h4 class="section-title">Dimensões</h4>
          
          <div class="control-group">
            <label class="control-label">
              <span>Linhas</span>
              <input 
                v-model.number="gridRows" 
                type="number" 
                min="3" 
                max="10"
                class="control-input"
              />
            </label>
            
            <label class="control-label">
              <span>Colunas</span>
              <input 
                v-model.number="gridCols" 
                type="number" 
                min="3" 
                max="10"
                class="control-input"
              />
            </label>
          </div>
        </div>
        
        <div class="control-section">
          <h4 class="section-title">Espaçamento</h4>
          
          <label class="control-label">
            <span>{{ spacing }}px</span>
            <input 
              v-model.number="spacing" 
              type="range" 
              min="80" 
              max="200"
              class="control-range"
            />
          </label>
        </div>
        
        <div class="control-section">
          <h4 class="section-title">Layouts Predefinidos</h4>
          
          <div class="preset-buttons">
            <button 
              v-for="preset in presets" 
              :key="preset.name"
              @click="applyPreset(preset)"
              class="preset-btn"
            >
              <div class="preset-icon" v-html="preset.icon"></div>
              <span>{{ preset.name }}</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="grid-preview">
        <div class="preview-canvas">
          <div 
            class="grid-container"
            :style="{
              gridTemplateColumns: `repeat(${gridCols}, 1fr)`,
              gap: `${spacing / 2}px`
            }"
          >
            <div 
              v-for="(cell, index) in totalCells" 
              :key="index"
              class="grid-cell"
              :class="{ 'cell-occupied': cell.occupied }"
              @click="toggleCell(index)"
            >
              <div class="cell-number">{{ index + 1 }}</div>
              <div v-if="cell.occupied" class="cell-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 00-13.074.003z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <div class="preview-info">
          <div class="info-item">
            <span class="info-label">Total de assentos:</span>
            <span class="info-value">{{ totalCells.length }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Ocupados:</span>
            <span class="info-value">{{ occupiedCount }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Disponíveis:</span>
            <span class="info-value">{{ totalCells.length - occupiedCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const gridRows = ref(5)
const gridCols = ref(6)
const spacing = ref(120)

const cells = ref({})

const presets = [
  {
    name: 'Tradicional',
    rows: 5,
    cols: 6,
    spacing: 120,
    icon: '<div style="display:grid;grid-template-columns:repeat(3,4px);gap:2px;"><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div><div style="width:4px;height:4px;background:#2d531a;border-radius:1px"></div></div>'
  },
  {
    name: 'Grupos',
    rows: 4,
    cols: 4,
    spacing: 150,
    icon: '<div style="display:grid;grid-template-columns:repeat(2,8px);gap:4px;"><div style="width:8px;height:8px;background:#2d531a;border-radius:2px"></div><div style="width:8px;height:8px;background:#2d531a;border-radius:2px"></div><div style="width:8px;height:8px;background:#2d531a;border-radius:2px"></div><div style="width:8px;height:8px;background:#2d531a;border-radius:2px"></div></div>'
  },
  {
    name: 'Circular',
    rows: 1,
    cols: 12,
    spacing: 100,
    icon: '<div style="width:20px;height:20px;border:3px solid #2d531a;border-radius:50%"></div>'
  }
]

const totalCells = computed(() => {
  const total = gridRows.value * gridCols.value
  return Array.from({ length: total }, (_, i) => ({
    occupied: cells.value[i] || false
  }))
})

const occupiedCount = computed(() => {
  return Object.values(cells.value).filter(Boolean).length
})

const toggleCell = (index) => {
  cells.value[index] = !cells.value[index]
}

const applyPreset = (preset) => {
  gridRows.value = preset.rows
  gridCols.value = preset.cols
  spacing.value = preset.spacing
  cells.value = {}
}

const resetGrid = () => {
  cells.value = {}
  gridRows.value = 5
  gridCols.value = 6
  spacing.value = 120
}

const saveGrid = () => {
  console.log('Salvando configuração da grade...')
  // Lógica de salvamento
}
</script>

<style scoped>
.grid-editor {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  overflow: hidden;
}

.editor-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(225, 212, 194, 0.3), transparent 60%);
  pointer-events: none;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 2px solid rgba(45, 83, 26, 0.1);
  position: relative;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 8px 16px rgba(45, 83, 26, 0.3);
}

.header-icon svg {
  width: 2rem;
  height: 2rem;
  color: #e1d4c2;
}

.editor-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
  line-height: 1.2;
}

.editor-subtitle {
  font-size: 0.875rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0.25rem 0 0 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

.action-btn.secondary {
  background: #e1d4c2;
  color: #1f1d20;
}

.action-btn.secondary:hover {
  background: #d4c7b5;
}

.btn-icon {
  width: 1.125rem;
  height: 1.125rem;
}

.editor-content {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  padding: 2rem;
  position: relative;
}

.controls-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.control-section {
  background: rgba(225, 212, 194, 0.3);
  border-radius: 1rem;
  padding: 1.25rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #1f1d20;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.control-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.control-label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f1d20;
}

.control-input {
  padding: 0.625rem;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  color: #1f1d20;
  font-weight: 600;
  transition: border-color 0.2s ease;
}

.control-input:focus {
  outline: none;
  border-color: #2d531a;
}

.control-range {
  width: 100%;
  accent-color: #2d531a;
}

.preset-buttons {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.preset-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  border-color: #2d531a;
  transform: translateX(4px);
}

.preset-icon {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grid-preview {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.preview-canvas {
  background: rgba(225, 212, 194, 0.2);
  border-radius: 1rem;
  padding: 2rem;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.grid-container {
  display: grid;
  width: 100%;
  max-width: 800px;
}

.grid-cell {
  aspect-ratio: 1;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.grid-cell:hover {
  border-color: #2d531a;
  transform: scale(1.05);
}

.grid-cell.cell-occupied {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-color: #2d531a;
}

.cell-number {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.5;
}

.cell-occupied .cell-number {
  opacity: 0;
}

.cell-icon {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cell-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  color: #e1d4c2;
}

.preview-info {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #2d531a;
}

@media (max-width: 1024px) {
  .editor-content {
    grid-template-columns: 1fr;
  }
  
  .controls-panel {
    order: 2;
  }
  
  .grid-preview {
    order: 1;
  }
}

@media (max-width: 640px) {
  .editor-header {
    padding: 1.5rem;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .action-btn {
    flex: 1;
  }
  
  .editor-content {
    padding: 1.5rem;
  }
}
</style>