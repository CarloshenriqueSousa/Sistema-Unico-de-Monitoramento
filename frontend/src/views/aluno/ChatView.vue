<template>
  <div class="chat-root">
    <div class="chat-container">
      <div class="chat-header">
        <h1 class="title">Mensagens</h1>
        <p class="subtitle">Converse com professores e colegas</p>
      </div>

      <div class="chat-layout">
        <div class="contacts-sidebar">
          <div class="sidebar-header">
            <h2 class="sidebar-title">Conversas</h2>
            <button class="icon-btn">
              <i class="fas fa-edit"></i>
            </button>
          </div>

          <div class="search-box">
            <i class="fas fa-search"></i>
            <input 
              v-model="search" 
              type="text" 
              placeholder="Buscar contatos..." 
              class="search-input"
            />
          </div>

          <div class="contacts-list">
            <div 
              v-for="contact in filteredContacts" 
              :key="contact.id"
              :class="['contact-item', { active: activeContact?.id === contact.id }]"
              @click="selectContact(contact)">
              <div class="contact-avatar">
                <img v-if="contact.avatar" :src="contact.avatar" :alt="contact.name" />
                <div v-else class="avatar-placeholder">
                  {{ contact.name.charAt(0) }}
                </div>
                <div v-if="contact.online" class="online-indicator"></div>
              </div>
              
              <div class="contact-info">
                <div class="contact-header">
                  <h3 class="contact-name">{{ contact.name }}</h3>
                  <span class="contact-time">2h</span>
                </div>
                <div class="contact-preview">
                  <span class="contact-role">{{ contact.role }}</span>
                  <span class="contact-separator">•</span>
                  <span class="last-message">{{ contact.lastMessage }}</span>
                </div>
              </div>
              
              <div v-if="contact.unread > 0" class="unread-badge">
                {{ contact.unread }}
              </div>
            </div>
          </div>
        </div>

        <div class="chat-content">
          <div v-if="activeContact" class="chat-area">
            <div class="chat-topbar">
              <div class="chat-user-info">
                <div class="chat-avatar">
                  <div class="avatar-placeholder">
                    {{ activeContact.name.charAt(0) }}
                  </div>
                  <div v-if="activeContact.online" class="online-indicator"></div>
                </div>
                <div>
                  <h3 class="chat-user-name">{{ activeContact.name }}</h3>
                  <p class="chat-user-status">
                    <span v-if="activeContact.online">Online agora</span>
                    <span v-else>Ausente</span>
                  </p>
                </div>
              </div>
              <div class="chat-actions">
                <button class="icon-btn">
                  <i class="fas fa-phone"></i>
                </button>
                <button class="icon-btn">
                  <i class="fas fa-video"></i>
                </button>
                <button class="icon-btn">
                  <i class="fas fa-ellipsis-v"></i>
                </button>
              </div>
            </div>

            <div class="messages-container">
              <div class="messages-scroll">
                <div class="date-separator">
                  <span>Hoje</span>
                </div>

                <div class="message received">
                  <div class="message-avatar">
                    {{ activeContact.name.charAt(0) }}
                  </div>
                  <div class="message-content">
                    <div class="message-bubble">
                      <p>{{ activeContact.lastMessage }}</p>
                    </div>
                    <span class="message-time">14:30</span>
                  </div>
                </div>

                <div class="message sent">
                  <div class="message-content">
                    <div class="message-bubble">
                      <p>Entendi! Vou revisar o conteúdo e fazer os exercícios.</p>
                    </div>
                    <span class="message-time">14:32</span>
                  </div>
                </div>

                <div class="message received">
                  <div class="message-avatar">
                    {{ activeContact.name.charAt(0) }}
                  </div>
                  <div class="message-content">
                    <div class="message-bubble">
                      <p>Ótimo! Se tiver dúvidas, estou à disposição.</p>
                    </div>
                    <span class="message-time">14:33</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="message-input-container">
              <button class="icon-btn">
                <i class="fas fa-paperclip"></i>
              </button>
              <input 
                v-model="draftMessage"
                @keydown.enter.prevent="handleSend"
                type="text" 
                placeholder="Digite sua mensagem..." 
                class="message-input"
              />
              <button class="send-btn" @click="handleSend" :disabled="!draftMessage.trim()">
                <i class="fas fa-paper-plane"></i>
              </button>
            </div>
          </div>

          <div v-else class="empty-chat">
            <div class="empty-icon">
              <i class="fas fa-comments"></i>
            </div>
            <h3 class="empty-title">Selecione uma conversa</h3>
            <p class="empty-text">Escolha um contato para iniciar uma conversa</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useAIStore } from '@/store/ai';

interface Contact {
  id: number;
  name: string;
  role: 'Professor' | 'Aluno' | 'PDT';
  avatar: string;
  lastMessage: string;
  unread: number;
  online: boolean;
}

export default defineComponent({
  name: 'ChatView',
  setup() {
    const contacts = ref<Contact[]>([
      { 
        id: 1, 
        name: 'Prof. Mariana Silva', 
        role: 'Professor', 
        avatar: '', 
        lastMessage: 'Não esqueça da atividade de álgebra', 
        unread: 2, 
        online: true 
      },
      { 
        id: 2, 
        name: 'Carlos Oliveira', 
        role: 'Aluno', 
        avatar: '', 
        lastMessage: 'Você fez o exercício 5?', 
        unread: 0, 
        online: true 
      },
      { 
        id: 3, 
        name: 'Ana Beatriz (PDT)', 
        role: 'PDT', 
        avatar: '', 
        lastMessage: 'Seu relatório foi analisado', 
        unread: 1, 
        online: false 
      },
      { 
        id: 4, 
        name: 'Prof. João Santos', 
        role: 'Professor', 
        avatar: '', 
        lastMessage: 'Parabéns pelo desempenho!', 
        unread: 0, 
        online: false 
      }
    ]);
    
    const search = ref('');
    const activeContact = ref<Contact | null>(null);
    const draftMessage = ref('');
    const ai = useAIStore();
    
    const filteredContacts = computed(() => {
      if (!search.value) return contacts.value;
      return contacts.value.filter(c => 
        c.name.toLowerCase().includes(search.value.toLowerCase())
      );
    });
    
    const selectContact = (contact: Contact) => {
      activeContact.value = contact;
      contact.unread = 0;
    };
    
    const handleSend = async () => {
      if (!draftMessage.value.trim()) return;
      // For now, send as a generic chat to AI backend to unblock UI
      const userText = draftMessage.value;
      draftMessage.value = '';
      // Append a local echo message
      // In a full impl, messages would be a reactive list; here we rely on UI placeholders
      await ai.sendChatMessage({ role: 'user', message: userText, context: activeContact.value?.name || '' });
    };

    return { 
      contacts, 
      search, 
      filteredContacts, 
      activeContact, 
      selectContact,
      draftMessage,
      handleSend,
    };
  },
});
</script>

<style scoped>
.chat-root {
  min-height: 100vh;
  background: #17181e;
  color: #fcfcfc;
  padding: 2rem;
}

.chat-container {
  max-width: 1400px;
  margin: 0 auto;
}

.chat-header {
  margin-bottom: 2rem;
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

.chat-layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 1.5rem;
  height: calc(100vh - 200px);
}

.contacts-sidebar {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fcfcfc;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #8b92a8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.search-box {
  position: relative;
  margin-bottom: 1.25rem;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #8b92a8;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fcfcfc;
  font-size: 0.9375rem;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.3);
}

.contacts-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.contact-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.contact-item.active {
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.contact-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 12px;
  font-size: 1.125rem;
  font-weight: 700;
  color: #fff;
}

.online-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: #10b981;
  border: 2px solid #17181e;
  border-radius: 50%;
}

.contact-info {
  flex: 1;
  min-width: 0;
}

.contact-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.contact-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fcfcfc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.contact-time {
  font-size: 0.75rem;
  color: #8b92a8;
  flex-shrink: 0;
}

.contact-preview {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
}

.contact-role {
  color: #3b82f6;
  font-weight: 600;
  flex-shrink: 0;
}

.contact-separator {
  color: #8b92a8;
}

.last-message {
  color: #8b92a8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3b82f6;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.chat-content {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chat-area {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chat-avatar {
  position: relative;
}

.chat-user-name {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 0.25rem;
}

.chat-user-status {
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 500;
}

.chat-actions {
  display: flex;
  gap: 0.5rem;
}

.messages-container {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.messages-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.date-separator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
}

.date-separator span {
  padding: 0.375rem 0.875rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #8b92a8;
}

.message {
  display: flex;
  gap: 0.75rem;
  animation: fadeIn 0.3s ease;
}

.message.sent {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  max-width: 60%;
}

.message.sent .message-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 0.875rem 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  color: #fcfcfc;
  font-size: 0.9375rem;
  line-height: 1.5;
}

.message.sent .message-bubble {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: #fff;
}

.message-time {
  font-size: 0.75rem;
  color: #8b92a8;
  font-weight: 500;
}

.message-input-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.message-input {
  flex: 1;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fcfcfc;
  font-size: 0.9375rem;
  outline: none;
  transition: all 0.2s ease;
}

.message-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(59, 130, 246, 0.3);
}

.send-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 2rem;
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

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .chat-layout {
    grid-template-columns: 1fr;
  }

  .contacts-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .chat-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .chat-layout {
    height: calc(100vh - 160px);
  }

  .message-content {
    max-width: 75%;
  }
}
</style>