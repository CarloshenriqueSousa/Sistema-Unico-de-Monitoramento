// ExamCreator.vue
<template>
  <div class="exam-creator glass-card p-6 rounded-2xl relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-purple-900/30 to-indigo-900/20 z-0"></div>
    <h3 class="text-2xl font-bold mb-6 text-purple-400 flex items-center relative z-10">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      Criador de Provas com IA
    </h3>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 relative z-10">
      <!-- Painel de configuração -->
      <div class="config-panel lg:col-span-1">
        <div class="mb-4">
          <label class="block text-sm text-purple-300 mb-2">Matéria</label>
          <input 
            v-model="subject" 
            type="text" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 focus:outline-none" 
            placeholder="Matemática, História..."
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-purple-300 mb-2">Tópicos</label>
          <textarea 
            v-model="topics" 
            class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 focus:outline-none" 
            rows="3"
            placeholder="Liste os tópicos separados por vírgula"
          ></textarea>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-purple-300 mb-2">Nível</label>
          <div class="grid grid-cols-2 gap-2">
            <button 
              v-for="level in levels" 
              :key="level.value"
              @click="selectedLevel = level.value"
              class="py-2 rounded-lg transition-colors"
              :class="selectedLevel === level.value ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
            >
              {{ level.label }}
            </button>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-purple-300 mb-2">Tipo de Questões</label>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="type in questionTypes" 
              :key="type.value"
              @click="toggleQuestionType(type.value)"
              class="px-3 py-1 rounded-full transition-colors"
              :class="selectedQuestionTypes.includes(type.value) ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
            >
              {{ type.label }}
            </button>
          </div>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm text-purple-300 mb-2">Número de Questões</label>
          <input 
            v-model.number="questionCount" 
            type="range" 
            min="5" 
            max="30" 
            class="w-full accent-purple-500"
          >
          <div class="text-center text-purple-400 font-medium">{{ questionCount }} questões</div>
        </div>
        
        <Button 
          @click="generateQuestions" 
          variant="primary" 
          class="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-700 hover:from-purple-500 hover:to-indigo-600"
          :loading="isGenerating"
        >
          <SparklesIcon class="w-5 h-5 mr-2" /> Gerar Prova com IA
        </Button>
      </div>
      
      <!-- Visualização da prova -->
      <div class="exam-preview lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h4 class="text-lg font-bold text-purple-300">Pré-visualização da Prova</h4>
          <Button 
            @click="saveExam" 
            variant="secondary" 
            class="px-4"
            :disabled="questions.length === 0"
          >
            <SaveIcon class="w-5 h-5 mr-2" /> Salvar Prova
          </Button>
        </div>
        
        <div class="exam-content glass-card-inner p-6 rounded-xl overflow-y-auto max-h-[70vh]">
          <div v-if="isGenerating" class="flex flex-col items-center justify-center py-12">
            <div class="w-16 h-16 mb-4">
              <div class="w-full h-full rounded-full border-4 border-purple-500 border-t-transparent animate-spin"></div>
            </div>
            <p class="text-purple-400">Gerando questões com IA...</p>
          </div>
          
          <div v-else-if="questions.length > 0">
            <div class="exam-header text-center mb-8">
              <h2 class="text-2xl font-bold text-white">{{ subject || 'Prova' }}</h2>
              <div class="text-purple-300 mt-2">Prova Opcional - {{ selectedLevelLabel }}</div>
            </div>
            
            <div 
              v-for="(question, index) in questions" 
              :key="index"
              class="question mb-8 p-4 border-b border-gray-700 last:border-0"
            >
              <div class="flex items-start">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center text-white font-bold mr-3 flex-shrink-0">
                  {{ index + 1 }}
                </div>
                <div class="flex-1">
                  <div class="question-text text-white mb-3" v-html="question.text"></div>
                  
                  <div v-if="question.type === 'multiple_choice'" class="options space-y-2">
                    <div 
                      v-for="(option, optIndex) in question.options" 
                      :key="optIndex"
                      class="option p-3 rounded-lg bg-gray-800 border border-gray-700"
                    >
                      <div class="flex items-start">
                        <div class="w-6 h-6 rounded-full border border-purple-500 flex items-center justify-center text-sm text-purple-300 mr-2 mt-0.5">
                          {{ String.fromCharCode(65 + optIndex) }}
                        </div>
                        <div class="flex-1" v-html="option"></div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-else-if="question.type === 'true_false'" class="options grid grid-cols-2 gap-2 mt-3">
                    <div class="option p-3 rounded-lg bg-gray-800 border border-gray-700 text-center">
                      Verdadeiro
                    </div>
                    <div class="option p-3 rounded-lg bg-gray-800 border border-gray-700 text-center">
                      Falso
                    </div>
                  </div>
                  
                  <div v-else-if="question.type === 'open_ended'" class="answer-field mt-3">
                    <div class="h-24 bg-gray-800 rounded-lg border border-dashed border-gray-700"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="flex flex-col items-center justify-center py-12 text-center text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>Configure a prova e clique em "Gerar Prova com IA" para criar questões personalizadas.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Efeito de partículas -->
    <div class="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-purple-500/20 blur-3xl z-0"></div>
    <div class="absolute -bottom-10 -left-10 w-40 h-40 rounded-full bg-indigo-500/20 blur-3xl z-0"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import Button from '@/shared/Button.vue';
import SparklesIcon from '@/assets/SparklesIcon.vue';
import SaveIcon from '@/assets/SaveIcon.vue';

interface Question {
  text: string;
  type: string;
  options?: string[];
}

export default defineComponent({
  name: 'ExamCreator3D',
  components: { Button, SparklesIcon, SaveIcon },
  setup() {
    const subject = ref('');
    const topics = ref('');
    const selectedLevel = ref('medium');
    const questionCount = ref(10);
    const selectedQuestionTypes = ref(['multiple_choice', 'true_false', 'open_ended']);
    const questions = ref<Question[]>([]);
    const isGenerating = ref(false);
    
    const levels = [
      { value: 'easy', label: 'Fácil' },
      { value: 'medium', label: 'Médio' },
      { value: 'hard', label: 'Difícil' }
    ];
    
    const questionTypes = [
      { value: 'multiple_choice', label: 'Múltipla Escolha' },
      { value: 'true_false', label: 'Verdadeiro/Falso' },
      { value: 'open_ended', label: 'Dissertativa' },
      { value: 'matching', label: 'Correspondência' },
      { value: 'fill_in', label: 'Preencher Lacunas' }
    ];
    
    const selectedLevelLabel = computed(() => {
      return levels.find(l => l.value === selectedLevel.value)?.label || '';
    });
    
    const toggleQuestionType = (type: string) => {
      if (selectedQuestionTypes.value.includes(type)) {
        selectedQuestionTypes.value = selectedQuestionTypes.value.filter(t => t !== type);
      } else {
        selectedQuestionTypes.value.push(type);
      }
    };
    
    const generateQuestions = async () => {
      if (!subject.value || !topics.value) return;
      
      isGenerating.value = true;
      questions.value = [];
      
      // Simulação de chamada à API de IA
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Gerar questões de exemplo
      const generatedQuestions: Question[] = [];
      const topicList = topics.value.split(',').map(t => t.trim());
      
      for (let i = 0; i < questionCount.value; i++) {
        const topic = topicList[i % topicList.length];
        const type = selectedQuestionTypes.value[i % selectedQuestionTypes.value.length];
        
        let question: Question = { text: '', type };
        
        switch (type) {
          case 'multiple_choice':
            question.text = `Sobre ${topic}, qual das alternativas abaixo está correta?`;
            question.options = [
              'Alternativa A: Lorem ipsum dolor sit amet',
              'Alternativa B: Consectetur adipiscing elit',
              'Alternativa C: Sed do eiusmod tempor incididunt',
              'Alternativa D: Ut labore et dolore magna aliqua'
            ];
            break;
          case 'true_false':
            question.text = `Verdadeiro ou Falso: ${topic} é um tema importante no contexto atual.`;
            break;
          case 'open_ended':
            question.text = `Explique detalhadamente como ${topic} influencia na sociedade contemporânea.`;
            break;
          case 'matching':
            question.text = `Relacione os conceitos sobre ${topic} com suas definições:`;
            // Implementar opções de correspondência
            break;
          case 'fill_in':
            question.text = `Complete a lacuna: A principal característica de ${topic} é __________.`;
            break;
          default:
            question.text = `Questão sobre ${topic}: Descreva os principais aspectos.`;
        }
        
        generatedQuestions.push(question);
      }
      
      questions.value = generatedQuestions;
      isGenerating.value = false;
    };
    
    const saveExam = () => {
      console.log('Prova salva:', questions.value);
      // Lógica para salvar no backend
    };

    return {
      subject,
      topics,
      selectedLevel,
      questionCount,
      selectedQuestionTypes,
      questions,
      isGenerating,
      levels,
      questionTypes,
      selectedLevelLabel,
      toggleQuestionType,
      generateQuestions,
      saveExam
    };
  }
});
</script>

<style scoped>
.glass-card {
  background: rgba(32, 32, 54, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.glass-card-inner {
  background: rgba(25, 25, 40, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.question {
  transition: all 0.3s ease;
}

.question:hover {
  background: rgba(50, 40, 70, 0.4);
  border-radius: 0.5rem;
}
</style>