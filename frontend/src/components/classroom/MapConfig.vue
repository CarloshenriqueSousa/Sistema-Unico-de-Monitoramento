<template>
  <div class="config-root">
    <div class="section">
      <h4>Layout de Fileiras</h4>
      <div class="rows">
        <div v-for="(count, idx) in localRows" :key="idx" class="row-item">
          <span class="idx">{{ idx + 1 }}ª</span>
          <input class="num" type="number" min="0" :value="count" @input="onRowChange(idx, ($event.target as HTMLInputElement).valueAsNumber)"/>
          <button class="btn small" @click="removeRow(idx)">Remover</button>
        </div>
      </div>
      <div class="actions">
        <button class="btn" @click="addRow">Adicionar Fileira</button>
      </div>
    </div>

    <div class="section">
      <h4>Área do Professor</h4>
      <div class="row">
        <label>Posição</label>
        <select v-model="localTeacherPos" class="select">
          <option value="left">Esquerda</option>
          <option value="center">Centro</option>
          <option value="right">Direita</option>
          <option value="hidden">Oculto</option>
        </select>
      </div>
      <div class="row">
        <label>Rótulo</label>
        <input class="text" v-model="localTeacherLabel"/>
      </div>
    </div>

    <div class="section">
      <h4>Visual</h4>
      <div class="row">
        <label>Cor de Fundo</label>
        <input class="text" v-model="localBackground" placeholder="#ffffff"/>
      </div>
      <div class="row toggles">
        <label><input type="checkbox" v-model="localAlternate"/> Alternar cores dos assentos</label>
        <label><input type="checkbox" v-model="localShowNumbers"/> Mostrar números</label>
        <label><input type="checkbox" v-model="localShowBorders"/> Mostrar bordas</label>
      </div>
    </div>

    <div class="section">
      <h4>Distribuição de Alunos</h4>
      <div class="row">
        <select v-model="method" class="select">
          <option value="random">Ordem Aleatória</option>
          <option value="alpha">Ordem Alfabética</option>
          <option value="input">Ordem de Entrada</option>
          <option value="mix">Misturar Listas</option>
        </select>
        <button class="btn" @click="$emit('distribute', method)">Aplicar</button>
      </div>
      <div class="rules">
        <h5>Regras Especiais</h5>
        <textarea class="rules-box" v-model="rulesJson" placeholder='{"firstRow":["Ana"], "lastRow":["Bruno"], "distance":[["Carlos","Daniel"]], "adjacent":[["Eva","Fabi"]]}'></textarea>
        <button class="btn" @click="emitRules">Aplicar Regras</button>
      </div>
    </div>

    <div class="section">
      <h4>Dados</h4>
      <div class="row">
        <button class="btn" @click="$emit('save-defaults')">Salvar como Padrão</button>
        <button class="btn" @click="$emit('load-defaults')">Carregar Padrão</button>
        <button class="btn" @click="$emit('reset-layout')">Resetar Layout</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  rows: number[]
  teacherPos: 'left'|'center'|'right'|'hidden'
  teacherLabel: string
  background: string
  alternate: boolean
  showNumbers: boolean
  showBorders: boolean
}>()

const emit = defineEmits<{
  (e:'update:rows', rows:number[]):void
  (e:'update:teacher-pos', pos:'left'|'center'|'right'|'hidden'):void
  (e:'update:teacher-label', label:string):void
  (e:'update:background', color:string):void
  (e:'update:alternate', v:boolean):void
  (e:'update:show-numbers', v:boolean):void
  (e:'update:show-borders', v:boolean):void
  (e:'distribute', method:'random'|'alpha'|'input'|'mix'):void
  (e:'apply-rules', rules:any):void
  (e:'save-defaults'):void
  (e:'load-defaults'):void
  (e:'reset-layout'):void
}>()

const localRows = ref<number[]>([...props.rows])
const localTeacherPos = ref(props.teacherPos)
const localTeacherLabel = ref(props.teacherLabel)
const localBackground = ref(props.background)
const localAlternate = ref(props.alternate)
const localShowNumbers = ref(props.showNumbers)
const localShowBorders = ref(props.showBorders)

const method = ref<'random'|'alpha'|'input'|'mix'>('random')
const rulesJson = ref('')

watch(localRows, v => emit('update:rows', v), { deep:true })
watch(localTeacherPos, v => emit('update:teacher-pos', v))
watch(localTeacherLabel, v => emit('update:teacher-label', v))
watch(localBackground, v => emit('update:background', v))
watch(localAlternate, v => emit('update:alternate', v))
watch(localShowNumbers, v => emit('update:show-numbers', v))
watch(localShowBorders, v => emit('update:show-borders', v))

function onRowChange(idx:number, val:number) {
  const v = Number.isFinite(val) && val >= 0 ? Math.floor(val) : 0
  localRows.value[idx] = v
}
function addRow() { localRows.value.push(0) }
function removeRow(idx:number) { localRows.value.splice(idx,1) }

function emitRules() {
  try { emit('apply-rules', JSON.parse(rulesJson.value || '{}')) } catch {}
}
</script>

<style scoped>
.config-root { display:flex; flex-direction:column; gap:1rem; }
.section { border:1px solid rgba(23,24,30,0.08); border-radius:12px; padding:0.75rem; background:#fcfcfc; }
.section h4 { margin:0 0 0.5rem 0; font-size:0.95rem; color:#17181e; }
.section h5 { margin:0.35rem 0; font-size:0.85rem; color:#17181e; }
.rows { display:flex; flex-direction:column; gap:0.5rem; }
.row-item { display:flex; align-items:center; gap:0.5rem; }
.idx { width:32px; color:#6b6b6b; font-size:0.85rem; }
.num { width:84px; padding:6px 8px; border-radius:8px; border:1px solid rgba(23,24,30,0.12); }
.actions { margin-top:0.5rem; }
.row { display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap; }
.toggles { display:flex; flex-direction:column; align-items:flex-start; gap:0.4rem; }
.select, .text { padding:6px 8px; border:1px solid rgba(23,24,30,0.12); border-radius:8px; }
.rules-box { width:100%; min-height:80px; padding:6px 8px; border:1px solid rgba(23,24,30,0.12); border-radius:8px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.btn { padding:0.45rem 0.8rem; background:#fcfcfc; border:1.5px solid rgba(23,24,30,0.12); border-radius:10px; cursor:pointer; font-size:0.85rem; }
.btn.small { padding:0.3rem 0.6rem; font-size:0.8rem; }
.btn:hover { border-color: rgba(23,24,30,0.25); transform: translateY(-1px); }
</style>
