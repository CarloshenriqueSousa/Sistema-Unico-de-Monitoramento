<template>
  <div class="seat-editor">
    <div class="editor-background"></div>
    
    <div class="editor-header">
      <div class="header-content">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M3 6a3 3 0 013-3h2.25a3 3 0 013 3v2.25a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm9.75 0a3 3 0 013-3H18a3 3 0 013 3v2.25a3 3 0 01-3 3h-2.25a3 3 0 01-3-3V6zM3 15.75a3 3 0 013-3h2.25a3 3 0 013 3V18a3 3 0 01-3 3H6a3 3 0 01-3-3v-2.25zm9.75 0a3 3 0 013-3H18a3 3 0 013 3V18a3 3 0 01-3 3h-2.25a3 3 0 01-3-3v-2.25z" clip-rule="evenodd" />
          </svg>
        </div>
        <div>
          <h3 class="editor-title">Editor de Assentos</h3>
          <p class="editor-subtitle">Organize os alunos na sala de aula</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button @click="resetSeats" class="action-btn secondary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 01-9.201 2.466l-.312-.311h2.433a.75.75 0 000-1.5H3.989a.75.75 0 00-.75.75v4.242a.75.75 0 001.5 0v-2.43l.31.31a7 7 0 0011.712-3.138.75.75 0 00-1.449-.39zm1.23-3.723a.75.75 0 00.219-.53V2.929a.75.75 0 00-1.5 0V5.36l-.31-.31A7 7 0 003.239 8.188a.75.75 0 101.448.389A5.5 5.5 0 0113.89 6.11l.311.31h-2.432a.75.75 0 000 1.5h4.243a.75.75 0 00.53-.219z" clip-rule="evenodd" />
          </svg>
          Resetar
        </button>
        
        <button @click="saveSeats" class="action-btn primary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
            <path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
          </svg>
          Salvar Layout
        </button>
      </div>
    </div>
    
    <div class="editor-content">
      <div class="sidebar">
        <div class="sidebar-section">
          <h4 class="section-title">Alunos Disponíveis</h4>
          <div class="students-list">
            <div 
              v-for="student in availableStudents" 
              :key="student.id"
              class="student-item"
              draggable="true"
              @dragstart="startDrag($event, student)"
            >
              <div class="student-avatar">{{ getInitials(student.name) }}</div>
              <span class="student-name">{{ student.name }}</span>
              <div v-if="student.visionIssues" class="vision-badge">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z" />
                  <path fill-rule="evenodd" d="M.664 10.59a1.651 1.651 0 010-1.186A10.004 10.004 0 0110 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0110 17c-4.257 0-7.893-2.66-9.336-6.41zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <div class="sidebar-section">
          <h4 class="section-title">Layouts</h4>
          <div class="layout-buttons">
            <button @click="changeLayout('rows')" class="layout-btn" :class="{ active: layout === 'rows' }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M3 6a3 3 0 013-3h2.25a3 3 0 013 3v2.25a3 3 0 01-3 3H6a3 3 0 01-3-3V6zm9.75 0a3 3 0 013-3H18a3 3 0 013 3v2.25a3 3 0 01-3 3h-2.25a3 3 0 01-3-3V6zM3 15.75a3 3 0 013-3h2.25a3 3 0 013 3V18a3 3 0 01-3 3H6a3 3 0 01-3-3v-2.25zm9.75 0a3 3 0 013-3H18a3 3 0 013 3V18a3 3 0 01-3 3h-2.25a3 3 0 01-3-3v-2.25z" clip-rule="evenodd" />
              </svg>
              <span>Fileiras</span>
            </button>
            
            <button @click="changeLayout('groups')" class="layout-btn" :class="{ active: layout === 'groups' }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M4.5 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM14.25 8.625a3.375 3.375 0 116.75 0 3.375 3.375 0 01-6.75 0zM1.5 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM17.25 19.128l-.001.144a2.25 2.25 0 01-.233.96 10.088 10.088 0 005.06-1.01.75.75 0 00.42-.643 4.875 4.875 0 00-6.957-4.611 8.586 8.586 0 011.71 5.157v.003z" />
              </svg>
              <span>Grupos</span>
            </button>
            
            <button @click="changeLayout('circle')" class="layout-btn" :class="{ active: layout === 'circle' }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z" clip-rule="evenodd" />
              </svg>
              <span>Círculo</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="seats-area">
        <div class="seats-grid">
          <div 
            v-for="(seat, index) in seats" 
            :key="index"
            class="seat"
            :class="{
              'occupied': seat.student,
              'vision-issue': seat.student?.visionIssues
            }"
            @dragover.prevent
            @drop="dropStudent($event, index)"
          >
            <div v-if="seat.student" class="seat-content">
              <div class="seat-avatar">{{ getInitials(seat.student.name) }}</div>
              <div class="seat-name">{{ seat.student.name.split(' ')[0] }}</div>
              <button @click="removeSeat(index)" class="remove-btn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                </svg>
              </button>
            </div>
            <div v-else class="seat-empty">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z" clip-rule="evenodd" />
              </svg>
            </div>
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

const layout = ref('rows')

const allStudents = ref([
  { id: 1, name: 'João Silva', visionIssues: false },
  { id: 2, name: 'Maria Santos', visionIssues: true },
  { id: 3, name: 'Pedro Costa', visionIssues: false },
  { id: 4, name: 'Ana Oliveira', visionIssues: false },
  { id: 5, name: 'Carlos Souza', visionIssues: true }
])

const seats = ref(generateSeats('rows'))

const availableStudents = computed(() => {
  const seatedIds = new Set(seats.value.filter(s => s.student).map(s => s.student.id))
  return allStudents.value.filter(s => !seatedIds.has(s.id))
})

function generateSeats(layoutType) {
  const configs = {
    rows: { count: 25, grid: 'repeat(5, 1fr)' },
    groups: { count: 20, grid: 'repeat(4, 1fr)' },
    circle: { count: 16, grid: 'repeat(4, 1fr)' }
  }
  
  return Array.from({ length: configs[layoutType].count }, () => ({
    student: null
  }))
}

function getInitials(name) {
  const parts = name.split(' ')
  return parts.length >= 2 
    ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

function startDrag(event, student) {
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('studentId', student.id)
}

function dropStudent(event, seatIndex) {
  const studentId = parseInt(event.dataTransfer.getData('studentId'))
  const student = allStudents.value.find(s => s.id === studentId)
  
  if (student && !seats.value[seatIndex].student) {
    seats.value[seatIndex].student = { ...student }
  }
}

function removeSeat(index) {
  seats.value[index].student = null
}

function changeLayout(newLayout) {
  layout.value = newLayout
  seats.value = generateSeats(newLayout)
}

function resetSeats() {
  seats.value.forEach(seat => seat.student = null)
}

function saveSeats() {
  console.log('Salvando layout de assentos...', seats.value)
}
</script>

<style scoped>
.seat-editor {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  overflow: hidden;
}

.editor-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at bottom left, rgba(225, 212, 194, 0.3), transparent 60%);
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
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  padding: 2rem;
  position: relative;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-section {
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

.students-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  max-height: 400px;
  overflow-y: auto;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  cursor: move;
  transition: all 0.2s ease;
}

.student-item:hover {
  border-color: #2d531a;
  transform: translateX(4px);
}

.student-avatar {
  width: 2.25rem;
  height: 2.25rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #e1d4c2;
  flex-shrink: 0;
}

.student-name {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f1d20;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vision-badge {
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7c3aed;
}

.vision-badge svg {
  width: 1.125rem;
  height: 1.125rem;
}

.layout-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.layout-btn {
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

.layout-btn:hover {
  border-color: #2d531a;
}

.layout-btn.active {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  border-color: transparent;
}

.layout-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.seats-area {
  background: rgba(225, 212, 194, 0.2);
  border-radius: 1rem;
  padding: 2rem;
  min-height: 600px;
}

.seats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}

.seat {
  aspect-ratio: 1;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  position: relative;
}

.seat:hover {
  border-color: #2d531a;
  transform: scale(1.05);
}

.seat.occupied {
  background: linear-gradient(135deg, rgba(45, 83, 26, 0.1), rgba(15, 30, 63, 0.1));
  border-color: #2d531a;
}

.seat.vision-issue {
  border-color: #7c3aed;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
}

.seat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.seat-avatar {
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 700;
  color: #e1d4c2;
}

.seat-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  text-align: center;
}

.remove-btn {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  width: 1.5rem;
  height: 1.5rem;
  background: #dc2626;
  border: none;
  border-radius: 0.375rem;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.seat:hover .remove-btn {
  opacity: 1;
}

.remove-btn svg {
  width: 1rem;
  height: 1rem;
}

.seat-empty {
  width: 2rem;
  height: 2rem;
  color: #9ca3af;
  opacity: 0.5;
}

.seat-empty svg {
  width: 100%;
  height: 100%;
}

@media (max-width: 1024px) {
  .editor-content {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    order: 2;
  }
  
  .seats-area {
    order: 1;
  }
}

@media (max-width: 640px) {
  .seats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>