<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#1f1d20]/60 backdrop-blur-sm"
        @click.self="close"
      >
        <div 
          class="relative w-full max-w-4xl max-h-[90vh] bg-white rounded-2xl shadow-2xl overflow-hidden"
          @click.stop
        >
          <!-- Header -->
          <div class="sticky top-0 z-10 bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-4">
            <div class="flex items-center justify-between">
              <h2 class="text-2xl font-bold text-white">
                {{ activity?.title || 'Detalhes da Atividade' }}
              </h2>
              <button 
                @click="close"
                class="w-10 h-10 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
              >
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Metadata -->
            <div class="flex items-center gap-4 mt-3 text-sm text-white/80">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{{ activity?.dueDate }}</span>
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span>{{ activity?.subject }}</span>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="overflow-y-auto max-h-[calc(90vh-180px)] p-6">
            <!-- Description -->
            <div class="mb-6">
              <h3 class="text-lg font-semibold text-[#1f1d20] mb-3">Descrição</h3>
              <p class="text-[#1f1d20]/70 leading-relaxed">
                {{ activity?.description || 'Sem descrição disponível.' }}
              </p>
            </div>

            <!-- Attachments -->
            <div v-if="activity?.attachments?.length" class="mb-6">
              <h3 class="text-lg font-semibold text-[#1f1d20] mb-3">Anexos</h3>
              <div class="space-y-2">
                <div 
                  v-for="(attachment, idx) in activity.attachments" 
                  :key="idx"
                  class="flex items-center justify-between p-3 bg-[#e1d4c2]/30 rounded-lg hover:bg-[#e1d4c2]/50 transition-colors"
                >
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-[#2d531a]/10 flex items-center justify-center">
                      <svg class="w-5 h-5 text-[#2d531a]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <span class="text-sm font-medium text-[#1f1d20]">{{ attachment.name }}</span>
                  </div>
                  <button class="p-2 rounded-lg hover:bg-white/50 transition-colors">
                    <svg class="w-5 h-5 text-[#1f1d20]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Submissions -->
            <div v-if="activity?.submissions" class="mb-6">
              <h3 class="text-lg font-semibold text-[#1f1d20] mb-3">Entregas</h3>
              <div class="p-4 bg-[#e1d4c2]/20 rounded-lg">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-[#1f1d20]/70">
                    {{ activity.submissions.submitted }} de {{ activity.submissions.total }} alunos entregaram
                  </span>
                  <div class="flex items-center gap-2">
                    <div class="w-32 h-2 bg-[#e1d4c2] rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] transition-all"
                        :style="{ width: `${(activity.submissions.submitted / activity.submissions.total) * 100}%` }"
                      ></div>
                    </div>
                    <span class="text-sm font-semibold text-[#2d531a]">
                      {{ Math.round((activity.submissions.submitted / activity.submissions.total) * 100) }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="sticky bottom-0 bg-[#e1d4c2]/30 backdrop-blur-sm px-6 py-4 border-t border-[#e1d4c2]">
            <div class="flex items-center justify-end gap-3">
              <button 
                @click="close"
                class="px-6 py-2.5 rounded-lg border border-[#1f1d20]/20 text-[#1f1d20] font-medium hover:bg-[#e1d4c2] transition-colors"
              >
                Fechar
              </button>
              <button 
                class="px-6 py-2.5 rounded-lg bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white font-medium hover:shadow-lg transition-all"
              >
                Editar Atividade
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface Activity {
  title: string;
  subject: string;
  dueDate: string;
  description?: string;
  attachments?: { name: string; url: string }[];
  submissions?: { submitted: number; total: number };
}

defineProps<{
  isOpen: boolean;
  activity?: Activity;
}>();

const emit = defineEmits<{
  close: [];
}>();

const close = () => {
  emit('close');
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div,
.modal-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-enter-from > div,
.modal-leave-to > div {
  transform: scale(0.95);
}
</style>