<template>
  <div class="notification-center bg-white rounded-2xl shadow-xl border border-[#e1d4c2] overflow-hidden">
    <!-- Header -->
    <div class="notification-header bg-gradient-to-r from-[#0f1e3f] to-[#2d531a] px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white">Notificações</h3>
            <p class="text-xs text-white/70">{{ unreadCount }} não lidas</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <!-- Mark All as Read -->
          <button 
            v-if="unreadCount > 0"
            @click="markAllAsRead"
            class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-all"
          >
            Marcar todas
          </button>

          <!-- Close Button -->
          <button 
            @click="$emit('close')"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="flex items-center gap-2 mt-4">
        <button 
          v-for="filter in filters" 
          :key="filter.value"
          @click="activeFilter = filter.value"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="activeFilter === filter.value 
            ? 'bg-white text-[#2d531a]' 
            : 'bg-white/10 text-white hover:bg-white/20'"
        >
          {{ filter.label }}
          <span 
            v-if="filter.count > 0"
            class="ml-2 px-2 py-0.5 rounded-full text-xs"
            :class="activeFilter === filter.value 
              ? 'bg-[#2d531a] text-white' 
              : 'bg-white/20 text-white'"
          >
            {{ filter.count }}
          </span>
        </button>
      </div>
    </div>

    <!-- Notifications List -->
    <div class="notifications-list overflow-y-auto max-h-[600px]">
      <div v-if="filteredNotifications.length === 0" class="p-12 text-center">
        <div class="w-20 h-20 mx-auto mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
          <svg class="w-10 h-10 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
        </div>
        <p class="text-[#1f1d20] font-medium mb-1">Nenhuma notificação</p>
        <p class="text-sm text-[#1f1d20]/60">Você está em dia!</p>
      </div>

      <TransitionGroup name="notification-list">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          class="notification-item group relative border-b border-[#e1d4c2] hover:bg-[#e1d4c2]/20 transition-colors cursor-pointer"
          :class="{ 'bg-[#2d531a]/5': !notification.read }"
          @click="handleNotificationClick(notification)"
        >
          <div class="p-4 flex items-start gap-4">
            <!-- Icon -->
            <div 
              class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
              :class="getNotificationIconClass(notification.type)"
            >
              <component :is="getNotificationIcon(notification.type)" class="w-6 h-6 text-white" />
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-3 mb-1">
                <h4 
                  class="font-semibold text-[#1f1d20]"
                  :class="{ 'font-bold': !notification.read }"
                >
                  {{ notification.title }}
                </h4>
                <span class="text-xs text-[#1f1d20]/50 flex-shrink-0">
                  {{ notification.time }}
                </span>
              </div>

              <p class="text-sm text-[#1f1d20]/70 line-clamp-2 mb-2">
                {{ notification.message }}
              </p>

              <!-- Tags -->
              <div v-if="notification.tags" class="flex flex-wrap gap-2">
                <span 
                  v-for="tag in notification.tags" 
                  :key="tag"
                  class="px-2 py-1 rounded-full bg-[#e1d4c2] text-[#1f1d20] text-xs"
                >
                  {{ tag }}
                </span>
              </div>

              <!-- Action Buttons -->
              <div v-if="notification.actions" class="flex items-center gap-2 mt-3">
                <button 
                  v-for="action in notification.actions" 
                  :key="action.label"
                  @click.stop="handleAction(notification, action)"
                  class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                  :class="action.primary 
                    ? 'bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white hover:shadow-md' 
                    : 'bg-[#e1d4c2] text-[#1f1d20] hover:bg-[#2d531a] hover:text-white'"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>

            <!-- Unread Indicator -->
            <div 
              v-if="!notification.read"
              class="absolute top-4 left-0 w-1 h-12 bg-[#2d531a] rounded-r"
            ></div>

            <!-- Delete Button -->
            <button 
              @click.stop="deleteNotification(notification.id)"
              class="opacity-0 group-hover:opacity-100 p-2 rounded-lg hover:bg-red-50 transition-all"
            >
              <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- Footer -->
    <div class="notification-footer bg-[#e1d4c2]/30 px-6 py-3 border-t border-[#e1d4c2]">
      <button 
        @click="$emit('view-all')"
        class="w-full py-2 text-sm text-[#2d531a] font-medium hover:underline transition-all"
      >
        Ver todas as notificações
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface NotificationAction {
  label: string;
  primary?: boolean;
  action: string;
}

interface Notification {
  id: string;
  type: 'message' | 'activity' | 'grade' | 'system' | 'reminder';
  title: string;
  message: string;
  time: string;
  read: boolean;
  tags?: string[];
  actions?: NotificationAction[];
}

defineEmits<{
  close: [];
  'view-all': [];
}>();

const activeFilter = ref('all');
const filters = [
  { value: 'all', label: 'Todas', count: 0 },
  { value: 'unread', label: 'Não lidas', count: 0 },
  { value: 'important', label: 'Importantes', count: 0 }
];

const notifications = ref<Notification[]>([
  {
    id: '1',
    type: 'message',
    title: 'Nova mensagem de João Silva',
    message: 'Olá professor, tenho uma dúvida sobre a atividade de matemática...',
    time: '5 min',
    read: false,
    tags: ['Mensagem'],
    actions: [
      { label: 'Responder', primary: true, action: 'reply' }
    ]
  },
  {
    id: '2',
    type: 'activity',
    title: 'Atividade entregue',
    message: 'Maria Santos entregou a atividade "Revolução Industrial"',
    time: '1h',
    read: false,
    tags: ['Atividade', '8º Ano'],
    actions: [
      { label: 'Ver entrega', primary: true, action: 'view' }
    ]
  },
  {
    id: '3',
    type: 'grade',
    title: 'Notas pendentes',
    message: 'Você tem 5 atividades aguardando correção',
    time: '3h',
    read: true,
    tags: ['Avaliação'],
    actions: [
      { label: 'Corrigir', primary: true, action: 'grade' }
    ]
  },
  {
    id: '4',
    type: 'reminder',
    title: 'Reunião agendada',
    message: 'Reunião de pais e mestres amanhã às 14h',
    time: '1d',
    read: true,
    tags: ['Evento']
  },
  {
    id: '5',
    type: 'system',
    title: 'Atualização do sistema',
    message: 'Nova versão disponível com melhorias e correções',
    time: '2d',
    read: true,
    tags: ['Sistema']
  }
]);

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length;
});

const filteredNotifications = computed(() => {
  if (activeFilter.value === 'unread') {
    return notifications.value.filter(n => !n.read);
  }
  if (activeFilter.value === 'important') {
    return notifications.value.filter(n => n.type === 'grade' || n.type === 'reminder');
  }
  return notifications.value;
});

// Update filter counts
filters[0].count = notifications.value.length;
filters[1].count = unreadCount.value;
filters[2].count = notifications.value.filter(n => n.type === 'grade' || n.type === 'reminder').length;

const getNotificationIconClass = (type: string) => {
  const classes = {
    message: 'bg-gradient-to-br from-blue-500 to-blue-600',
    activity: 'bg-gradient-to-br from-[#2d531a] to-[#0f1e3f]',
    grade: 'bg-gradient-to-br from-amber-500 to-amber-600',
    system: 'bg-gradient-to-br from-purple-500 to-purple-600',
    reminder: 'bg-gradient-to-br from-red-500 to-red-600'
  };
  return classes[type as keyof typeof classes] || classes.system;
};

const getNotificationIcon = (type: string) => {
  // Return SVG component based on type
  return 'svg';
};

const handleNotificationClick = (notification: Notification) => {
  notification.read = true;
  console.log('Notification clicked:', notification);
  // Navigate or open modal based on notification type
};

const handleAction = (notification: Notification, action: NotificationAction) => {
  console.log('Action:', action.action, 'for notification:', notification.id);
  notification.read = true;
  // Handle specific action
};

const deleteNotification = (id: string) => {
  const index = notifications.value.findIndex(n => n.id === id);
  if (index > -1) {
    notifications.value.splice(index, 1);
  }
};

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true);
};
</script>

<style scoped>
.notifications-list::-webkit-scrollbar {
  width: 6px;
}

.notifications-list::-webkit-scrollbar-track {
  background: #e1d4c2;
}

.notifications-list::-webkit-scrollbar-thumb {
  background: #2d531a;
  border-radius: 3px;
}

.notifications-list::-webkit-scrollbar-thumb:hover {
  background: #0f1e3f;
}

.notification-list-enter-active,
.notification-list-leave-active {
  transition: all 0.3s ease;
}

.notification-list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.notification-list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>