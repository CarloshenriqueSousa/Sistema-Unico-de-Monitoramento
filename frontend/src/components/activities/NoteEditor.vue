// NoteEditor.vue
<template>
  <div class="note-editor glass-card p-6 rounded-2xl relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-emerald-900/30 to-green-900/20 z-0"></div>
    <h3 class="text-2xl font-bold mb-6 text-emerald-400 flex items-center relative z-10">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
      Editor de Anotações com IA
    </h3>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
      <!-- Painel de configuração -->
      <div class="config-panel lg:col-span-1">
        <div class="mb-4">
          <label class="block text-sm text-emerald-300 mb-2">Título</label>
          <input 
            v-model="noteTitle" 
            type="text" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
            placeholder="Título da anotação"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-emerald-300 mb-2">Tópico Principal</label>
          <input 
            v-model="mainTopic" 
            type="text" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
            placeholder="Ex: Revolução Francesa, Álgebra..."
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-emerald-300 mb-2">Subtópicos</label>
          <textarea 
            v-model="subTopics" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
            rows="3"
            placeholder="Liste subtópicos separados por vírgula"
          ></textarea>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-emerald-300 mb-2">Formato</label>
          <div class="grid grid-cols-2 gap-2">
            <button 
              v-for="format in formats" 
              :key="format.value"
              @click="selectedFormat = format.value"
              class="py-2 rounded-lg transition-colors"
              :class="selectedFormat === format.value ? 'bg-emerald-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
            >
              {{ format.label }}
            </button>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-emerald-300 mb-2">Detalhes Adicionais</label>
          <textarea 
            v-model="additionalDetails" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
            rows="3"
            placeholder="Conceitos importantes, referências..."
          ></textarea>
        </div>
        
        <Button 
          @click="generateNote" 
          variant="primary" 
          class="w-full py-3 bg-gradient-to-r from-emerald-600 to-green-700 hover:from-emerald-500 hover:to-green-600"
          :loading="isGenerating"
        >
          <SparklesIcon class="w-5 h-5 mr-2" /> Gerar Anotação com IA
        </Button>
      </div>
      
      <!-- Editor de anotações -->
      <div class="editor-panel lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h4 class="text-lg font-bold text-emerald-300">Editor de Anotações</h4>
          <div class="flex gap-2">
            <Button 
              @click="saveNote" 
              variant="secondary" 
              class="px-4"
              :disabled="!noteContent"
            >
              <SaveIcon class="w-5 h-5 mr-2" /> Salvar
            </Button>
            <Button variant="secondary" class="px-3">
              <DownloadIcon class="w-5 h-5" />
            </Button>
          </div>
        </div>
        
        <div class="editor-container glass-card-inner rounded-xl overflow-hidden">
          <textarea
            v-model="noteContent"
            class="w-full h-96 p-6 bg-transparent text-white focus:outline-none resize-none"
            placeholder="Comece a digitar ou gere uma anotação com IA..."
          ></textarea>
          
          <!-- Barra de ferramentas -->
          <div class="toolbar bg-gray-800 border-t border-gray-700 p-3 flex flex-wrap gap-2">
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <BoldIcon class="w-5 h-5" />
            </button>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <ItalicIcon class="w-5 h-5" />
            </button>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <UnderlineIcon class="w-5 h-5" />
            </button>
            <div class="border-r border-gray-700 h-6 mx-2"></div>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <ListBulletIcon class="w-5 h-5" />
            </button>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <ListNumberIcon class="w-5 h-5" />
            </button>
            <div class="border-r border-gray-700 h-6 mx-2"></div>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <LinkIcon class="w-5 h-5" />
            </button>
            <button class="p-2 rounded-lg hover:bg-gray-700">
              <ImageIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <!-- Sugestões de IA -->
        <div v-if="aiSuggestions.length > 0" class="suggestions mt-6">
          <h5 class="text-md font-bold text-emerald-300 mb-3">Sugestões de IA</h5>
          <div class="space-y-3">
            <button 
              v-for="(suggestion, index) in aiSuggestions" 
              :key="index"
              @click="applySuggestion(suggestion)"
              class="suggestion-item w-full p-3 bg-gray-800 rounded-lg border border-gray-700 text-left hover:bg-gray-700 transition-colors"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Efeito de partículas -->
    <div class="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-emerald-500/20 blur-3xl z-0"></div>
    <div class="absolute -bottom-10 -left-10 w-40 h-40 rounded-full bg-green-500/20 blur-3xl z-0"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Button from '@/shared/Button.vue';
import SparklesIcon from '@/assets/SparklesIcon.vue';
import SaveIcon from '@/assets/SaveIcon.vue';
import DownloadIcon from '@/assets/DownloadIcon.vue';
import BoldIcon from '@/assets/BoldIcon.vue';
import ItalicIcon from '@/assets/ItalicIcon.vue';
import UnderlineIcon from '@/assets/UnderlineIcon.vue';
import ListBulletIcon from '@/assets/ListBulletIcon.vue';
import ListNumberIcon from '@/assets/ListNumberIcon.vue';
import LinkIcon from '@/assets/LinkIcon.vue';
import ImageIcon from '@/assets/ImageIcon.vue';

export default defineComponent({
  name: 'NoteEditor3D',
  components: { 
    Button, 
    SparklesIcon, 
    SaveIcon,
    DownloadIcon,
    BoldIcon,
    ItalicIcon,
    UnderlineIcon,
    ListBulletIcon,
    ListNumberIcon,
    LinkIcon,
    ImageIcon
  },
  setup() {
    const noteTitle = ref('');
    const mainTopic = ref('');
    const subTopics = ref('');
    const selectedFormat = ref('outline');
    const additionalDetails = ref('');
    const noteContent = ref('');
    const aiSuggestions = ref<string[]>([]);
    const isGenerating = ref(false);
    
    const formats = [
      { value: 'outline', label: 'Esquema' },
      { value: 'summary', label: 'Resumo' },
      { value: 'detailed', label: 'Detalhado' },
      { value: 'mindmap', label: 'Mapa Mental' }
    ];
    
    const generateNote = async () => {
      if (!mainTopic.value) return;
      
      isGenerating.value = true;
      noteContent.value = '';
      aiSuggestions.value = [];
      
      // Simulação de chamada à API de IA
      await new Promise(resolve => setTimeout(resolve, 2500));
      
      // Conteúdo gerado pela IA
      noteContent.value = `# ${mainTopic.value}\n\n` +
        `## Introdução\n` +
        `Aqui está uma introdução sobre ${mainTopic.value}...\n\n` +
        `## Principais Conceitos\n` +
        `- Conceito 1: Descrição breve\n` +
        `- Conceito 2: Descrição breve\n` +
        `- Conceito 3: Descrição breve\n\n` +
        `## Conclusão\n` +
        `Resumo dos pontos mais importantes sobre ${mainTopic.value}.`;
      
      // Gerar sugestões
      aiSuggestions.value = [
        'Adicionar linha do tempo histórica',
        'Incluir exemplos práticos',
        'Adicionar citações importantes',
        'Criar diagrama de relações'
      ];
      
      isGenerating.value = false;
    };
    
    const applySuggestion = (suggestion: string) => {
      noteContent.value += `\n\n## ${suggestion}\n[Adicione conteúdo aqui]`;
    };
    
    const saveNote = () => {
      console.log('Anotação salva:', noteContent.value);
      // Lógica para salvar no backend
    };

    return {
      noteTitle,
      mainTopic,
      subTopics,
      selectedFormat,
      additionalDetails,
      noteContent,
      aiSuggestions,
      isGenerating,
      formats,
      generateNote,
      applySuggestion,
      saveNote
    };
  }
});
</script>

<style scoped>
.glass-card {
  background: rgba(25, 35, 40, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.glass-card-inner {
  background: rgba(20, 30, 35, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.editor-container {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.toolbar {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.suggestion-item {
  transition: all 0.2s ease;
}

.suggestion-item:hover {
  border-color: rgba(52, 211, 153, 0.5);
  transform: translateY(-2px);
}
</style>