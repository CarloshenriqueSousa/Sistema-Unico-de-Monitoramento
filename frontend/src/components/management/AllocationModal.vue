<template>
  <div class="allocation-modal-overlay" @click.self="$emit('close')">
    <div class="allocation-modal">
      <div class="modal-background"></div>
      
      <div class="modal-header">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M7.502 6h7.128A3.375 3.375 0 0118 9.375v9.375a3 3 0 003-3V6.108c0-1.505-1.125-2.811-2.664-2.94a48.972 48.972 0 00-.673-.05A3 3 0 0015 1.5h-1.5a3 3 0 00-2.663 1.618c-.225.015-.45.032-.673.05C8.662 3.295 7.554 4.542 7.502 6zM13.5 3A1.5 1.5 0 0012 4.5h4.5A1.5 1.5 0 0015 3h-1.5z" clip-rule="evenodd" />
            <path fill-rule="evenodd" d="M3 9.375C3 8.339 3.84 7.5 4.875 7.5h9.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 013 20.625V9.375zm9.586 4.594a.75.75 0 00-1.172-.938l-2.476 3.096-.908-.907a.75.75 0 00-1.06 1.06l1.5 1.5a.75.75 0 001.116-.062l3-3.75z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="header-content">
          <h3 class="modal-title">
            {{ allocation ? 'Editar Alocação' : 'Nova Alocação' }}
          </h3>
          <p class="modal-subtitle">Configure os detalhes da alocação</p>
        </div>
        <button @click="$emit('close')" class="close-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Recurso</label>
            <select v-model="formData.resourceId" class="form-select">
              <option v-for="resource in resources" :key="resource.id" :value="resource.id">
                {{ resource.name }} ({{ resource.type }})
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Turma</label>
            <select v-model="formData.class" class="form-select">
              <option v-for="classroom in classrooms" :key="classroom" :value="classroom">
                {{ classroom }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Dia da Semana</label>
            <select v-model="formData.day" class="form-select">
              <option v-for="day in weekDays" :key="day" :value="day">
                {{ day }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Horário</label>
            <select v-model="formData.time" class="form-select">
              <option v-for="slot in timeSlots" :key="slot.id" :value="slot.time">
                {{ slot.time }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Status</label>
            <select v-model="formData.status" class="form-select">
              <option v-for="status in statusOptions" :key="status" :value="status">
                {{ status }}
              </option>
            </select>
          </div>
          
          <div class="form-group full-width">
            <label class="form-label">Professor Responsável</label>
            <input 
              v-model="formData.teacher" 
              type="text" 
              class="form-input"
              placeholder="Nome do professor"
            />
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="$emit('close')" class="btn-secondary">
          Cancelar
        </button>
        <button @click="saveAllocation" class="btn-primary" :disabled="saving">
          <svg v-if="saving" class="loading-spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>{{ allocation ? 'Atualizar' : 'Criar' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  allocation: Object,
  resources: Array
})

const emit = defineEmits(['close', 'save'])

const formData = ref({
  resourceId: 1,
  resource: '',
  type: '',
  class: '1A',
  day: 'Segunda',
  time: '07:00 - 08:00',
  teacher: '',
  status: 'Alocado'
})

const saving = ref(false)

const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
const timeSlots = [
  { id: 1, time: '07:00 - 08:00' },
  { id: 2, time: '08:00 - 09:00' },
  { id: 3, time: '09:00 - 10:00' },
  { id: 4, time: '10:00 - 11:00' },
  { id: 5, time: '11:00 - 12:00' },
  { id: 6, time: '13:00 - 14:00' },
  { id: 7, time: '14:00 - 15:00' },
  { id: 8, time: '15:00 - 16:00' },
  { id: 9, time: '16:00 - 17:00' }
]
const statusOptions = ['Liberado', 'Alocado', 'Manutenção', 'Bloqueado']
const classrooms = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B']

watch(() => props.allocation, (newVal) => {
  if (newVal) {
    formData.value = {
      resourceId: newVal.id,
      resource: newVal.resource,
      type: newVal.type,
      class: newVal.class,
      day: newVal.day,
      time: newVal.time,
      teacher: newVal.teacher,
      status: newVal.status
    }
  }
}, { immediate: true })

const saveAllocation = async () => {
  saving.value = true
  
  const resource = props.resources.find(r => r.id === formData.value.resourceId)
  
  const allocationData = {
    ...formData.value,
    resource: resource?.name || '',
    type: resource?.type || ''
  }
  
  setTimeout(() => {
    emit('save', allocationData)
    saving.value = false
  }, 800)
}
</script>

<style scoped>
.allocation-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(31, 29, 32, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.allocation-modal {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  width: 100%;
  max-width: 42rem;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(31, 29, 32, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(225, 212, 194, 0.3), transparent 60%);
  pointer-events: none;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  border-bottom: 2px solid rgba(45, 83, 26, 0.1);
  position: relative;
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

.header-content {
  flex: 1;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
  line-height: 1.2;
}

.modal-subtitle {
  font-size: 0.875rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0.25rem 0 0 0;
}

.close-btn {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(225, 212, 194, 0.3);
  border: none;
  border-radius: 0.75rem;
  color: #1f1d20;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.close-btn:hover {
  background: rgba(225, 212, 194, 0.5);
  transform: rotate(90deg);
}

.close-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.modal-body {
  padding: 2rem;
  position: relative;
  max-height: 60vh;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f1d20;
}

.form-select,
.form-input {
  padding: 0.875rem 1rem;
  background: rgba(225, 212, 194, 0.2);
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  font-size: 0.9375rem;
  color: #1f1d20;
  font-weight: 500;
  transition: all 0.2s ease;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #2d531a;
  background: rgba(225, 212, 194, 0.3);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem 2rem;
  border-top: 2px solid rgba(45, 83, 26, 0.1);
  position: relative;
}

.btn-secondary,
.btn-primary {
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary {
  background: #e1d4c2;
  color: #1f1d20;
}

.btn-secondary:hover {
  background: #d4c7b5;
}

.btn-primary {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 1.25rem;
  height: 1.25rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-header {
    padding: 1.5rem;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
}
</style>