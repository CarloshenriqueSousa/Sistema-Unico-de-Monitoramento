<template>
  <div class="schedule-manager">
    <!-- Header Section -->
    <div class="header-section">
      <div class="header-content">
        <div class="title-group">
          <div class="icon-wrapper">
            <i class="fas fa-calendar-alt"></i>
          </div>
          <div>
            <h2 class="main-title">Gerenciador de Horários</h2>
            <p class="subtitle">Organize e gerencie os horários das turmas</p>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="showReleaseModal = true" class="btn-secondary">
            <i class="fas fa-unlock"></i>
            <span>Liberar Turmas</span>
          </button>
          <button @click="addSchedule" class="btn-primary">
            <i class="fas fa-plus"></i>
            <span>Adicionar Horário</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Weekly Schedule Visualization -->
    <div class="schedule-card">
      <div class="card-header">
        <h3 class="card-title">Visualização Semanal</h3>
        <div class="view-controls">
          <button class="icon-btn">
            <i class="fas fa-filter"></i>
          </button>
          <button class="icon-btn">
            <i class="fas fa-download"></i>
          </button>
        </div>
      </div>

      <div class="schedule-grid-container">
        <!-- Days Header -->
        <div class="days-header">
          <div 
            v-for="day in weekDays" 
            :key="day" 
            class="day-cell"
          >
            <span class="day-name">{{ day }}</span>
          </div>
        </div>

        <!-- Time Slots Grid -->
        <div class="time-grid">
          <div 
            v-for="(timeSlot, index) in timeSlots" 
            :key="index"
            class="time-row"
          >
            <div class="time-label">
              <i class="fas fa-clock"></i>
              <span>{{ timeSlot.time }}</span>
            </div>
            
            <div class="slots-row">
              <div
                v-for="(day, dayIndex) in weekDays"
                :key="dayIndex"
                class="schedule-slot"
                @dragover.prevent
                @drop="handleScheduleDrop($event, timeSlot)"
              >
                <div
                  v-for="schedule in getSchedulesForSlot(timeSlot)"
                  :key="schedule.id"
                  draggable="true"
                  @dragstart="handleDragStart($event, schedule)"
                  :class="['schedule-item', scheduleClass(schedule)]"
                >
                  <div class="schedule-header">
                    <span class="class-name">{{ schedule.class }}</span>
                    <i class="fas fa-grip-vertical drag-handle"></i>
                  </div>
                  <div class="schedule-teacher">{{ schedule.teacher }}</div>
                  <div class="schedule-footer">
                    <span class="duration-badge">
                      <i class="fas fa-clock"></i>
                      {{ schedule.duration }}min
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="content-grid">
      <!-- Schedules Table -->
      <div class="schedules-section">
        <div class="section-header">
          <h3 class="section-title">Horários Programados</h3>
          <div class="filter-group">
            <div class="search-box">
              <i class="fas fa-search"></i>
              <input type="text" placeholder="Buscar horário...">
            </div>
          </div>
        </div>

        <div class="table-card">
          <table class="modern-table">
            <thead>
              <tr>
                <th>Turma</th>
                <th>Horário</th>
                <th>Professor</th>
                <th>Duração</th>
                <th>Status</th>
                <th class="text-center">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="schedule in schedules" :key="schedule.id">
                <td>
                  <div class="class-cell">
                    <div class="class-icon">
                      <i class="fas fa-graduation-cap"></i>
                    </div>
                    <span class="font-medium">{{ schedule.class }}</span>
                  </div>
                </td>
                <td class="text-muted">{{ schedule.time }}</td>
                <td class="text-muted">{{ schedule.teacher }}</td>
                <td>
                  <span class="duration-pill">{{ schedule.duration }} min</span>
                </td>
                <td>
                  <span :class="['status-badge', `status-${schedule.status.toLowerCase()}`]">
                    {{ schedule.status }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons-group">
                    <button @click="editSchedule(schedule)" class="action-btn edit">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button @click="deleteSchedule(schedule)" class="action-btn delete">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                    <button @click="toggleScheduleStatus(schedule)" class="action-btn toggle">
                      <i :class="schedule.status === 'Liberado' ? 'fas fa-lock' : 'fas fa-unlock'"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pending Requests Sidebar -->
      <div class="requests-sidebar">
        <div class="sidebar-header">
          <div class="sidebar-title">
            <i class="fas fa-bell"></i>
            <h4>Liberações Pendentes</h4>
          </div>
          <span class="badge-count">{{ releaseRequests.length }}</span>
        </div>

        <div class="requests-list">
          <div 
            v-for="request in releaseRequests" 
            :key="request.id"
            class="request-card"
          >
            <div class="request-info">
              <div class="request-header">
                <span class="request-class">{{ request.class }}</span>
                <span class="request-time">{{ request.time }}</span>
              </div>
              <div class="request-teacher">{{ request.teacher }}</div>
              <div class="request-date">
                <i class="fas fa-calendar"></i>
                {{ request.date }}
              </div>
            </div>
            <div class="request-actions">
              <button @click="approveRequest(request)" class="approve-btn">
                <i class="fas fa-check"></i>
              </button>
              <button @click="rejectRequest(request)" class="reject-btn">
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>

          <div v-if="releaseRequests.length === 0" class="empty-state">
            <i class="fas fa-check-circle"></i>
            <p>Nenhuma solicitação pendente</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <ScheduleModal 
      v-if="showScheduleModal"
      :schedule="selectedSchedule"
      @close="showScheduleModal = false"
      @save="handleSaveSchedule"
    />

    <ReleaseModal 
      v-if="showReleaseModal"
      @close="showReleaseModal = false"
      @release="handleReleaseSchedules"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import DynamicTable from '@/shared/DynamicTable.vue';
import Button from '@/shared/Button.vue';
import ScheduleModal from '@/management/ScheduleModal.vue';
import ReleaseModal from '@/management/ReleaseModal.vue';
import { fetchSchedules, createSchedule, updateSchedule, deleteSchedule, toggleScheduleStatus } from '@/services/scheduleService';
import type { Schedule } from '@/types';

export default defineComponent({
  name: 'ScheduleManager',
  components: { ScheduleModal, ReleaseModal },
  setup() {
    const schedules = ref<Schedule[]>([
      { id: 1, class: '9º A', time: '08:00 - 09:00', teacher: 'Prof. Silva', duration: 60, status: 'Liberado' },
      { id: 2, class: '8º B', time: '09:00 - 10:00', teacher: 'Prof. Costa', duration: 60, status: 'Pendente' },
      { id: 3, class: '7º C', time: '10:00 - 11:00', teacher: 'Prof. Santos', duration: 60, status: 'Bloqueado' }
    ]);
    
    const loading = ref(true);
    const showScheduleModal = ref(false);
    const showReleaseModal = ref(false);
    const selectedSchedule = ref<Schedule | null>(null);
    const dragSchedule = ref<Schedule | null>(null);
    
    const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
    
    const timeSlots = ref([
      { id: 1, time: '07:00 - 08:00' },
      { id: 2, time: '08:00 - 09:00' },
      { id: 3, time: '09:00 - 10:00' },
      { id: 4, time: '10:00 - 11:00' },
      { id: 5, time: '11:00 - 12:00' },
      { id: 6, time: '12:00 - 13:00' },
      { id: 7, time: '13:00 - 14:00' },
      { id: 8, time: '14:00 - 15:00' }
    ]);

    const releaseRequests = ref([
      { id: 1, class: '9º A', time: '11:00 - 12:00', teacher: 'Prof. Silva', date: '25/10/2025' },
      { id: 2, class: '8º B', time: '14:00 - 15:00', teacher: 'Prof. Oliveira', date: '26/10/2025' }
    ]);

    const loadSchedules = async () => {
      try {
        loading.value = true;
        schedules.value = await fetchSchedules();
      } catch (error) {
        console.error('Erro ao carregar horários:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(loadSchedules);

    const addSchedule = () => {
      selectedSchedule.value = null;
      showScheduleModal.value = true;
    };

    const editSchedule = (schedule: Schedule) => {
      selectedSchedule.value = { ...schedule };
      showScheduleModal.value = true;
    };

    const handleSaveSchedule = async (scheduleData: Schedule) => {
      if (selectedSchedule.value?.id) {
        await updateSchedule(selectedSchedule.value.id, scheduleData);
      } else {
        await createSchedule(scheduleData);
      }
      await loadSchedules();
      showScheduleModal.value = false;
    };

    const handleReleaseSchedules = (classes: string[]) => {
      console.log('Liberar turmas:', classes);
      showReleaseModal.value = false;
    };

    const handleDragStart = (event: DragEvent, schedule: Schedule) => {
      dragSchedule.value = schedule;
      event.dataTransfer?.setData('text/plain', schedule.id.toString());
    };

    const handleScheduleDrop = (event: DragEvent, timeSlot: any) => {
      if (dragSchedule.value) {
        console.log(`Movendo ${dragSchedule.value.class} para ${timeSlot.time}`);
      }
    };

    const getSchedulesForSlot = (timeSlot: any) => {
      return schedules.value.filter(s => s.time === timeSlot.time).slice(0, 2);
    };

    const scheduleClass = (schedule: Schedule) => {
      const statusClass = {
        'Liberado': 'status-liberado',
        'Pendente': 'status-pendente',
        'Bloqueado': 'status-bloqueado'
      };
      return statusClass[schedule.status] || '';
    };

    const approveRequest = (request: any) => {
      releaseRequests.value = releaseRequests.value.filter(r => r.id !== request.id);
    };

    const rejectRequest = (request: any) => {
      releaseRequests.value = releaseRequests.value.filter(r => r.id !== request.id);
    };

    return { 
      schedules, 
      loading,
      showScheduleModal,
      showReleaseModal,
      selectedSchedule,
      releaseRequests,
      weekDays,
      timeSlots,
      addSchedule, 
      editSchedule,
      deleteSchedule,
      toggleScheduleStatus,
      handleSaveSchedule,
      handleReleaseSchedules,
      handleDragStart,
      handleScheduleDrop,
      getSchedulesForSlot,
      scheduleClass,
      approveRequest,
      rejectRequest
    };
  },
});
</script>

<style scoped>
.schedule-manager {
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

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #e1d4c2;
  color: #1f1d20;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(225, 212, 194, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(225, 212, 194, 0.4);
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #2d531a;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: rgba(45, 83, 26, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

/* Schedule Card */
.schedule-card {
  background: #ffffff;
  border: 2px solid #e1d4c2;
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(31, 29, 32, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f1d20;
  margin: 0;
}

.view-controls {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 40px;
  height: 40px;
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

/* Schedule Grid */
.schedule-grid-container {
  overflow-x: auto;
}

.days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.day-cell {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  font-weight: 700;
  font-size: 14px;
}

.time-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.time-row {
  display: flex;
  gap: 12px;
}

.time-label {
  min-width: 120px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(31, 29, 32, 0.6);
  font-size: 13px;
  font-weight: 600;
}

.slots-row {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.schedule-slot {
  min-height: 100px;
  background: rgba(225, 212, 194, 0.15);
  border: 2px dashed rgba(225, 212, 194, 0.4);
  border-radius: 12px;
  padding: 8px;
  transition: all 0.3s ease;
}

.schedule-slot:hover {
  background: rgba(225, 212, 194, 0.25);
  border-color: #2d531a;
}

.schedule-item {
  background: #ffffff;
  border-left: 4px solid;
  border-radius: 10px;
  padding: 12px;
  cursor: move;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(31, 29, 32, 0.1);
}

.schedule-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(31, 29, 32, 0.15);
}

.schedule-item.status-liberado {
  border-left-color: #2d531a;
  background: rgba(45, 83, 26, 0.05);
}

.schedule-item.status-pendente {
  border-left-color: #e1d4c2;
  background: rgba(225, 212, 194, 0.15);
}

.schedule-item.status-bloqueado {
  border-left-color: #1f1d20;
  background: rgba(31, 29, 32, 0.05);
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.class-name {
  font-weight: 700;
  font-size: 13px;
  color: #1f1d20;
}

.drag-handle {
  color: rgba(31, 29, 32, 0.3);
  font-size: 12px;
}

.schedule-teacher {
  font-size: 11px;
  color: rgba(31, 29, 32, 0.7);
  margin-bottom: 8px;
}

.schedule-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.duration-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(31, 29, 32, 0.08);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  color: #1f1d20;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 24px;
}

/* Schedules Section */
.schedules-section {
  background: #ffffff;
  border: 2px solid #e1d4c2;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(31, 29, 32, 0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f1d20;
  margin: 0;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 12px;
  color: rgba(31, 29, 32, 0.4);
}

.search-box input {
  padding: 10px 12px 10px 36px;
  background: rgba(225, 212, 194, 0.2);
  border: 2px solid #e1d4c2;
  border-radius: 10px;
  font-size: 14px;
  color: #1f1d20;
  outline: none;
  transition: all 0.3s ease;
  width: 220px;
}

.search-box input:focus {
  border-color: #2d531a;
  background: rgba(225, 212, 194, 0.3);
}

/* Modern Table */
.table-card {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.modern-table thead tr {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
}

.modern-table th {
  padding: 16px;
  text-align: left;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-table th:first-child {
  border-top-left-radius: 12px;
}

.modern-table th:last-child {
  border-top-right-radius: 12px;
}

.modern-table tbody tr {
  background: #ffffff;
  transition: all 0.3s ease;
}

.modern-table tbody tr:nth-child(even) {
  background: rgba(225, 212, 194, 0.1);
}

.modern-table tbody tr:hover {
  background: rgba(225, 212, 194, 0.2);
  transform: scale(1.01);
  box-shadow: 0 2px 8px rgba(31, 29, 32, 0.08);
}

.modern-table td {
  padding: 16px;
  font-size: 14px;
  color: #1f1d20;
  border-bottom: 1px solid rgba(225, 212, 194, 0.3);
}

.class-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.class-icon {
  width: 36px;
  height: 36px;
  background: #2d531a;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.duration-pill {
  display: inline-block;
  padding: 6px 12px;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #1f1d20;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  border: 2px solid;
}

.status-badge.status-liberado {
  background: rgba(45, 83, 26, 0.15);
  color: #2d531a;
  border-color: #2d531a;
}

.status-badge.status-pendente {
  background: rgba(225, 212, 194, 0.3);
  color: #1f1d20;
  border-color: #e1d4c2;
}

.status-badge.status-bloqueado {
  background: rgba(15, 30, 63, 0.15);
  color: #0f1e3f;
  border-color: #0f1e3f;
}

.action-buttons-group {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn.edit {
  background: rgba(225, 212, 194, 0.3);
  color: #1f1d20;
}

.action-btn.edit:hover {
  background: #e1d4c2;
}

.action-btn.delete {
  background: rgba(31, 29, 32, 0.1);
  color: #1f1d20;
}

.action-btn.delete:hover {
  background: #1f1d20;
  color: #ffffff;
}

.action-btn.toggle {
  background: rgba(45, 83, 26, 0.1);
  color: #2d531a;
}

.action-btn.toggle:hover {
  background: #2d531a;
  color: #ffffff;
}

/* Requests Sidebar */
.requests-sidebar {
  background: #ffffff;
  border: 2px solid #e1d4c2;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(31, 29, 32, 0.08);
  height: fit-content;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-title i {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #ffffff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-title h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1f1d20;
  margin: 0;
}

.badge-count {
  background: #2d531a;
  color: #ffffff;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.request-card {
  background: rgba(225, 212, 194, 0.15);
  border: 2px solid #e1d4c2;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.request-card:hover {
  background: rgba(225, 212, 194, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(31, 29, 32, 0.1);
}

.request-info {
  flex: 1;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.request-class {
  font-weight: 700;
  font-size: 14px;
  color: #1f1d20;
}

.request-time {
  font-size: 12px;
  color: rgba(31, 29, 32, 0.6);
  background: rgba(45, 83, 26, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
}

.request-teacher {
  font-size: 13px;
  color: rgba(31, 29, 32, 0.7);
  margin-bottom: 8px;
}

.request-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: rgba(31, 29, 32, 0.5);
}

.request-date i {
  font-size: 10px;
}

.request-actions {
  display: flex;
  gap: 8px;
}

.approve-btn, .reject-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.approve-btn {
  background: rgba(45, 83, 26, 0.15);
  color: #2d531a;
}

.approve-btn:hover {
  background: #2d531a;
  color: #ffffff;
  transform: scale(1.1);
}

.reject-btn {
  background: rgba(31, 29, 32, 0.1);
  color: #1f1d20;
}

.reject-btn:hover {
  background: #1f1d20;
  color: #ffffff;
  transform: scale(1.1);
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: rgba(31, 29, 32, 0.4);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 12px;
  color: #2d531a;
  opacity: 0.3;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

.text-center {
  text-align: center;
}

.text-muted {
  color: rgba(31, 29, 32, 0.6);
}

.font-medium {
  font-weight: 600;
}

/* Responsive */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .requests-sidebar {
    order: -1;
  }
}

@media (max-width: 768px) {
  .schedule-manager {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .btn-primary, .btn-secondary {
    flex: 1;
  }
  
  .days-header {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .slots-row {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>