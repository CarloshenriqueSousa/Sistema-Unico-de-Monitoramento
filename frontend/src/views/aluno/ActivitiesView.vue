<template>
  <div class="activities-root">
    <div class="container">
      <div class="header">
        <div>
          <h1 class="title">Atividades</h1>
          <p class="subtitle">Gerencie suas tarefas e exercícios</p>
        </div>
        <div class="header-actions">
          <select v-model="filter" class="filter-select">
            <option value="all">Todas</option>
            <option value="pending">Pendentes</option>
            <option value="completed">Concluídas</option>
            <option value="late">Atrasadas</option>
          </select>
        </div>
      </div>

      <div class="filter-chips">
        <button 
          v-for="status in filterOptions" 
          :key="status.value"
          :class="['filter-chip', { active: filter === status.value }]"
          @click="filter = status.value">
          <i :class="status.icon"></i>
          <span>{{ status.label }}</span>
          <span v-if="getCount(status.value)" class="chip-count">{{ getCount(status.value) }}</span>
        </button>
      </div>

      <div v-if="filteredActivities.length" class="activities-grid">
        <div 
          v-for="activity in filteredActivities" 
          :key="activity.id"
          class="activity-card"
          @click="selectActivity(activity)">
          <div class="card-header">
            <div class="subject-badge" :class="getSubjectClass(activity.subject)">
              {{ activity.subject }}
            </div>
            <div class="status-badge" :class="activity.status">
              <i :class="getStatusIcon(activity.status)"></i>
              <span>{{ getStatusLabel(activity.status) }}</span>
            </div>
          </div>
          
          <h3 class="activity-title">{{ activity.title }}</h3>
          <p class="activity-description">{{ activity.description }}</p>
          
          <div class="card-footer">
            <div class="deadline-info">
              <i class="fas fa-calendar-alt"></i>
              <span>{{ formatDate(activity.dueDate) }}</span>
            </div>
            <button class="action-btn">
              <span>Ver Detalhes</span>
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">
          <i class="fas fa-inbox"></i>
        </div>
        <h3 class="empty-title">Nenhuma atividade encontrada</h3>
        <p class="empty-text">Não há atividades correspondentes ao filtro selecionado</p>
      </div>

      <ActivityModal 
        v-if="selectedActivity"
        :activity="selectedActivity"
        @close="selectedActivity = null"
        @complete="markCompleted(selectedActivity)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import ActivityModal from '@/components/activities/ActivityModal.vue';

interface Activity {
  id: number;
  title: string;
  subject: string;
  dueDate: string;
  status: 'pending' | 'completed' | 'late';
  description: string;
  content: string;
}

export default defineComponent({
  name: 'ActivitiesView',
  components: { ActivityModal },
  setup() {
    const filter = ref<'all' | 'pending' | 'completed' | 'late'>('all');
    const selectedActivity = ref<Activity | null>(null);

    const filterOptions = [
      { value: 'all', label: 'Todas', icon: 'fas fa-list' },
      { value: 'pending', label: 'Pendentes', icon: 'fas fa-clock' },
      { value: 'completed', label: 'Concluídas', icon: 'fas fa-check-circle' },
      { value: 'late', label: 'Atrasadas', icon: 'fas fa-exclamation-triangle' }
    ];

    const activities = ref<Activity[]>([
      {
        id: 1,
        title: 'Exercícios de Álgebra Linear',
        subject: 'Matemática',
        dueDate: '2025-11-15',
        status: 'pending',
        description: 'Resolva a lista de exercícios sobre matrizes e determinantes',
        content: '<p>Conteúdo detalhado da atividade...</p>'
      },
      {
        id: 2,
        title: 'Análise de Poema Modernista',
        subject: 'Literatura',
        dueDate: '2025-11-10',
        status: 'completed',
        description: 'Análise do poema "No Meio do Caminho" de Carlos Drummond de Andrade',
        content: '<p>Conteúdo detalhado da atividade...</p>'
      },
      {
        id: 3,
        title: 'Relatório de Experimento',
        subject: 'Ciências',
        dueDate: '2025-10-25',
        status: 'late',
        description: 'Relatório completo sobre o experimento de termodinâmica',
        content: '<p>Conteúdo detalhado da atividade...</p>'
      },
      {
        id: 4,
        title: 'Redação: Meio Ambiente',
        subject: 'Português',
        dueDate: '2025-11-20',
        status: 'pending',
        description: 'Escreva uma redação dissertativa sobre sustentabilidade',
        content: '<p>Conteúdo detalhado da atividade...</p>'
      }
    ]);

    const filteredActivities = computed(() => {
      if (filter.value === 'all') return activities.value;
      return activities.value.filter(a => a.status === filter.value);
    });

    const getCount = (status: string) => {
      if (status === 'all') return activities.value.length;
      return activities.value.filter(a => a.status === status).length;
    };

    const selectActivity = (activity: Activity) => {
      selectedActivity.value = activity;
    };

    const markCompleted = (activity: Activity | null) => {
      if (!activity) return;
      const idx = activities.value.findIndex(a => a.id === activity.id);
      if (idx !== -1) activities.value[idx].status = 'completed';
      selectedActivity.value = null;
    };

    const getStatusIcon = (status: string) => {
      const icons: Record<string, string> = {
        pending: 'fas fa-clock',
        completed: 'fas fa-check-circle',
        late: 'fas fa-exclamation-circle'
      };
      return icons[status] || 'fas fa-circle';
    };

    const getStatusLabel = (status: string) => {
      const labels: Record<string, string> = {
        pending: 'Pendente',
        completed: 'Concluída',
        late: 'Atrasada'
      };
      return labels[status] || status;
    };

    const getSubjectClass = (subject: string) => {
      const classes: Record<string, string> = {
        'Matemática': 'math',
        'Literatura': 'literature',
        'Ciências': 'science',
        'Português': 'portuguese'
      };
      return classes[subject] || 'default';
    };

    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat('pt-BR', { 
        day: '2-digit', 
        month: 'short' 
      }).format(date);
    };

    return { 
      filter,
      filterOptions,
      activities, 
      filteredActivities,
      selectedActivity,
      getCount,
      selectActivity,
      markCompleted,
      getStatusIcon,
      getStatusLabel,
      getSubjectClass,
      formatDate
    };
  },
});
</script>

<style scoped>
.activities-root {
  min-height: 100vh;
  background: #17181e;
  color: #fcfcfc;
  padding: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fcfcfc;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1rem;
  color: #8b92a8;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fcfcfc;
  font-size: 0.9375rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 150px;
}

.filter-select:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.3);
}

.filter-chips {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  color: #8b92a8;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-chip:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fcfcfc;
}

.filter-chip.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
  border-color: rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.chip-count {
  padding: 0.125rem 0.5rem;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.25rem;
}

.activity-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.activity-card:hover {
  transform: translateY(-4px);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 0.75rem;
}

.subject-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.subject-badge.math {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
}

.subject-badge.literature {
  background: rgba(236, 72, 153, 0.15);
  color: #f472b6;
}

.subject-badge.science {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.subject-badge.portuguese {
  background: rgba(251, 146, 60, 0.15);
  color: #fb923c;
}

.subject-badge.default {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.status-badge.completed {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-badge.late {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.activity-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.activity-description {
  font-size: 0.875rem;
  color: #8b92a8;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.deadline-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #8b92a8;
  font-weight: 600;
}

.deadline-info i {
  color: #3b82f6;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  color: #3b82f6;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(59, 130, 246, 0.25);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  margin-bottom: 1.5rem;
}

.empty-icon i {
  font-size: 2.5rem;
  color: #3b82f6;
  opacity: 0.3;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 0.5rem;
}

.empty-text {
  font-size: 1rem;
  color: #8b92a8;
}

@media (max-width: 768px) {
  .activities-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .activities-grid {
    grid-template-columns: 1fr;
  }

  .filter-chips {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.5rem;
  }
}
</style>