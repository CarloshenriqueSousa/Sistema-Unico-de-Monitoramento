<template>
  <div class="chat-window flex flex-col bg-white rounded-2xl shadow-lg border border-[#e1d4c2] overflow-hidden h-full">
    <!-- Header -->
    <div class="chat-header bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] px-6 py-4 flex-shrink-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="relative">
            <div class="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center text-white font-bold text-lg">
              {{ getInitials(currentContact?.name) }}
            </div>
            <div 
              v-if="currentContact?.online"
              class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-400 rounded-full border-2 border-white"
            ></div>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white">{{ currentContact?.name || 'Selecione um contato' }}</h3>
            <p class="text-xs text-white/70">
              {{ currentContact?.online ? 'Online' : 'Offline' }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button 
            @click="startVideoCall"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
            title="Videochamada"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
          <button 
            @click="$emit('close')"
            class="p-2 rounded-lg hover:bg-white/10 transition-colors"
            title="Fechar"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Messages Area -->
    <div 
      ref="messagesContainer"
      class="messages-area flex-1 overflow-y-auto p-6 space-y-4 bg-[#e1d4c2]/10"
    >
      <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-[#e1d4c2] flex items-center justify-center">
            <svg class="w-8 h-8 text-[#1f1d20]/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <p class="text-[#1f1d20]/60 text-sm">Nenhuma mensagem ainda</p>
          <p class="text-[#1f1d20]/40 text-xs mt-1">Envie uma mensagem para começar</p>
        </div>
      </div>

      <div 
        v-for="message in messages" 
        :key="message.id"
        class="message-item"
        :class="message.sent ? 'sent' : 'received'"
      >
        <div 
          class="message-bubble max-w-[70%] rounded-2xl px-4 py-3 shadow-sm"
          :class="message.sent 
            ? 'ml-auto bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white' 
            : 'bg-white text-[#1f1d20] border border-[#e1d4c2]'"
        >
          <p class="text-sm leading-relaxed whitespace-pre-wrap">{{ message.text }}</p>
          <div 
            class="flex items-center justify-between gap-3 mt-2 pt-2 border-t"
            :class="message.sent ? 'border-white/20' : 'border-[#e1d4c2]'"
          >
            <span 
              class="text-xs"
              :class="message.sent ? 'text-white/70' : 'text-[#1f1d20]/50'"
            >
              {{ message.time }}
            </span>
            <div v-if="message.sent" class="flex items-center gap-1">
              <svg 
                v-if="message.read"
                class="w-4 h-4 text-white/70" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <svg 
                v-else
                class="w-4 h-4 text-white/70" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isTyping" class="message-item received">
        <div class="message-bubble max-w-[70%] rounded-2xl px-4 py-3 bg-white border border-[#e1d4c2]">
          <div class="flex items-center gap-2">
            <div class="flex gap-1">
              <div class="w-2 h-2 bg-[#2d531a] rounded-full animate-bounce" style="animation-delay: 0ms"></div>
              <div class="w-2 h-2 bg-[#2d531a] rounded-full animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 bg-[#2d531a] rounded-full animate-bounce" style="animation-delay: 300ms"></div>
            </div>
            <span class="text-xs text-[#1f1d20]/50">digitando...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-area bg-white border-t border-[#e1d4c2] p-4 flex-shrink-0">
      <div class="flex items-end gap-3">
        <!-- Attachment Button -->
        <button 
          @click="attachFile"
          class="p-2.5 rounded-lg bg-[#e1d4c2] hover:bg-[#2d531a] text-[#1f1d20] hover:text-white transition-all flex-shrink-0"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
          </svg>
        </button>

        <!-- Text Input -->
        <div class="flex-1 relative">
          <textarea
            v-model="newMessage"
            @keydown.enter.exact.prevent="sendMessage"
            @input="handleTyping"
            rows="1"
            placeholder="Digite sua mensagem..."
            class="w-full px-4 py-3 pr-12 bg-[#e1d4c2]/30 border border-[#e1d4c2] rounded-xl text-[#1f1d20] placeholder-[#1f1d20]/40 focus:outline-none focus:ring-2 focus:ring-[#2d531a] focus:border-transparent transition-all resize-none max-h-32"
          ></textarea>
          
          <!-- Emoji Button -->
          <button 
            @click="toggleEmojiPicker"
            class="absolute right-3 bottom-3 p-1 rounded-lg hover:bg-[#e1d4c2] transition-colors"
          >
            <svg class="w-5 h-5 text-[#1f1d20]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>

        <!-- Send Button -->
        <button 
          @click="sendMessage"
          :disabled="!newMessage.trim()"
          class="p-3 rounded-xl bg-gradient-to-r from-[#2d531a] to-[#0f1e3f] text-white hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex-shrink-0"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';

interface Message {
  id: string;
  text: string;
  time: string;
  sent: boolean;
  read?: boolean;
}

interface Contact {
  id: string;
  name: string;
  online: boolean;
}

const props = defineProps<{
  currentContact?: Contact;
}>();

const emit = defineEmits<{
  close: [];
}>();

const messagesContainer = ref<HTMLElement | null>(null);
const newMessage = ref('');
const isTyping = ref(false);
const messages = ref<Message[]>([
  {
    id: '1',
    text: 'Olá! Como posso ajudar?',
    time: '10:30',
    sent: false
  },
  {
    id: '2',
    text: 'Preciso de ajuda com a atividade de matemática',
    time: '10:31',
    sent: true,
    read: true
  }
]);

const getInitials = (name?: string) => {
  if (!name) return '?';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;

  const message: Message = {
    id: Date.now().toString(),
    text: newMessage.value,
    time: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
    sent: true,
    read: false
  };

  messages.value.push(message);
  newMessage.value = '';
  scrollToBottom();

  // Simulate read after 2s
  setTimeout(() => {
    message.read = true;
  }, 2000);
};

let typingTimeout: any;
const handleTyping = () => {
  // Simulate typing indicator
  clearTimeout(typingTimeout);
  typingTimeout = setTimeout(() => {
    // Send typing stopped event
  }, 1000);
};

const attachFile = () => {
  console.log('Attach file');
};

const toggleEmojiPicker = () => {
  console.log('Toggle emoji picker');
};

const startVideoCall = () => {
  console.log('Starting video call');
};

watch(() => props.currentContact, () => {
  // Load messages for new contact
  messages.value = [];
}, { deep: true });
</script>

<style scoped>
.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-track {
  background: #e1d4c2;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb {
  background: #2d531a;
  border-radius: 3px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background: #0f1e3f;
}

.message-item {
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

textarea {
  field-sizing: content;
}
</style>