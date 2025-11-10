<template>
  <div class="demo-classroom">
    <!-- Hero Section -->
    <section class="hero-demo">
      <div class="hero-bg">
        <div class="gradient-sphere sphere-1"></div>
        <div class="gradient-sphere sphere-2"></div>
      </div>
      
      <div class="hero-content-demo">
        <div class="hero-badge-demo">
          <span class="badge-dot"></span>
          <span>Mapeamento Interativo de Salas</span>
        </div>
        
        <h1 class="hero-title-demo">
          Organize sua <span class="gradient-txt">Sala de Aula</span>
        </h1>
        
        <p class="hero-desc-demo">
          Crie layouts personalizados com drag-and-drop, distribua alunos 
          inteligentemente e visualize sua sala em tempo real
        </p>
        
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-num">100%</div>
            <div class="stat-txt">Personalizável</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">3+</div>
            <div class="stat-txt">Métodos</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">∞</div>
            <div class="stat-txt">Layouts</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Demo Area -->
    <section class="main-demo">
      <div class="demo-container">
        <!-- Control Panel -->
        <div class="control-panel">
          <div class="panel-header">
            <h2 class="panel-title">Configuração do Mapa</h2>
            <p class="panel-subtitle">Personalize o layout da sua sala</p>
          </div>

          <!-- Layout Config -->
          <div class="config-section">
            <div class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              </svg>
              <span>Layout da Sala</span>
            </div>
            
            <div class="config-grid">
              <div class="config-item">
                <label class="config-label">Fileiras</label>
                <div class="number-input">
                  <button @click="adjustRows(-1)" class="num-btn">-</button>
                  <input v-model.number="rows" type="number" min="1" max="10" class="num-field"/>
                  <button @click="adjustRows(1)" class="num-btn">+</button>
                </div>
              </div>

              <div class="config-item">
                <label class="config-label">Colunas</label>
                <div class="number-input">
                  <button @click="adjustCols(-1)" class="num-btn">-</button>
                  <input v-model.number="cols" type="number" min="1" max="12" class="num-field"/>
                  <button @click="adjustCols(1)" class="num-btn">+</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Teacher Position -->
          <div class="config-section">
            <div class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span>Professor</span>
            </div>
            
            <div class="teacher-positions">
              <button 
                v-for="pos in teacherPositions" 
                :key="pos.value"
                @click="teacherPos = pos.value"
                :class="['pos-btn', { active: teacherPos === pos.value }]"
              >
                {{ pos.label }}
              </button>
            </div>
          </div>

          <!-- Students List -->
          <div class="config-section">
            <div class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              <span>Lista de Alunos</span>
            </div>
            
            <textarea 
              v-model="studentsList"
              class="students-input"
              placeholder="Digite um aluno por linha...&#10;Ex:&#10;João Silva&#10;Maria Santos&#10;Pedro Costa"
            ></textarea>
            
            <div class="student-count">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <polyline points="17 11 19 13 23 9"/>
              </svg>
              <span>{{ parsedStudents.length }} alunos</span>
            </div>
          </div>

          <!-- Distribution Methods -->
          <div class="config-section">
            <div class="section-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              <span>Distribuição</span>
            </div>
            
            <div class="distribution-btns">
              <button 
                v-for="method in distributionMethods" 
                :key="method.value"
                @click="distributeStudents(method.value)"
                :class="['dist-btn', method.color]"
              >
                <span class="dist-icon">{{ method.icon }}</span>
                <span class="dist-label">{{ method.label }}</span>
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="config-section">
            <div class="action-buttons-demo">
              <button @click="clearMap" class="action-btn-demo secondary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
                <span>Limpar</span>
              </button>
              <button @click="exportMap" class="action-btn-demo primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                <span>Exportar</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Classroom Canvas -->
        <div class="classroom-canvas">
          <div class="canvas-header">
            <div class="canvas-info">
              <h3 class="canvas-title">Mapa da Sala</h3>
              <p class="canvas-subtitle">Arraste os alunos para reposicionar</p>
            </div>
            <div class="canvas-actions">
              <button @click="zoomOut" class="canvas-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
              </button>
              <button @click="zoomIn" class="canvas-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="11" y1="8" x2="11" y2="14"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
              </button>
              <button @click="resetZoom" class="canvas-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="1 4 1 10 7 10"/>
                  <polyline points="23 20 23 14 17 14"/>
                  <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="canvas-body" ref="canvasRef">
            <div class="classroom-grid" :style="gridStyle">
              <!-- Teacher Area -->
              <div v-if="teacherPos !== 'hidden'" :class="['teacher-area', `teacher-${teacherPos}`]">
                <div class="teacher-desk">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <span>Professor</span>
                </div>
              </div>

              <!-- Student Seats -->
              <div 
                v-for="(seat, index) in seats" 
                :key="index"
                @dragover.prevent
                @drop="handleDrop($event, index)"
                :class="['seat', { 
                  'occupied': seat.student, 
                  'dragging': draggedIndex === index 
                }]"
              >
                <div 
                  v-if="seat.student"
                  draggable="true"
                  @dragstart="handleDragStart($event, index)"
                  @dragend="handleDragEnd"
                  class="student-card"
                >
                  <div class="student-avatar">
                    {{ getInitials(seat.student) }}
                  </div>
                  <div class="student-info">
                    <div class="student-name">{{ seat.student }}</div>
                    <div class="student-position">Fileira {{ Math.floor(index / cols) + 1 }}, Assento {{ (index % cols) + 1 }}</div>
                  </div>
                </div>
                <div v-else class="empty-seat">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="seats.length === 0" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="9" y1="9" x2="15" y2="15"/>
                  <line x1="15" y1="9" x2="9" y2="15"/>
                </svg>
              </div>
              <h3 class="empty-title">Nenhum assento configurado</h3>
              <p class="empty-desc">Configure o número de fileiras e colunas para começar</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-demo">
      <div class="features-content">
        <div class="features-header">
          <h2 class="features-title">Como Funciona</h2>
          <p class="features-subtitle">Três passos simples para criar seu mapa perfeito</p>
        </div>

        <div class="features-cards">
          <div class="feature-card-demo">
            <div class="feature-num">01</div>
            <div class="feature-icon-demo">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <line x1="3" y1="9" x2="21" y2="9"/>
                <line x1="9" y1="21" x2="9" y2="9"/>
              </svg>
            </div>
            <h3 class="feature-title-demo">Configure o Layout</h3>
            <p class="feature-desc-demo">Defina o número de fileiras e colunas que melhor se adequa à sua sala</p>
          </div>

          <div class="feature-card-demo">
            <div class="feature-num">02</div>
            <div class="feature-icon-demo">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <h3 class="feature-title-demo">Adicione Alunos</h3>
            <p class="feature-desc-demo">Insira a lista de alunos e escolha o método de distribuição ideal</p>
          </div>

          <div class="feature-card-demo">
            <div class="feature-num">03</div>
            <div class="feature-icon-demo">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                <path d="M2 2l7.586 7.586"/>
                <circle cx="11" cy="11" r="2"/>
              </svg>
            </div>
            <h3 class="feature-title-demo">Personalize</h3>
            <p class="feature-desc-demo">Arraste e solte para ajustar posições e exporte o resultado final</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// State
const rows = ref(5)
const cols = ref(6)
const teacherPos = ref<'left' | 'center' | 'right' | 'hidden'>('center')
const studentsList = ref('')
const draggedIndex = ref<number | null>(null)
const zoom = ref(1)
const canvasRef = ref<HTMLElement>()

// Data
const teacherPositions: Array<{ value: 'left'|'center'|'right'|'hidden'; label: string }> = [
  { value: 'left', label: 'Esquerda' },
  { value: 'center', label: 'Centro' },
  { value: 'right', label: 'Direita' },
  { value: 'hidden', label: 'Ocultar' }
]

const distributionMethods = [
  { value: 'random', label: 'Aleatória', icon: '🎲', color: 'blue' },
  { value: 'alphabetical', label: 'Alfabética', icon: '🔤', color: 'green' },
  { value: 'sequential', label: 'Sequencial', icon: '📋', color: 'purple' }
]

// Computed
const parsedStudents = computed(() => {
  return studentsList.value
    .split('\n')
    .map(s => s.trim())
    .filter(s => s.length > 0)
})

const seats = ref<Array<{ student: string | null }>>([])

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${cols.value}, 1fr)`,
  transform: `scale(${zoom.value})`,
  transformOrigin: 'center center'
}))

// Methods
const adjustRows = (delta: number) => {
  const newRows = rows.value + delta
  if (newRows >= 1 && newRows <= 10) {
    rows.value = newRows
    initializeSeats()
  }
}

const adjustCols = (delta: number) => {
  const newCols = cols.value + delta
  if (newCols >= 1 && newCols <= 12) {
    cols.value = newCols
    initializeSeats()
  }
}

const initializeSeats = () => {
  const totalSeats = rows.value * cols.value
  const currentSeats = seats.value.length
  
  if (totalSeats > currentSeats) {
    // Add empty seats
    for (let i = currentSeats; i < totalSeats; i++) {
      seats.value.push({ student: null })
    }
  } else if (totalSeats < currentSeats) {
    // Remove excess seats
    seats.value = seats.value.slice(0, totalSeats)
  }
}

const distributeStudents = (method: string) => {
  initializeSeats()
  
  let students = [...parsedStudents.value]
  
  // Apply distribution method
  switch (method) {
    case 'alphabetical':
      students.sort((a, b) => a.localeCompare(b))
      break
    case 'random':
      students = students.sort(() => Math.random() - 0.5)
      break
    // sequential: keep as is
  }
  
  // Assign students to seats
  seats.value.forEach((seat, index) => {
    seat.student = students[index] || null
  })
}

const handleDragStart = (event: DragEvent, index: number) => {
  draggedIndex.value = index
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
  }
}

const handleDragEnd = () => {
  draggedIndex.value = null
}

const handleDrop = (event: DragEvent, targetIndex: number) => {
  event.preventDefault()
  
  if (draggedIndex.value === null || draggedIndex.value === targetIndex) return
  
  // Swap students
  const temp = seats.value[targetIndex].student
  seats.value[targetIndex].student = seats.value[draggedIndex.value].student
  seats.value[draggedIndex.value].student = temp
  
  draggedIndex.value = null
}

const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const clearMap = () => {
  seats.value.forEach(seat => {
    seat.student = null
  })
}

const exportMap = () => {
  const mapData = {
    rows: rows.value,
    cols: cols.value,
    teacherPos: teacherPos.value,
    students: seats.value.map((seat, index) => ({
      position: index,
      row: Math.floor(index / cols.value) + 1,
      col: (index % cols.value) + 1,
      student: seat.student
    })).filter(s => s.student)
  }
  
  const dataStr = JSON.stringify(mapData, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `mapa-sala-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const zoomIn = () => {
  if (zoom.value < 1.5) zoom.value += 0.1
}

const zoomOut = () => {
  if (zoom.value > 0.5) zoom.value -= 0.1
}

const resetZoom = () => {
  zoom.value = 1
}

// Initialize
initializeSeats()
</script>

<style scoped>
.demo-classroom {
  min-height: 100vh;
  background: linear-gradient(180deg, #fcfcfc 0%, #f5f5f5 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
}

/* Hero Section */
.hero-demo {
  position: relative;
  padding: 8rem 2rem 4rem;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.gradient-sphere {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.2;
}

.sphere-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #10b981);
  top: -200px;
  right: -100px;
}

.sphere-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  bottom: -150px;
  left: -100px;
}

.hero-content-demo {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.hero-badge-demo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  padding: 0.75rem 1.5rem;
  border-radius: 100px;
  border: 1px solid rgba(23, 24, 28, 0.1);
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.06);
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.hero-title-demo {
  font-size: 4.5rem;
  font-weight: 900;
  color: #17181c;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
}

.gradient-txt {
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc-demo {
  font-size: 1.3rem;
  color: #6b7280;
  line-height: 1.7;
  margin-bottom: 3rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-num {
  font-size: 2.5rem;
  font-weight: 900;
  color: #17181c;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-txt {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 600;
}

/* Main Demo */
.main-demo {
  padding: 4rem 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.demo-container {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 2rem;
  align-items: start;
}

/* Control Panel */
.control-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  padding: 2rem;
  position: sticky;
  top: 2rem;
  box-shadow: 0 8px 32px rgba(23, 24, 28, 0.08);
}

.panel-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(23, 24, 28, 0.08);
}

.panel-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #17181c;
  margin-bottom: 0.5rem;
}

.panel-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
}

.config-section {
  margin-bottom: 2rem;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #17181c;
  margin-bottom: 1rem;
}

.section-label svg {
  color: #3b82f6;
}

.config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b7280;
}

.number-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 10px;
  padding: 0.25rem;
}

.num-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #17181c;
  color: #fcfcfc;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.num-btn:hover {
  background: #2d2f36;
  transform: scale(1.05);
}

.num-field {
  flex: 1;
  text-align: center;
  border: none;
  background: none;
  font-size: 1rem;
  font-weight: 700;
  color: #17181c;
  outline: none;
}

.teacher-positions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.pos-btn {
  padding: 0.75rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.pos-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.pos-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  border-color: transparent;
  color: #fcfcfc;
  transform: scale(1.02);
}

.students-input {
  width: 100%;
  min-height: 200px;
  padding: 1rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 12px;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 0.9rem;
  color: #17181c;
  resize: vertical;
  transition: all 0.2s;
}

.students-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.student-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #17181c;
  margin-top: 0.75rem;
}

.student-count svg {
  color: #10b981;
}

.distribution-btns {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.dist-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  text-align: left;
}

.dist-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(23, 24, 28, 0.1);
}

.dist-btn.blue:hover {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.dist-btn.green:hover {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.dist-btn.purple:hover {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}

.dist-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(23, 24, 28, 0.05);
  border-radius: 10px;
}

.dist-label {
  font-weight: 700;
  font-size: 0.95rem;
  color: #17181c;
}

.action-buttons-demo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.action-btn-demo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.action-btn-demo.secondary {
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  color: #6b7280;
}

.action-btn-demo.secondary:hover {
  background: #ef4444;
  border-color: #ef4444;
  color: #fcfcfc;
  transform: translateY(-2px);
}

.action-btn-demo.primary {
  background: linear-gradient(135deg, #17181c 0%, #2d2f36 100%);
  color: #fcfcfc;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.2);
}

.action-btn-demo.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(23, 24, 28, 0.3);
}

/* Classroom Canvas */
.classroom-canvas {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(23, 24, 28, 0.08);
}

.canvas-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(23, 24, 28, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, rgba(59, 130, 246, 0.02) 0%, transparent 100%);
}

.canvas-info {
  flex: 1;
}

.canvas-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #17181c;
  margin-bottom: 0.25rem;
}

.canvas-subtitle {
  font-size: 0.85rem;
  color: #6b7280;
}

.canvas-actions {
  display: flex;
  gap: 0.5rem;
}

.canvas-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 10px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.canvas-btn:hover {
  background: #17181c;
  border-color: #17181c;
  color: #fcfcfc;
  transform: scale(1.05);
}

.canvas-body {
  padding: 3rem;
  min-height: 600px;
  background: linear-gradient(180deg, #fcfcfc 0%, #f8f9fa 100%);
  position: relative;
  overflow: auto;
}

.classroom-grid {
  display: grid;
  gap: 1.5rem;
  transition: transform 0.3s;
  max-width: 100%;
  margin: 0 auto;
}

/* Teacher Area */
.teacher-area {
  grid-column: 1 / -1;
  display: flex;
  margin-bottom: 2rem;
}

.teacher-area.teacher-left {
  justify-content: flex-start;
}

.teacher-area.teacher-center {
  justify-content: center;
}

.teacher-area.teacher-right {
  justify-content: flex-end;
}

.teacher-desk {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 2.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  border-radius: 16px;
  color: #fcfcfc;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

/* Seats */
.seat {
  aspect-ratio: 1;
  background: rgba(255, 255, 255, 0.8);
  border: 2px dashed rgba(23, 24, 28, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  position: relative;
}

.seat:hover {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
  transform: scale(1.02);
}

.seat.occupied {
  background: rgba(255, 255, 255, 1);
  border: 2px solid rgba(23, 24, 28, 0.1);
}

.seat.dragging {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
  border-style: solid;
}

.empty-seat {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(23, 24, 28, 0.2);
}

.student-card {
  width: 100%;
  height: 100%;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  cursor: move;
  transition: all 0.2s;
}

.student-card:hover {
  transform: scale(1.05);
}

.student-avatar {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  font-weight: 800;
  font-size: 1.25rem;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.student-info {
  text-align: center;
  width: 100%;
}

.student-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #17181c;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.student-position {
  font-size: 0.7rem;
  color: #6b7280;
  font-weight: 600;
}

/* Empty State */
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: rgba(23, 24, 28, 0.05);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(23, 24, 28, 0.3);
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #17181c;
}

.empty-desc {
  font-size: 1rem;
  color: #6b7280;
  max-width: 400px;
  text-align: center;
}

/* Features Demo Section */
.features-demo {
  padding: 6rem 2rem;
  background: linear-gradient(180deg, #f8f9fa 0%, #fcfcfc 100%);
}

.features-content {
  max-width: 1200px;
  margin: 0 auto;
}

.features-header {
  text-align: center;
  margin-bottom: 4rem;
}

.features-title {
  font-size: 3rem;
  font-weight: 900;
  color: #17181c;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.features-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
}

.features-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.feature-card-demo {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  padding: 3rem;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card-demo:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 64px rgba(23, 24, 28, 0.15);
  border-color: rgba(23, 24, 28, 0.2);
}

.feature-num {
  position: absolute;
  top: 2rem;
  right: 2rem;
  font-size: 4rem;
  font-weight: 900;
  color: rgba(23, 24, 28, 0.04);
  line-height: 1;
}

.feature-icon-demo {
  width: 68px;
  height: 68px;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  margin-bottom: 2rem;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card-demo:hover .feature-icon-demo {
  transform: scale(1.1) rotate(5deg);
}

.feature-title-demo {
  font-size: 1.75rem;
  font-weight: 800;
  color: #17181c;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.feature-desc-demo {
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.7;
}

/* Responsive */
@media (max-width: 1200px) {
  .demo-container {
    grid-template-columns: 1fr;
  }
  
  .control-panel {
    position: static;
  }
}

@media (max-width: 768px) {
  .hero-title-demo {
    font-size: 3rem;
  }
  
  .hero-desc-demo {
    font-size: 1.1rem;
  }
  
  .features-title {
    font-size: 2rem;
  }
  
  .canvas-body {
    padding: 1.5rem;
  }
  
  .classroom-grid {
    gap: 1rem;
  }
  
  .student-avatar {
    width: 50px;
    height: 50px;
    font-size: 1rem;
  }
  
  .student-name {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .hero-title-demo {
    font-size: 2.5rem;
  }
  
  .hero-stats {
    gap: 2rem;
  }
  
  .stat-num {
    font-size: 2rem;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
  }
  
  .teacher-positions {
    grid-template-columns: 1fr;
  }
  
  .action-buttons-demo {
    grid-template-columns: 1fr;
  }
}
</style>