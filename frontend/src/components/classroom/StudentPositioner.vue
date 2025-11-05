<template>
  <div class="student-positioner">
    <div class="positioner-background"></div>
    
    <div class="positioner-header">
      <div class="header-content">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M8.161 2.58a1.875 1.875 0 011.678 0l4.993 2.498c.106.052.23.052.336 0l3.869-1.935A1.875 1.875 0 0121.75 4.82v12.485c0 .71-.401 1.36-1.037 1.677l-4.875 2.437a1.875 1.875 0 01-1.676 0l-4.994-2.497a.375.375 0 00-.336 0l-3.868 1.935A1.875 1.875 0 012.25 19.18V6.695c0-.71.401-1.36 1.036-1.677l4.875-2.437zM9 6a.75.75 0 01.75.75V15a.75.75 0 01-1.5 0V6.75A.75.75 0 019 6zm6.75 3a.75.75 0 00-1.5 0v8.25a.75.75 0 001.5 0V9z" clip-rule="evenodd" />
          </svg>
        </div>
        <div>
          <h3 class="positioner-title">Posicionador de Alunos</h3>
          <p class="positioner-subtitle">Organize estrategicamente a sala</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button @click="savePositions" class="action-btn primary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
            <path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
          </svg>
          Salvar Posições
        </button>
      </div>
    </div>
    
    <div class="positioner-content">
      <div class="controls-panel">
        <div class="control-section">
          <h4 class="section-title">Modo de Visualização</h4>
          <div class="view-mode-buttons">
            <button 
              @click="viewMode = '2d'" 
              class="mode-btn"
              :class="{ active: viewMode === '2d' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M3 6a3 3 0 013-3h2.25a3 3 0 013 3v2.25a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm9.75 0a3 3 0 013-3H18a3 3 0 013 3v2.25a3 3 0 01-3 3h-2.25a3 3 0 01-3-3V6zM3 15.75a3 3 0 013-3h2.25a3 3 0 013 3V18a3 3 0 01-3 3H6a3 3 0 01-3-3v-2.25zm9.75 0a3 3 0 013-3H18a3 3 0 013 3V18a3 3 0 01-3 3h-2.25a3 3 0 01-3-3v-2.25z" clip-rule="evenodd" />
              </svg>
              <span>2D</span>
            </button>
            
            <button 
              @click="viewMode = '3d'" 
              class="mode-btn"
              :class="{ active: viewMode === '3d' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 .75a8.25 8.25 0 00-4.135 15.39c.686.398 1.115 1.008 1.134 1.623a.75.75 0 00.577.706c.352.083.71.148 1.074.195.323.041.6-.218.6-.544v-4.661a6.714 6.714 0 01-.937-.171.75.75 0 11.374-1.453 5.261 5.261 0 002.626 0 .75.75 0 11.374 1.452 6.712 6.712 0 01-.937.172v4.66c0 .327.277.586.6.545.364-.047.722-.112 1.074-.195a.75.75 0 00.577-.706c.02-.615.448-1.225 1.134-1.623A8.25 8.25 0 0012 .75z" />
                <path fill-rule="evenodd" d="M9.013 19.9a.75.75 0 01.877-.597 11.319 11.319 0 004.22 0 .75.75 0 11.28 1.473 12.819 12.819 0 01-4.78 0 .75.75 0 01-.597-.876zM9.754 22.344a.75.75 0 01.824-.668 13.682 13.682 0 002.844 0 .75.75 0 11.156 1.492 15.156 15.156 0 01-3.156 0 .75.75 0 01-.668-.824z" clip-rule="evenodd" />
              </svg>
              <span>3D</span>
            </button>
          </div>
        </div>
        
        <div class="control-section">
          <h4 class="section-title">Filtros</h4>
          <div class="filter-buttons">
            <button 
              v-for="filter in filters" 
              :key="filter.key"
              @click="toggleFilter(filter.key)"
              class="filter-btn"
              :class="{ active: activeFilters.includes(filter.key) }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
              </svg>
              <span>{{ filter.label }}</span>
            </button>
          </div>
        </div>
        
        <div class="students-info">
          <div class="info-card">
            <span class="info-label">Total</span>
            <span class="info-value">{{ filteredStudents.length }}</span>
          </div>
          <div class="info-card">
            <span class="info-label">Selecionado</span>
            <span class="info-value">{{ selectedStudent ? '1' : '0' }}</span>
          </div>
        </div>
      </div>
      
      <div class="positioning-area">
        <div v-if="viewMode === '2d'" class="grid-2d">
          <div 
            v-for="student in filteredStudents" 
            :key="student.id"
            class="student-marker"
            :class="{
              'vision-issue': student.visionIssues,
              'selected': selectedStudent === student.id,
              'dragging': student.dragging
            }"
            :style="{
              left: `${student.position?.x || 50}%`,
              top: `${student.position?.y || 50}%`
            }"
            draggable="true"
            @dragstart="startDrag($event, student.id)"
            @dragend="stopDrag(student.id)"
            @click="selectStudent(student.id)"
          >
            <div class="marker-avatar">{{ getInitials(student.name) }}</div>
            <div class="marker-name">{{ student.name.split(' ')[0] }}</div>
          </div>
        </div>
        
        <div v-else class="grid-3d">
          <div class="placeholder-3d">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 .75a8.25 8.25 0 00-4.135 15.39c.686.398 1.115 1.008 1.134 1.623a.75.75 0 00.577.706c.352.083.71.148 1.074.195.323.041.6-.218.6-.544v-4.661a6.714 6.714 0 01-.937-.171.75.75 0 11.374-1.453 5.261 5.261 0 002.626 0 .75.75 0 11.374 1.452 6.712 6.712 0 01-.937.172v4.66c0 .327.277.586.6.545.364-.047.722-.112 1.074-.195a.75.75 0 00.577-.706c.02-.615.448-1.225 1.134-1.623A8.25 8.25 0 0012 .75z" />
              <path fill-rule="evenodd" d="M9.013 19.9a.75.75 0 01.877-.597 11.319 11.319 0 004.22 0 .75.75 0 11.28 1.473 12.819 12.819 0 01-4.78 0 .75.75 0 01-.597-.876zM9.754 22.344a.75.75 0 01.824-.668 13.682 13.682 0 002.844 0 .75.75 0 11.156 1.492 15.156 15.156 0 01-3.156 0 .75.75 0 01-.668-.824z" clip-rule="evenodd" />
            </svg>
            <p>Visualização 3D</p>
            <span>Requer biblioteca Three.js</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  classroomId: String
})

const viewMode = ref('2d')
const selectedStudent = ref(null)
const activeFilters = ref([])

const filters = [
  { key: 'vision', label: 'Dificuldade Visual' },
  { key: 'math', label: 'Matemática Baixa' },
  { key: 'language', label: 'Linguagem Baixa' }
]

const students = ref([
  { id: 1, name: 'João Silva', visionIssues: false, position: { x: 20, y: 30 }, skills: { math: 85, language: 78 }, dragging: false },
  { id: 2, name: 'Maria Santos', visionIssues: true, position: { x: 40, y: 50 }, skills: { math: 92, language: 88 }, dragging: false },
  { id: 3, name: 'Pedro Costa', visionIssues: false, position: { x: 60, y: 40 }, skills: { math: 55, language: 82 }, dragging: false },
  { id: 4, name: 'Ana Oliveira', visionIssues: false, position: { x: 30, y: 70 }, skills: { math: 88, language: 90 }, dragging: false },
  { id: 5, name: 'Carlos Souza', visionIssues: true, position: { x: 70, y: 60 }, skills: { math: 70, language: 55 }, dragging: false }
])

const filteredStudents = computed(() => {
  if (activeFilters.value.length === 0) return students.value
  
  return students.value.filter(student => {
    return activeFilters.value.some(filter => {
      if (filter === 'vision') return student.visionIssues
      if (filter === 'math') return student.skills?.math < 60
      if (filter === 'language') return student.skills?.language < 60
      return true
    })
  })
})

function getInitials(name) {
  const parts = name.split(' ')
  return parts.length >= 2 
    ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

function toggleFilter(key) {
  const index = activeFilters.value.indexOf(key)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(key)
  }
}

function startDrag(event, studentId) {
  const student = students.value.find(s => s.id === studentId)
  if (student) student.dragging = true
}

function stopDrag(studentId) {
  const student = students.value.find(s => s.id === studentId)
  if (student) student.dragging = false
}

function selectStudent(studentId) {
  selectedStudent.value = selectedStudent.value === studentId ? null : studentId
}

function savePositions() {
  console.log('Salvando posições...', students.value)
}
</script>

<style scoped>
.student-positioner {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  overflow: hidden;
}

.positioner-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(45, 83, 26, 0.1), transparent 60%);
  pointer-events: none;
}

.positioner-header {
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
  box-shadow: 0 8px 16px rgba(45, 83, 26, 0.3);
}

.header-icon svg {
  width: 2rem;
  height: 2rem;
  color: #e1d4c2;
}

.positioner-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
}

.positioner-subtitle {
  font-size: 0.875rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0.25rem 0 0 0;
}

.header-actions .action-btn {
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
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

.btn-icon {
  width: 1.125rem;
  height: 1.125rem;
}

.positioner-content {
  display: grid;
  grid-template-columns: 280px 1fr;
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

.view-mode-buttons,
.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.mode-btn,
.filter-btn {
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

.mode-btn:hover,
.filter-btn:hover {
  border-color: #2d531a;
}

.mode-btn.active,
.filter-btn.active {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  border-color: transparent;
}

.mode-btn svg,
.filter-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.students-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.info-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: #ffffff;
  border-radius: 0.75rem;
  border: 2px solid rgba(45, 83, 26, 0.2);
}

.info-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.6;
  text-transform: uppercase;
}

.info-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: #2d531a;
  margin-top: 0.25rem;
}

.positioning-area {
  background: rgba(225, 212, 194, 0.2);
  border-radius: 1rem;
  padding: 2rem;
  min-height: 600px;
  position: relative;
}

.grid-2d {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 550px;
  background-image: radial-gradient(circle, rgba(45, 83, 26, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  border-radius: 0.75rem;
}

.student-marker {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  cursor: move;
  transition: all 0.2s ease;
  transform: translate(-50%, -50%);
}

.student-marker:hover {
  transform: translate(-50%, -50%) scale(1.1);
  z-index: 10;
}

.student-marker.selected {
  z-index: 20;
}

.student-marker.dragging {
  opacity: 0.7;
  z-index: 30;
}

.marker-avatar {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 700;
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
  border: 3px solid #ffffff;
}

.student-marker.vision-issue .marker-avatar {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.3);
}

.student-marker.selected .marker-avatar {
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.3);
}

.marker-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  background: #ffffff;
  padding: 0.25rem 0.625rem;
  border-radius: 0.375rem;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(31, 29, 32, 0.1);
}

.grid-3d {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 550px;
}

.placeholder-3d {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #9ca3af;
}

.placeholder-3d svg {
  width: 4rem;
  height: 4rem;
  opacity: 0.5;
}

.placeholder-3d p {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.placeholder-3d span {
  font-size: 0.875rem;
}

@media (max-width: 1024px) {
  .positioner-content {
    grid-template-columns: 1fr;
  }
}
</style>