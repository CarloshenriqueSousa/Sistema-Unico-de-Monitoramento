<template>
  <div class="class-management-view">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold">Gerenciamento de Turma</h2>
        <p class="text-gray-400">Sala 1A - 32 alunos</p>
      </div>
      <div class="flex space-x-3">
        <select v-model="selectedClass" class="bg-gray-800 rounded-lg px-3 py-2">
          <option value="1A">1A</option>
          <option value="1B">1B</option>
          <option value="2A">2A</option>
        </select>
        <button class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg transition-colors">
          <i class="fas fa-save mr-2"></i>Salvar Layout
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Editor de Sala -->
      <GlassCard class="lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Layout da Sala de Aula</h3>
          <div class="flex space-x-2">
            <button @click="viewMode = '3d'" :class="viewMode === '3d' ? 'bg-cyan-600' : 'bg-gray-700'" class="px-4 py-2 rounded-lg">
              <i class="fas fa-cube mr-2"></i>3D
            </button>
            <button @click="viewMode = '2d'" :class="viewMode === '2d' ? 'bg-cyan-600' : 'bg-gray-700'" class="px-4 py-2 rounded-lg">
              <i class="fas fa-th mr-2"></i>2D
            </button>
          </div>
        </div>
        
        <div class="classroom-editor-container bg-gray-800/20 rounded-xl p-4 min-h-[500px] grid grid-cols-1 lg:grid-cols-4 gap-4">
          <div class="lg:col-span-1">
            <MapConfig
              :rows="rowsConfig"
              :teacher-pos="teacherPos"
              :teacher-label="teacherLabel"
              :background="background"
              :alternate="alternate"
              :show-numbers="showNumbers"
              :show-borders="showBorders"
              @update:rows="v => rowsConfig = v"
              @update:teacher-pos="v => teacherPos = v"
              @update:teacher-label="v => teacherLabel = v"
              @update:background="v => background = v"
              @update:alternate="v => alternate = v"
              @update:show-numbers="v => showNumbers = v"
              @update:show-borders="v => showBorders = v"
              @distribute="method => mapRef?.distribute(method, rules)"
              @apply-rules="v => { rules = v; }"
              @save-defaults="saveDefaults"
              @load-defaults="loadDefaults"
              @reset-layout="resetLayout"
            />
            <div class="mt-4 space-y-2">
              <h4 class="text-sm font-semibold text-gray-300">Objetos da Sala</h4>
              <div class="grid grid-cols-2 gap-2">
                <button class="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600" @click="addObject('locker')"><i class="fas fa-box mr-2"></i>Armário</button>
                <button class="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600" @click="addObject('computer')"><i class="fas fa-desktop mr-2"></i>Computador</button>
                <button class="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600" @click="addObject('desk')"><i class="fas fa-table mr-2"></i>Mesa</button>
                <button class="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600" @click="addObject('custom')"><i class="fas fa-cube mr-2"></i>Custom</button>
              </div>
              <div class="flex gap-2">
                <button class="flex-1 px-3 py-2 bg-red-700 rounded hover:bg-red-600" @click="removeAllObjects"><i class="fas fa-trash mr-2"></i>Remover Objetos</button>
              </div>
            </div>
            <div class="mt-3 flex gap-2">
              <button class="px-3 py-2 bg-cyan-600 rounded" @click="mapRef?.exportPng()">Exportar PNG</button>
              <button class="px-3 py-2 bg-amber-600 rounded" @click="mapRef?.exportCsv()">Exportar Excel</button>
              <button class="px-3 py-2 bg-gray-700 rounded" @click="mapRef?.printMap()">Imprimir</button>
            </div>
          </div>
          <div class="lg:col-span-3">
            <ClassroomMap2D
              ref="mapRef"
              :rows="rowsConfig.length"
              :cols="Math.max(...rowsConfig, 0)"
              groupMode="single"
              :rowsConfig="rowsConfig"
              :students="studentsForMap"
              :alternateColors="alternate"
              :showNumbers="showNumbers"
              :showBorders="showBorders"
              :backgroundColor="background"
              :teacherArea="teacherPos"
              :teacherLabel="teacherLabel"
              :editable="true"
              :objects="objects"
            />
          </div>
        </div>
      </GlassCard>
      
      <!-- Análise de Alunos -->
      <GlassCard>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Análise de Alunos</h3>
          <button class="bg-purple-600 hover:bg-purple-500 px-4 py-2 rounded-lg transition-colors">
            <i class="fas fa-sync mr-2"></i>Atualizar
          </button>
        </div>
        
        <StudentAnalysisView />
      </GlassCard>
    </div>

    <!-- Lista de Alunos -->
    <GlassCard class="mt-6">
      <h3 class="text-xl font-bold mb-4">Alunos da Turma</h3>
      <DynamicTable 
        :headers="[
          { label: 'Aluno', key: 'name' },
          { label: 'Matemática', key: 'math' },
          { label: 'Linguagens', key: 'language' },
          { label: 'Status', key: 'status' },
          { label: 'Ações', key: 'actions' }
        ]" 
        :items="students"
        class="rounded-xl overflow-hidden"
      >
        <template #row="props">
          <td class="py-3 px-4">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 flex items-center justify-center mr-3">
                <span class="font-bold text-xs">{{ props.item.initials }}</span>
              </div>
              <span>{{ props.item.name }}</span>
            </div>
          </td>
          <td class="py-3 px-4">
            <ProgressRing :progress="props.item.math" :size="40" />
          </td>
          <td class="py-3 px-4">
            <ProgressRing :progress="props.item.language" :size="40" />
          </td>
          <td class="py-3 px-4">
            <span :class="statusClass(props.item.status)">
              {{ props.item.status }}
            </span>
          </td>
          <td class="py-3 px-4">
            <div class="flex space-x-2">
              <button class="text-cyan-400 hover:text-cyan-300">
                <i class="fas fa-eye"></i>
              </button>
              <button class="text-amber-400 hover:text-amber-300">
                <i class="fas fa-edit"></i>
              </button>
            </div>
          </td>
        </template>
      </DynamicTable>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import GlassCard from '@/shared/GlassCard.vue';
import ClassroomMapEditor from '@components/classroom/ClassroomMapEditor.vue';
import ClassroomGridEditor from '@components/classroom/ClassroomGridEditor.vue';
import StudentAnalysisView from '@views/professor/StudentAnalysisView.vue';
import DynamicTable from '@/shared/DynamicTable.vue';
import ProgressRing from '@/shared/ProgressRing.vue';
import MapConfig from '@components/classroom/MapConfig.vue';
import ClassroomMap2D from '@components/classroom/ClassroomMap2D.vue';

export default defineComponent({
  name: 'ClassManagementView',
  components: {
    GlassCard,
    ClassroomMapEditor,
    ClassroomGridEditor,
    StudentAnalysisView,
    DynamicTable,
    ProgressRing
  },
  setup() {
    const selectedClass = ref('1A');
    const viewMode = ref('3d');
    const mapRef = ref<InstanceType<typeof ClassroomMap2D> | null>(null);
    const rowsConfig = ref<number[]>([6,6,6,6,6]);
    const teacherPos = ref<'left'|'center'|'right'|'hidden'>('center');
    const teacherLabel = ref('Prof');
    const background = ref('#f8fafc');
    const alternate = ref(true);
    const showNumbers = ref(true);
    const showBorders = ref(true);
    let rules: any = {};
    
    const students = ref([
      { id: 1, name: 'João Silva', initials: 'JS', math: 85, language: 78, status: 'Ativo' },
      { id: 2, name: 'Maria Oliveira', initials: 'MO', math: 92, language: 88, status: 'Ativo' },
      { id: 3, name: 'Carlos Pereira', initials: 'CP', math: 76, language: 95, status: 'Ativo' },
      { id: 4, name: 'Ana Costa', initials: 'AC', math: 88, language: 82, status: 'Inativo' }
    ]);
    const studentsForMap = computed(() => students.value.map(s => ({ name: s.name })));

    const objects = ref<Array<{ id:string; type:'locker'|'computer'|'desk'|'custom'; x:number; y:number; w:number; h:number; label?:string }>>([])
    const addObject = (type:'locker'|'computer'|'desk'|'custom') => {
      mapRef.value?.addObject?.(type)
      // local mirror: rely on map internal; optional sync if needed later
    }
    const removeAllObjects = () => {
      mapRef.value?.removeAllObjects?.()
      objects.value = []
    }

    const saveDefaults = () => {
      localStorage.setItem('sum-map-defaults', JSON.stringify({ rowsConfig: rowsConfig.value, teacherPos: teacherPos.value, teacherLabel: teacherLabel.value, background: background.value, alternate: alternate.value, showNumbers: showNumbers.value, showBorders: showBorders.value }));
    };
    const loadDefaults = () => {
      const raw = localStorage.getItem('sum-map-defaults');
      if (!raw) return;
      try {
        const data = JSON.parse(raw);
        if (Array.isArray(data.rowsConfig)) rowsConfig.value = data.rowsConfig;
        if (data.teacherPos) teacherPos.value = data.teacherPos;
        if (data.teacherLabel) teacherLabel.value = data.teacherLabel;
        if (data.background) background.value = data.background;
        if (typeof data.alternate === 'boolean') alternate.value = data.alternate;
        if (typeof data.showNumbers === 'boolean') showNumbers.value = data.showNumbers;
        if (typeof data.showBorders === 'boolean') showBorders.value = data.showBorders;
      } catch {}
    };
    const resetLayout = () => { rowsConfig.value = [6,6,6,6,6]; };
    
    const statusClass = (status: 'Ativo' | 'Inativo' | 'Transferido') => {
      const classes: Record<'Ativo' | 'Inativo' | 'Transferido', string> = {
        'Ativo': 'bg-emerald-500/20 text-emerald-400',
        'Inativo': 'bg-amber-500/20 text-amber-400',
        'Transferido': 'bg-gray-500/20 text-gray-400'
      };
      return `px-3 py-1 rounded-full text-xs font-medium ${classes[status]}`;
    };
    
    return {
      selectedClass,
      viewMode,
      mapRef,
      rowsConfig,
      teacherPos,
      teacherLabel,
      background,
      alternate,
      showNumbers,
      showBorders,
      students,
      studentsForMap,
      objects,
      addObject,
      removeAllObjects,
      saveDefaults,
      loadDefaults,
      resetLayout,
      statusClass
    };
  }
});
</script>

<style scoped>
.classroom-editor-container {
  background-image: 
    radial-gradient(circle at center, rgba(139, 92, 246, 0.1) 0%, transparent 70%),
    linear-gradient(to bottom, rgba(30, 30, 40, 0.8), rgba(30, 30, 40, 0.9));
}
</style>