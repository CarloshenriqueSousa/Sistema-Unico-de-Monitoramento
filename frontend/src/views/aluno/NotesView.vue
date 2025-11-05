<template>
  <div class="notes-root">
    <div class="notes-container">
      <div class="notes-header">
        <div>
          <h1 class="title">Anotações</h1>
          <p class="subtitle">Organize e gerencie seus estudos</p>
        </div>
        <button @click="createNewNote" class="create-btn">
          <i class="fas fa-plus"></i>
          <span>Nova Anotação</span>
        </button>
      </div>

      <div class="notes-layout">
        <div class="notes-sidebar">
          <div class="sidebar-header">
            <h2 class="sidebar-title">Minhas Notas</h2>
            <span class="notes-count">{{ notes.length }}</span>
          </div>

          <div class="search-box">
            <i class="fas fa-search"></i>
            <input 
              type="text" 
              placeholder="Buscar anotações..." 
              class="search-input"
            />
          </div>

          <div class="filter-tabs">
            <button class="filter-tab active">
              <i class="fas fa-inbox"></i>
              <span>Todas</span>
            </button>
            <button class="filter-tab">
              <i class="fas fa-star"></i>
              <span>Favoritas</span>
            </button>
          </div>

          <div class="notes-list">
            <div 
              v-for="note in notes" 
              :key="note.id"
              :class="['note-item', { active: selectedNote?.id === note.id }]"
              @click="selectNote(note)">
              <div class="note-item-header">
                <div class="note-subject-badge" :class="getSubjectColor(note.subject)">
                  {{ note.subject }}
                </div>
                <span class="note-date">{{ formatDate(note.updatedAt) }}</span>
              </div>
              <h3 class="note-item-title">{{ note.title }}</h3>
              <p class="note-item-preview">{{ getPreview(note.content) }}</p>
            </div>
          </div>
        </div>

        <div class="notes-editor">
          <div v-if="selectedNote" class="editor-container">
            <div class="editor-header">
              <input 
                v-model="selectedNote.title" 
                type="text" 
                placeholder="Título da anotação" 
                class="editor-title-input"
              />
              <div class="editor-actions">
                <select v-model="selectedNote.subject" class="subject-select">
                  <option value="Geral">Geral</option>
                  <option value="Matemática">Matemática</option>
                  <option value="Literatura">Literatura</option>
                  <option value="História">História</option>
                  <option value="Ciências">Ciências</option>
                  <option value="Português">Português</option>
                </select>
                <button @click="generateWithAI" class="icon-btn" title="Gerar com IA">
                  <i class="fas fa-magic"></i>
                </button>
                <button @click="deleteNote(selectedNote.id)" class="icon-btn delete-btn">
                  <i class="fas fa-trash"></i>
                </button>
                <button @click="saveNote" class="save-btn">
                  <i class="fas fa-check"></i>
                  <span>Salvar</span>
                </button>
              </div>
            </div>

            <div class="editor-toolbar">
              <button class="toolbar-btn">
                <i class="fas fa-bold"></i>
              </button>
              <button class="toolbar-btn">
                <i class="fas fa-italic"></i>
              </button>
              <button class="toolbar-btn">
                <i class="fas fa-underline"></i>
              </button>
              <div class="toolbar-divider"></div>
              <button class="toolbar-btn">
                <i class="fas fa-list-ul"></i>
              </button>
              <button class="toolbar-btn">
                <i class="fas fa-list-ol"></i>
              </button>
              <div class="toolbar-divider"></div>
              <button class="toolbar-btn">
                <i class="fas fa-link"></i>
              </button>
              <button class="toolbar-btn">
                <i class="fas fa-image"></i>
              </button>
              <button class="toolbar-btn">
                <i class="fas fa-code"></i>
              </button>
            </div>

            <textarea 
              v-model="selectedNote.content" 
              class="editor-textarea"
              placeholder="Comece a escrever suas anotações..."
            ></textarea>

            <div class="editor-footer">
              <span class="editor-info">
                <i class="fas fa-clock"></i>
                Última edição: {{ formatDateTime(selectedNote.updatedAt) }}
              </span>
              <span class="editor-info">
                {{ getWordCount(selectedNote.content) }} palavras
              </span>
            </div>
          </div>

          <div v-else class="empty-editor">
            <div class="empty-icon">
              <i class="fas fa-pen-fancy"></i>
            </div>
            <h3 class="empty-title">Nenhuma nota selecionada</h3>
            <p class="empty-text">Selecione uma anotação ou crie uma nova para começar</p>
            <button @click="createNewNote" class="create-note-btn">
              <i class="fas fa-plus"></i>
              <span>Criar Nova Anotação</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useAIStore } from '@/store/ai';

interface Note {
  id: number;
  title: string;
  content: string;
  subject: string;
  createdAt: string;
  updatedAt: string;
}

export default defineComponent({
  name: 'NotesView',
  setup() {
    const notes = ref<Note[]>([
      { 
        id: 1, 
        title: 'Álgebra Linear - Matrizes', 
        content: 'Conceitos básicos de matrizes e operações fundamentais. Matriz identidade, matriz inversa, determinantes...', 
        subject: 'Matemática',
        createdAt: '2025-10-15',
        updatedAt: '2025-10-28'
      },
      { 
        id: 2, 
        title: 'Revolução Industrial', 
        content: 'Impactos sociais e econômicos da Revolução Industrial. Transformações no modo de produção...', 
        subject: 'História',
        createdAt: '2025-10-20',
        updatedAt: '2025-10-25'
      },
      { 
        id: 3, 
        title: 'Termodinâmica', 
        content: 'Leis da termodinâmica. Primeira lei: conservação de energia. Segunda lei: entropia...', 
        subject: 'Ciências',
        createdAt: '2025-10-18',
        updatedAt: '2025-10-29'
      }
    ]);
    
    const selectedNote = ref<Note | null>(null);
    const ai = useAIStore();
    
    const selectNote = (note: Note) => { 
      selectedNote.value = { ...note }; 
    };
    
    const createNewNote = () => {
      const newNote: Note = {
        id: Date.now(),
        title: 'Nova Anotação',
        content: '',
        subject: 'Geral',
        createdAt: new Date().toISOString().split('T')[0],
        updatedAt: new Date().toISOString().split('T')[0]
      };
      notes.value.unshift(newNote);
      selectedNote.value = newNote;
    };
    
    const saveNote = () => {
      if (!selectedNote.value) return;
      const index = notes.value.findIndex(n => n.id === selectedNote.value!.id);
      if (index !== -1) {
        notes.value[index] = { 
          ...selectedNote.value, 
          updatedAt: new Date().toISOString().split('T')[0]
        };
      }
    };
    
    const generateWithAI = async () => {
      if (!selectedNote.value) return;
      const payload = {
        subject: selectedNote.value.subject || 'Geral',
        topics: selectedNote.value.title ? [selectedNote.value.title] : [],
        level: 'médio'
      } as any;
      const result = await ai.generateNotes(payload);
      if (result) {
        selectedNote.value.content = result;
      }
    };
    
    const deleteNote = (noteId: number) => {
      notes.value = notes.value.filter(n => n.id !== noteId);
      if (selectedNote.value?.id === noteId) {
        selectedNote.value = null;
      }
    };

    const getPreview = (content: string) => {
      return content.length > 80 ? content.substring(0, 80) + '...' : content;
    };

    const getWordCount = (content: string) => {
      return content.trim().split(/\s+/).filter(word => word.length > 0).length;
    };

    const getSubjectColor = (subject: string) => {
      const colors: Record<string, string> = {
        'Matemática': 'math',
        'Literatura': 'literature',
        'História': 'history',
        'Ciências': 'science',
        'Português': 'portuguese',
        'Geral': 'general'
      };
      return colors[subject] || 'general';
    };

    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat('pt-BR', { 
        day: '2-digit', 
        month: 'short' 
      }).format(date);
    };

    const formatDateTime = (dateStr: string) => {
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat('pt-BR', { 
        day: '2-digit', 
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    return { 
      notes, 
      selectedNote, 
      selectNote, 
      createNewNote, 
      saveNote, 
      deleteNote,
      getPreview,
      getWordCount,
      getSubjectColor,
      formatDate,
      formatDateTime,
      generateWithAI
    };
  },
});
</script>

<style scoped>
.notes-root {
  min-height: 100vh;
  background: #17181e;
  color: #fcfcfc;
  padding: 2rem;
}

.notes-container {
  max-width: 1400px;
  margin: 0 auto;
}

.notes-header {
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

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.notes-layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 1.5rem;
  height: calc(100vh - 200px);
}

.notes-sidebar {
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

.notes-count {
  padding: 0.25rem 0.625rem;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 999px;
  font-size: 0.8125rem;
  font-weight: 700;
  color: #3b82f6;
}

.search-box {
  position: relative;
  margin-bottom: 1rem;
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

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.filter-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: #8b92a8;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.05);
}

.filter-tab.active {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.notes-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.note-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.note-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.note-item.active {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

.note-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.625rem;
}

.note-subject-badge {
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.note-subject-badge.math { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }
.note-subject-badge.literature { background: rgba(236, 72, 153, 0.2); color: #f472b6; }
.note-subject-badge.history { background: rgba(251, 146, 60, 0.2); color: #fb923c; }
.note-subject-badge.science { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.note-subject-badge.portuguese { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.note-subject-badge.general { background: rgba(139, 146, 168, 0.2); color: #8b92a8; }

.note-date {
  font-size: 0.75rem;
  color: #8b92a8;
  font-weight: 500;
}

.note-item-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fcfcfc;
  margin-bottom: 0.375rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-item-preview {
  font-size: 0.8125rem;
  color: #8b92a8;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notes-editor {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.editor-title-input {
  flex: 1;
  padding: 0.625rem 0;
  background: transparent;
  border: none;
  color: #fcfcfc;
  font-size: 1.5rem;
  font-weight: 700;
  outline: none;
}

.editor-actions {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.subject-select {
  padding: 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fcfcfc;
  font-size: 0.875rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
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
  background: rgba(255, 255, 255, 0.08);
  color: #fcfcfc;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.toolbar-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: #8b92a8;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toolbar-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.toolbar-divider {
  width: 1px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0 0.25rem;
}

.editor-textarea {
  flex: 1;
  padding: 1.5rem;
  background: transparent;
  border: none;
  color: #fcfcfc;
  font-size: 1rem;
  font-family: inherit;
  line-height: 1.7;
  resize: none;
  outline: none;
}

.editor-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.editor-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 500;
}

.empty-editor {
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
  margin-bottom: 2rem;
}

.create-note-btn {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-note-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

@media (max-width: 1024px) {
  .notes-layout {
    grid-template-columns: 1fr;
  }

  .notes-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .notes-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .notes-layout {
    height: calc(100vh - 160px);
  }
}
</style>