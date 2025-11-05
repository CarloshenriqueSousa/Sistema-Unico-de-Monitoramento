<template>
  <div class="chat-view">
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Lista de Contatos -->
      <GlassCard class="lg:col-span-1">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Contatos</h2>
          <div class="relative">
            <input 
              type="text" 
              placeholder="Buscar..." 
              class="bg-gray-800 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
            <i class="fas fa-search absolute left-3 top-3 text-gray-500"></i>
          </div>
        </div>
        
        <div class="space-y-3">
          <div 
            v-for="contact in contacts" 
            :key="contact.id"
            class="flex items-center p-3 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors"
            :class="{'bg-gray-700': activeContact?.id === contact.id}"
            @click="activeContact = contact"
          >
            <div class="relative">
              <div class="w-12 h-12 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center mr-3">
                <span class="font-bold text-sm">{{ contact.initials }}</span>
              </div>
              <span v-if="contact.online" class="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 rounded-full border-2 border-gray-900"></span>
            </div>
            <div>
              <p class="font-medium">{{ contact.name }}</p>
              <p class="text-xs text-gray-400">{{ contact.role }}</p>
            </div>
            <span v-if="contact.unread" class="ml-auto bg-rose-500 text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {{ contact.unread }}
            </span>
          </div>
        </div>
      </GlassCard>
      
      <!-- Área de Conversa -->
      <GlassCard class="lg:col-span-3">
        <div v-if="activeContact" class="chat-container h-full flex flex-col">
          <div class="chat-header border-b border-gray-700 pb-4 mb-4">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center mr-3">
                <span class="font-bold text-xs">{{ activeContact.initials }}</span>
              </div>
              <div>
                <p class="font-medium">{{ activeContact.name }}</p>
                <p class="text-xs text-gray-400">{{ activeContact.role }}</p>
              </div>
              <div class="ml-auto flex space-x-3">
                <button class="text-cyan-400 hover:text-cyan-300">
                  <i class="fas fa-phone"></i>
                </button>
                <button class="text-purple-400 hover:text-purple-300">
                  <i class="fas fa-video"></i>
                </button>
                <button class="text-gray-400 hover:text-gray-300">
                  <i class="fas fa-ellipsis-v"></i>
                </button>
              </div>
            </div>
          </div>
          
          <ChatWindow :contact="activeContact" />
        </div>
        
        <div v-else class="flex flex-col items-center justify-center h-full text-gray-500 py-20">
          <i class="fas fa-comments text-5xl mb-4 opacity-30"></i>
          <p class="text-xl">Selecione um contato para iniciar uma conversa</p>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '../../shared/GlassCard.vue';
import ChatWindow from '@components/communication/ChatWindow.vue';

interface Contact {
  id: number;
  name: string;
  role: string;
  initials: string;
  unread: number;
  online: boolean;
}

export default defineComponent({
  name: 'ChatView',
  components: {
    GlassCard,
    ChatWindow
  },
  setup() {
    const contacts = ref<Contact[]>([
      { id: 1, name: 'Ana Costa (PDT)', role: 'Pedagoga', initials: 'AC', unread: 2, online: true },
      { id: 2, name: 'Carlos Oliveira', role: 'Professor de Matemática', initials: 'CO', unread: 0, online: true },
      { id: 3, name: 'Mariana Silva', role: 'Coordenação', initials: 'MS', unread: 1, online: false },
      { id: 4, name: 'Turma 1A', role: 'Grupo de Turma', initials: 'T1', unread: 5, online: true }
    ]);
    
    const activeContact = ref<Contact | null>(null);
    
    return {
      contacts,
      activeContact
    };
  }
});
</script>

<style scoped>
.chat-container {
  min-height: 600px;
}
</style>