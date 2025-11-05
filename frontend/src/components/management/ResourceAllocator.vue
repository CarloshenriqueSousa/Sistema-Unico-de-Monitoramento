<template>
  <div class="resource-allocator">
    <!-- Header Section -->
    <div class="header-section">
      <div class="header-content">
        <div class="title-group">
          <div class="icon-wrapper">
            <i class="fas fa-boxes"></i>
          </div>
          <div>
            <h2 class="main-title">Alocador de Recursos</h2>
            <p class="subtitle">Gerencie e otimize o uso dos recursos escolares</p>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="showCalendar = !showCalendar" class="btn-secondary">
            <i :class="showCalendar ? 'fas fa-list' : 'fas fa-calendar'"></i>
            <span>{{ showCalendar ? 'Ver Lista' : 'Ver Calendário' }}</span>
          </button>
          <button @click="showAllocationModal" class="btn-primary">
            <i class="fas fa-plus"></i>
            <span>Alocar Recurso</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Calendar View -->
    <div v-if="showCalendar" class="calendar-section">
      <div class="calendar-card">
        <!-- Calendar Controls -->
        <div class="calendar-controls">
          <div class="navigation-group">
            <button @click="prevWeek" class="nav-btn">
              <i class="fas fa-chevron-left"></i>
            </button>
            <div class="week-info">
              <i class="fas fa-calendar-week"></i>
              <h4 class="week-range">{{ currentWeekRange }}</h4>
            </div>
            <button @click="nextWeek" class="nav-btn">
              <i class="fas fa-chevron-right"></i>
            </button>
            <button @click="currentDate = new Date()" class="today-btn">
              <i class="fas fa-calendar-day"></i>
              Hoje
            </button>
          </div>
          
          <div class="filter-controls">
            <select v-model="selectedResourceType" class="select-filter">
              <option value="">Todos os Recursos</option>
              <option v-for="type in resourceTypes" :key="type" :value="type">{{ type }}</option>
            </select>
            <button class="icon-btn">
              <i class="fas fa-download"></i>
            </button>
          </div>
        </div>

        <!-- Calendar Grid -->
        <div class="calendar-grid-wrapper">
          <!-- Days Header -->
          <div class="calendar-header">
            <div class="time-column-header">Horário</div>
            <div class="days-row">
              <div v-for="day in weekDays" :key="day" class="day-header">
                <span class="day-label">{{ day }}</span>
              </div>
            </div>
          </div>

          <!-- Time Slots -->
          <div class="calendar-body">
            <div v-for="timeSlot in timeSlots" :key="timeSlot.id" class="time-row">
              <div class="time-column">
                <i class="fas fa-clock"></i>
                <span>{{ timeSlot.time }}</span>
              </div>
              
              <div class="slots-container">
                <div
                  v-for="(day, index) in weekDays"
                  :key="index"
                  class="resource-slot"
                  @dragover.prevent
                  @drop="handleResourceDrop($event, day, timeSlot)"
                >
                  <div
                    v-for="allocation in getAllocationsForSlot(day, timeSlot)"
                    :key="allocation.id"
                    draggable="true"
                    @dragstart="handleDragStart($event, allocation)"
                    :class="['allocation-card', allocationClass(allocation)]"
                  >
                    <div class="allocation-header">
                      <div class="resource-icon-small">
                        <i :class="resourceIcon(allocation.type)"></i>
                      </div>
                      <span class="resource-name">{{ allocation.resource }}</span>
                      <i class="fas fa-grip-vertical drag-icon"></i>
                    </div>
                    <div class="allocation-info">
                      <span class="class-tag">{{ allocation.class }}</span>
                      <span class="teacher-name">{{ allocation.teacher }}</span>
                    </div>
                  </div>
                  
                  <div v-if="getAllocationsForSlot(day, timeSlot).length === 0" class="empty-slot">
                    <i class="fas fa-plus-circle"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="list-section">
      <div class="list-card">
        <!-- Filters Bar -->
        <div class="filters-bar">
          <div class="search-wrapper">
            <i class="fas fa-search"></i>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar recurso, turma ou professor..." 
              class="search-input"
            >
          </div>
          
          <div class="filters-group">
            <select v-model="selectedResourceType" class="select-filter">
              <option value="">Tipo de Recurso</option>
              <option v-for="type in resourceTypes" :key="type" :value="type">{{ type }}</option>
            </select>
            
            <select v-model="selectedStatus" class="select-filter">
              <option value="">Status</option>
              <option v-for="status in statusOptions" :key="status" :value="status">{{ status }}</option>
            </select>
            
            <button class="filter-btn">
              <i class="fas fa-sliders-h"></i>
              Filtros
            </button>
          </div>
        </div>

        <!-- Resources Table -->
        <div class="table-wrapper">
          <table class="resources-table">
            <thead>
              <tr>
                <th>Recurso</th>
                <th>Tipo</th>
                <th>Turma</th>
                <th>Horário</th>
                <th>Status</th>
                <th class="text-center">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredResources" :key="item.id" class="table-row">
                <td>
                  <div class="resource-cell">
                    <div class="resource-icon-container" :class="getIconBg(item.type)">
                      <i :class="resourceIcon(item.type)"></i>
                    </div>
                    <span class="resource-title">{{ item.resource }}</span>
                  </div>
                </td>
                <td>
                  <span class="type-badge">{{ item.type }}</span>
                </td>
                <td>
                  <div class="class-info">
                    <i class="fas fa-users"></i>
                    <span>{{ item.class }}</span>
                  </div>
                </td>
                <td class="time-cell">{{ item.time }}</td>
                <td>
                  <span :class="['status-pill', statusBadgeClass(item.status)]">
                    <span class="status-dot"></span>
                    {{ item.status }}
                  </span>
                </td>
                <td>
                  <div class="actions-cell">
                    <button @click="editAllocation(item)" class="action-btn edit-btn" title="Editar">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteAllocation(item)" class="action-btn delete-btn" title="Excluir">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                    <button @click="toggleStatus(item)" class="action-btn toggle-btn" title="Alterar Status">
                      <i :class="item.status === 'Liberado' ? 'fas fa-lock' : 'fas fa-unlock'"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="filteredResources.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="fas fa-search"></i>
            </div>
            <h4>Nenhum recurso encontrado</h4>
            <p>Tente ajustar os filtros ou adicionar novos recursos</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Allocation Modal -->
    <AllocationModal 
      v-if="showModal"
      :allocation="selectedAllocation"
      :resources="resourcesList"
      @close="showModal = false"
      @save="handleSaveAllocation"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import DynamicTable from '@/shared/DynamicTable.vue';
import Button from '@/shared/Button.vue';
import AllocationModal from '@/components/management/AllocationModal.vue';
import { fetchResources, createAllocation, updateAllocation, deleteAllocation } from '@/services/resourceService';
import type { ResourceAllocation } from '@/types';

export default defineComponent({
  name: 'ResourceAllocator',
  components: { AllocationModal },
  setup() {
    const resources = ref<ResourceAllocation[]>([
      { id: 1, resource: 'Sala de Almoço', type: 'Alimentação', class: '9º A', time: '12:00 - 13:00', status: 'Alocado', teacher: 'Prof. Silva', day: 'Seg' },
      { id: 2, resource: 'Lab. Informática', type: 'Educacional', class: '8º B', time: '14:00 - 15:00', status: 'Liberado', teacher: 'Prof. Costa', day: 'Ter' },
      { id: 3, resource: 'Quadra Poliesportiva', type: 'Esportivo', class: '7º C', time: '10:00 - 11:00', status: 'Manutenção', teacher: 'Prof. Santos', day: 'Qua' },
      { id: 4, resource: 'Auditório', type: 'Eventos', class: 'Todos', time: '16:00 - 17:00', status: 'Bloqueado', teacher: 'Direção', day: 'Qui' },
      { id: 5, resource: 'Biblioteca', type: 'Educacional', class: '6º A', time: '09:00 - 10:00', status: 'Liberado', teacher: 'Prof. Lima', day: 'Sex' }
    ]);
    
    const resourcesList = ref([
      { id: 1, name: 'Sala de Almoço', type: 'Alimentação' },
      { id: 2, name: 'Laboratório de Informática', type: 'Educacional' },
      { id: 3, name: 'Quadra Poliesportiva', type: 'Esportivo' },
      { id: 4, name: 'Auditório', type: 'Eventos' },
      { id: 5, name: 'Biblioteca', type: 'Educacional' }
    ]);
    
    const loading = ref(true);
    const showModal = ref(false);
    const showCalendar = ref(true);
    const selectedAllocation = ref<ResourceAllocation | null>(null);
    const dragAllocation = ref<ResourceAllocation | null>(null);
    const searchQuery = ref('');
    const selectedResourceType = ref('');
    const selectedStatus = ref('');
    const currentDate = ref(new Date());

    const resourceTypes = ref(['Alimentação', 'Educacional', 'Esportivo', 'Eventos', 'Outros']);
    const statusOptions = ref(['Liberado', 'Alocado', 'Manutenção', 'Bloqueado']);

    const weekDays = computed(() => {
      const days = [];
      const startDate = new Date(currentDate.value);
      startDate.setDate(startDate.getDate() - startDate.getDay() + 1);
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        days.push(date.toLocaleDateString('pt-BR', { weekday: 'short', day: 'numeric' }));
      }
      return days;
    });

    const currentWeekRange = computed(() => {
      const startDate = new Date(currentDate.value);
      startDate.setDate(startDate.getDate() - startDate.getDay() + 1);
      const endDate = new Date(startDate);
      endDate.setDate(endDate.getDate() + 6);
      
      return `${startDate.toLocaleDateString('pt-BR')} - ${endDate.toLocaleDateString('pt-BR')}`;
    });

    const timeSlots = ref([
      { id: 1, time: '07:00 - 08:00' },
      { id: 2, time: '08:00 - 09:00' },
      { id: 3, time: '09:00 - 10:00' },
      { id: 4, time: '10:00 - 11:00' },
      { id: 5, time: '11:00 - 12:00' },
      { id: 6, time: '12:00 - 13:00' },
      { id: 7, time: '13:00 - 14:00' },
      { id: 8, time: '14:00 - 15:00' },
      { id: 9, time: '15:00 - 16:00' },
      { id: 10, time: '16:00 - 17:00' }
    ]);

    const filteredResources = computed(() => {
      return resources.value.filter(r => {
        const matchesSearch = r.resource.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                             r.class.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                             r.teacher.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesType = selectedResourceType.value ? r.type === selectedResourceType.value : true;
        const matchesStatus = selectedStatus.value ? r.status === selectedStatus.value : true;
        return matchesSearch && matchesType && matchesStatus;
      });
    });

    const loadResources = async () => {
      try {
        loading.value = true;
        resources.value = await fetchResources();
      } catch (error) {
        console.error('Erro ao carregar alocações:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(loadResources);

    const showAllocationModal = () => {
      selectedAllocation.value = null;
      showModal.value = true;
    };

    const editAllocation = (allocation: ResourceAllocation) => {
      selectedAllocation.value = { ...allocation };
      showModal.value = true;
    };

    const handleSaveAllocation = async (allocationData: ResourceAllocation) => {
      if (selectedAllocation.value?.id) {
        await updateAllocation(selectedAllocation.value.id, allocationData);
      } else {
        await createAllocation(allocationData);
      }
      await loadResources();
      showModal.value = false;
    };

    const deleteAllocation = async (allocation: ResourceAllocation) => {
      if (confirm(`Tem certeza que deseja excluir a alocação de ${allocation.resource}?`)) {
        await deleteAllocation(allocation.id);
        await loadResources();
      }
    };

    const toggleStatus = async (allocation: ResourceAllocation) => {
      const newStatus = allocation.status === 'Liberado' ? 'Bloqueado' : 'Liberado';
      await updateAllocation(allocation.id, { ...allocation, status: newStatus });
      await loadResources();
    };

    const prevWeek = () => {
      const date = new Date(currentDate.value);
      date.setDate(date.getDate() - 7);
      currentDate.value = date;
    };

    const nextWeek = () => {
      const date = new Date(currentDate.value);
      date.setDate(date.getDate() + 7);
      currentDate.value = date;
    };

    const handleDragStart = (event: DragEvent, allocation: ResourceAllocation) => {
      dragAllocation.value = allocation;
      event.dataTransfer?.setData('text/plain', allocation.id.toString());
    };

    const handleResourceDrop = (event: DragEvent, day: string, timeSlot: any) => {
      if (dragAllocation.value) {
        console.log(`Movendo ${dragAllocation.value.resource} para ${day} - ${timeSlot.time}`);
      }
    };

    const getAllocationsForSlot = (day: string, timeSlot: any) => {
      return resources.value.filter(a => 
        a.day === day.split(' ')[0] && 
        a.time === timeSlot.time
      ).slice(0, 2);
    };

    const allocationClass = (allocation: ResourceAllocation) => {
      const statusClass = {
        'Liberado': 'status-liberado',
        'Alocado': 'status-alocado',
        'Manutenção': 'status-manutencao',
        'Bloqueado': 'status-bloqueado'
      };
      return statusClass[allocation.status] || '';
    };

    const statusBadgeClass = (status: string) => {
      return status.toLowerCase().replace('ç', 'c').replace('ã', 'a');
    };

    const resourceIcon = (type: string) => {
      const icons = {
        'Alimentação': 'fas fa-utensils',
        'Educacional': 'fas fa-book',
        'Esportivo': 'fas fa-running',
        'Eventos': 'fas fa-calendar-alt'
      };
      return icons[type] || 'fas fa-box';
    };

    const getIconBg = (type: string) => {
      const colors = {
        'Alimentação': 'bg-food',
        'Educacional': 'bg-education',
        'Esportivo': 'bg-sports',
        'Eventos': 'bg-events'
      };
      return colors[type] || 'bg-default';
    };

    return { 
      resources,
      resourcesList,
      loading,
      showModal,
      showCalendar,
      selectedAllocation,
      searchQuery,
      selectedResourceType,
      selectedStatus,
      resourceTypes,
      statusOptions,
      filteredResources,
      weekDays,
      currentWeekRange,
      timeSlots,
      currentDate,
      showAllocationModal,
      editAllocation,
      deleteAllocation,
      toggleStatus,
      handleSaveAllocation,
      prevWeek,
      nextWeek,
      handleDragStart,
      handleResourceDrop,
      getAllocationsForSlot,
      allocationClass,
      statusBadgeClass,
      resourceIcon,
      getIconBg
    };
  },
});
</script>

<style scoped>
.resource-allocator {
  min-height: 100vh;
  background: #ffffff;
  padding: 2rem;
}

/* Header Section */
.header-section {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.2);
}

.main-title {
  font-size: 32px;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
}

.subtitle {
  font-size: 14px;
  color: rgba(31, 29, 32, 0.6);
  margin: 4px 0 0 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.btn-secondary, .btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #e1d4c2;
  color: #1f1d20;
}

.btn-secondary:hover {
  background: rgba(225, 212, 194, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(225, 212, 194, 0.4);
}

.btn-primary {
  background: #2d531a;
  color: #ffffff;
}

.btn-primary:hover {
  background: rgba(45, 83, 26, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

/* Calendar Section */
.calendar-section {
  margin-bottom: 2rem;
}

.calendar-card {
  background: #ffffff;
  border: 2px solid #e1d4c2;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(31, 29, 32, 0.08);
}

.calendar-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.navigation-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-btn {
  width: 44px;
  height: 44px;
  background: #e1d4c2;
  border: none;
  border-radius: 12px;
  color: #1f1d20;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.nav-btn:hover {
  background: rgba(225, 212, 194, 0.7);
  transform: scale(1.05);
}

.week-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: rgba(225, 212, 194, 0.2);
  border-radius: 12px;
}

.week-info i {
  color: #2d531a;
  font-size: 18px;
}

.week-range {
  font-size: 16px;
  font-weight: 700;
  color: #1f1d20;
  margin: 0;
}

.today-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.today-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.select-filter {
  padding: 10px 16px;
  background: rgba(225, 212, 194, 0.2);
  border: 2px solid #e1d4c2;
  border-radius: 10px;
  color: #1f1d20;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  transition: all 0.3s ease;
  min-width: 180px;
}

.select-filter:hover,
.select-filter:focus {
  border-color: #2d531a;
  background: rgba(225, 212, 194, 0.3);
}

.icon-btn {
  width: 44px;
  height: 44px;
  background: #e1d4c2;
  border: none;
  border-radius: 10px;
  color: #1f1d20;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: rgba(225, 212, 194, 0.7);
  transform: scale(1.05);
}

/* Calendar Grid */
.calendar-grid-wrapper {
  overflow-x: auto;
}

.calendar-header {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.time-column-header {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  color: rgba(31, 29, 32, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.days-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.day-header {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
  padding: 16px 12px;
  border-radius: 12px;
  text-align: center;
  font-weight: 700;
  font-size: 14px;
  text-transform: capitalize;
  box-shadow: 0 2px 8px rgba(45, 83, 26, 0.2);
}

.day-label {
  display: block;
}

.calendar-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.time-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px;
}

.time-column {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(31, 29, 32, 0.6);
  font-size: 13px;
  font-weight: 600;
  background: rgba(225, 212, 194, 0.15);
  border-radius: 10px;
  padding: 8px;
}

.time-column i {
  font-size: 12px;
  color: #2d531a;
}

.slots-container {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.resource-slot {
  min-height: 100px;
  background: rgba(225, 212, 194, 0.1);
  border: 2px dashed rgba(225, 212, 194, 0.4);
  border-radius: 12px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: all 0.3s ease;
  position: relative;
}

.resource-slot:hover {
  background: rgba(225, 212, 194, 0.2);
  border-color: #2d531a;
  border-style: solid;
}

.empty-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 80px;
  color: rgba(31, 29, 32, 0.2);
  font-size: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.resource-slot:hover .empty-slot {
  opacity: 1;
}

.allocation-card {
  background: #ffffff;
  border-left: 4px solid;
  border-radius: 10px;
  padding: 10px;
  cursor: move;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(31, 29, 32, 0.08);
}

.allocation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(31, 29, 32, 0.15);
}

.allocation-card.status-liberado {
  border-left-color: #2d531a;
  background: rgba(45, 83, 26, 0.05);
}

.allocation-card.status-alocado {
  border-left-color: #e1d4c2;
  background: rgba(225, 212, 194, 0.15);
}

.allocation-card.status-manutencao {
  border-left-color: #0f1e3f;
  background: rgba(15, 30, 63, 0.05);
}

.allocation-card.status-bloqueado {
  border-left-color: #1f1d20;
  background: rgba(31, 29, 32, 0.05);
}

.allocation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.resource-icon-small {
  width: 24px;
  height: 24px;
  background: #2d531a;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 10px;
  flex-shrink: 0;
}

.resource-name {
  flex: 1;
  font-weight: 700;
  font-size: 12px;
  color: #1f1d20;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.drag-icon {
  color: rgba(31, 29, 32, 0.3);
  font-size: 10px;
  flex-shrink: 0;
}

.allocation-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.class-tag {
  font-size: 11px;
  font-weight: 600;
  color: rgba(31, 29, 32, 0.8);
  background: rgba(31, 29, 32, 0.08);
  padding: 4px 8px;
  border-radius: 6px;
  width: fit-content;
}

.teacher-name {
  font-size: 10px;
  color: rgba(31, 29, 32, 0.6);
}

/* List Section */
.list-section {
  margin-bottom: 2rem;
}

.list-card {
  background: #ffffff;
  border: 2px solid #e1d4c2;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(31, 29, 32, 0.08);
}

.filters-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-wrapper {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-wrapper i {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(31, 29, 32, 0.4);
  font-size: 16px;
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 48px;
  background: rgba(225, 212, 194, 0.15);
  border: 2px solid #e1d4c2;
  border-radius: 12px;
  font-size: 14px;
  color: #1f1d20;
  font-weight: 500;
  outline: none;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(31, 29, 32, 0.4);
}

.search-input:focus {
  border-color: #2d531a;
  background: rgba(225, 212, 194, 0.25);
  box-shadow: 0 0 0 4px rgba(45, 83, 26, 0.1);
}

.filters-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #e1d4c2;
  border: none;
  border-radius: 10px;
  color: #1f1d20;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(225, 212, 194, 0.8);
  transform: translateY(-2px);
}

/* Resources Table */
.table-wrapper {
  overflow-x: auto;
}

.resources-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.resources-table thead tr {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
}

.resources-table th {
  padding: 16px 20px;
  text-align: left;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.resources-table th:first-child {
  border-top-left-radius: 12px;
}

.resources-table th:last-child {
  border-top-right-radius: 12px;
}

.resources-table tbody .table-row {
  background: #ffffff;
  transition: all 0.3s ease;
}

.resources-table tbody .table-row:nth-child(even) {
  background: rgba(225, 212, 194, 0.08);
}

.resources-table tbody .table-row:hover {
  background: rgba(225, 212, 194, 0.2);
  transform: scale(1.005);
  box-shadow: 0 4px 12px rgba(31, 29, 32, 0.08);
}

.resources-table td {
  padding: 18px 20px;
  font-size: 14px;
  color: #1f1d20;
  border-bottom: 1px solid rgba(225, 212, 194, 0.3);
}

.resource-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.resource-icon-container {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 18px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(31, 29, 32, 0.1);
}

.resource-icon-container.bg-food {
  background: linear-gradient(135deg, #2d531a, #1f4513);
}

.resource-icon-container.bg-education {
  background: linear-gradient(135deg, #0f1e3f, #081528);
}

.resource-icon-container.bg-sports {
  background: linear-gradient(135deg, #e1d4c2, #c9baa8);
  color: #1f1d20;
}

.resource-icon-container.bg-events {
  background: linear-gradient(135deg, #1f1d20, #0f0e10);
}

.resource-icon-container.bg-default {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
}

.resource-title {
  font-weight: 700;
  font-size: 14px;
  color: #1f1d20;
}

.type-badge {
  display: inline-block;
  padding: 6px 14px;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #1f1d20;
  white-space: nowrap;
}

.class-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(31, 29, 32, 0.7);
  font-weight: 500;
}

.class-info i {
  color: #2d531a;
  font-size: 12px;
}

.time-cell {
  color: rgba(31, 29, 32, 0.6);
  font-weight: 500;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  border: 2px solid;
  white-space: nowrap;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-pill.liberado {
  background: rgba(45, 83, 26, 0.1);
  color: #2d531a;
  border-color: #2d531a;
}

.status-pill.alocado {
  background: rgba(225, 212, 194, 0.3);
  color: #1f1d20;
  border-color: #e1d4c2;
}

.status-pill.manutencao {
  background: rgba(15, 30, 63, 0.1);
  color: #0f1e3f;
  border-color: #0f1e3f;
}

.status-pill.bloqueado {
  background: rgba(31, 29, 32, 0.1);
  color: #1f1d20;
  border-color: #1f1d20;
}

.actions-cell {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-btn {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.action-btn.edit-btn {
  background: rgba(225, 212, 194, 0.3);
  color: #1f1d20;
}

.action-btn.edit-btn:hover {
  background: #e1d4c2;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(225, 212, 194, 0.4);
}

.action-btn.delete-btn {
  background: rgba(31, 29, 32, 0.08);
  color: #1f1d20;
}

.action-btn.delete-btn:hover {
  background: #1f1d20;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(31, 29, 32, 0.3);
}

.action-btn.toggle-btn {
  background: rgba(45, 83, 26, 0.1);
  color: #2d531a;
}

.action-btn.toggle-btn:hover {
  background: #2d531a;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(45, 83, 26, 0.3);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(31, 29, 32, 0.4);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: rgba(225, 212, 194, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: rgba(31, 29, 32, 0.3);
}

.empty-state h4 {
  font-size: 18px;
  font-weight: 700;
  color: rgba(31, 29, 32, 0.6);
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

.text-center {
  text-align: center;
}

/* Responsive */
@media (max-width: 1400px) {
  .calendar-header,
  .time-row {
    grid-template-columns: 120px 1fr;
  }
}

@media (max-width: 1200px) {
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-wrapper {
    min-width: 100%;
  }
  
  .filters-group {
    width: 100%;
  }
  
  .select-filter {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .resource-allocator {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .title-group {
    flex-direction: column;
    text-align: center;
  }
  
  .main-title {
    font-size: 24px;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .btn-primary,
  .btn-secondary {
    flex: 1;
    justify-content: center;
  }
  
  .calendar-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .navigation-group {
    justify-content: center;
  }
  
  .filter-controls {
    width: 100%;
  }
  
  .select-filter {
    flex: 1;
  }
  
  .days-row,
  .slots-container {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .resources-table {
    font-size: 12px;
  }
  
  .resources-table th,
  .resources-table td {
    padding: 12px;
  }
  
  .resource-icon-container {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }
}
</style>