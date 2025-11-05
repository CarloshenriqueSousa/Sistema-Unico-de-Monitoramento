<template>
  <div class="group-manager">
    <div class="manager-background"></div>
    
    <div class="manager-header">
      <div class="header-content">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M4.5 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM14.25 8.625a3.375 3.375 0 116.75 0 3.375 3.375 0 01-6.75 0zM1.5 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM17.25 19.128l-.001.144a2.25 2.25 0 01-.233.96 10.088 10.088 0 005.06-1.01.75.75 0 00.42-.643 4.875 4.875 0 00-6.957-4.611 8.586 8.586 0 011.71 5.157v.003z" />
          </svg>
        </div>
        <div>
          <h3 class="manager-title">Gerenciador de Grupos</h3>
          <p class="manager-subtitle">Organize alunos em grupos colaborativos</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button @click="addGroup" class="action-btn secondary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
          </svg>
          Novo Grupo
        </button>
        
        <button @click="saveGroups" class="action-btn primary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 2.75a.75.75 0 00-1.5 0v8.614L6.295 8.235a.75.75 0 10-1.09 1.03l4.25 4.5a.75.75 0 001.09 0l4.25-4.5a.75.75 0 00-1.09-1.03l-2.955 3.129V2.75z" />
            <path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
          </svg>
          Salvar Grupos
        </button>
      </div>
    </div>
    
    <div class="groups-container">
      <div 
        v-for="(group, index) in groups" 
        :key="index"
        class="group-card"
        :style="{ '--group-index': index }"
      >
        <div class="group-header">
          <div class="group-number">Grupo {{ index + 1 }}</div>
          <button @click="removeGroup(index)" class="remove-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.52.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <div class="group-members">
          <div 
            v-for="student in group" 
            :key="student.id"
            class="member-card"
            draggable="true"
          >
            <div class="member-avatar">{{ getInitials(student.name) }}</div>
            <div class="member-info">
              <div class="member-name">{{ student.name }}</div>
              <div class="member-skills">
                <span class="skill-badge">Mat: {{ student.skills?.math || 0 }}%</span>
                <span class="skill-badge">Lng: {{ student.skills?.language || 0 }}%</span>
              </div>
            </div>
          </div>
          
          <div v-if="group.length === 0" class="empty-group">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z" clip-rule="evenodd" />
            </svg>
            <span>Arraste alunos aqui</span>
          </div>
        </div>
        
        <div class="group-stats">
          <div class="stat-item">
            <span class="stat-label">Média</span>
            <span class="stat-value">{{ calculateGroupAverage(group) }}%</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Membros</span>
            <span class="stat-value">{{ group.length }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="ungrouped-section">
      <h4 class="section-title">Alunos Disponíveis</h4>
      <div class="ungrouped-grid">
        <div 
          v-for="student in ungroupedStudents" 
          :key="student.id"
          class="ungrouped-card"
          draggable="true"
        >
          <div class="ungrouped-avatar">{{ getInitials(student.name) }}</div>
          <span class="ungrouped-name">{{ student.name }}</span>
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

const groups = ref([
  [
    { id: 1, name: 'João Silva', skills: { math: 85, language: 78 } },
    { id: 2, name: 'Maria Santos', skills: { math: 92, language: 88 } }
  ],
  [
    { id: 3, name: 'Pedro Costa', skills: { math: 76, language: 82 } }
  ],
  []
])

const allStudents = ref([
  { id: 1, name: 'João Silva', skills: { math: 85, language: 78 } },
  { id: 2, name: 'Maria Santos', skills: { math: 92, language: 88 } },
  { id: 3, name: 'Pedro Costa', skills: { math: 76, language: 82 } },
  { id: 4, name: 'Ana Oliveira', skills: { math: 88, language: 90 } },
  { id: 5, name: 'Carlos Souza', skills: { math: 70, language: 75 } }
])

const ungroupedStudents = computed(() => {
  const groupedIds = new Set()
  groups.value.forEach(group => {
    group.forEach(student => groupedIds.add(student.id))
  })
  return allStudents.value.filter(s => !groupedIds.has(s.id))
})

const getInitials = (name) => {
  const parts = name.split(' ')
  return parts.length >= 2 
    ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

const calculateGroupAverage = (group) => {
  if (group.length === 0) return 0
  const total = group.reduce((sum, student) => {
    const avg = ((student.skills?.math || 0) + (student.skills?.language || 0)) / 2
    return sum + avg
  }, 0)
  return Math.round(total / group.length)
}

const addGroup = () => {
  groups.value.push([])
}

const removeGroup = (index) => {
  if (groups.value.length > 1) {
    groups.value.splice(index, 1)
  }
}

const saveGroups = () => {
  console.log('Salvando grupos...', groups.value)
}
</script>

<style scoped>
.group-manager {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  overflow: hidden;
}

.manager-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(225, 212, 194, 0.3), transparent 60%);
  pointer-events: none;
}

.manager-header {
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

.manager-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
}

.manager-subtitle {
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

.groups-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
  position: relative;
}

.group-card {
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.group-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(31, 29, 32, 0.1);
  border-color: rgba(45, 83, 26, 0.4);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(45, 83, 26, 0.1), rgba(15, 30, 63, 0.1));
  border-bottom: 2px solid rgba(45, 83, 26, 0.1);
}

.group-number {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f1d20;
}

.remove-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: #dc2626;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: rgba(220, 38, 38, 0.1);
}

.remove-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.group-members {
  padding: 1.25rem;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 0.75rem;
  cursor: move;
  transition: all 0.2s ease;
}

.member-card:hover {
  background: rgba(225, 212, 194, 0.5);
  transform: translateX(4px);
}

.member-avatar {
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
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1f1d20;
  margin-bottom: 0.25rem;
}

.member-skills {
  display: flex;
  gap: 0.5rem;
}

.skill-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  background: #ffffff;
  border-radius: 0.25rem;
  color: #0f1e3f;
  font-weight: 600;
}

.empty-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: #9ca3af;
  text-align: center;
}

.empty-group svg {
  width: 3rem;
  height: 3rem;
  opacity: 0.5;
}

.group-stats {
  display: flex;
  justify-content: space-around;
  padding: 1rem 1.25rem;
  background: rgba(225, 212, 194, 0.2);
  border-top: 2px solid rgba(45, 83, 26, 0.1);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.6;
  text-transform: uppercase;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #2d531a;
}

.ungrouped-section {
  padding: 2rem;
  background: rgba(225, 212, 194, 0.2);
  border-top: 2px solid rgba(45, 83, 26, 0.1);
  position: relative;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1f1d20;
  margin: 0 0 1rem 0;
}

.ungrouped-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.ungrouped-card {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.75rem;
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  cursor: move;
  transition: all 0.2s ease;
}

.ungrouped-card:hover {
  border-color: #2d531a;
  transform: translateY(-2px);
}

.ungrouped-avatar {
  width: 2rem;
  height: 2rem;
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

.ungrouped-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f1d20;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .groups-container {
    grid-template-columns: 1fr;
  }
  
  .ungrouped-grid {
    grid-template-columns: 1fr;
  }
}
</style>