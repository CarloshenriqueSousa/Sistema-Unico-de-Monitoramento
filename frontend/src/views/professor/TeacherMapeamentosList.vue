<template>
  <div class="mapeamentos-list">
    <div class="header">
      <div>
        <h1>Meus Mapeamentos</h1>
        <p>Gerencie os layouts de sala das suas turmas</p>
      </div>
      <button class="btn" @click="novoMapeamento">➕ Novo Mapeamento</button>
    </div>

    <div class="controls">
      <select v-model="turmaFiltro">
        <option value="">Todas as Turmas</option>
        <option v-for="t in turmas" :key="t.id" :value="t.id">{{ t.nome }}</option>
      </select>
      <input v-model="searchQuery" type="text" placeholder="Buscar mapeamento..." />
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>Carregando...</span>
    </div>

    <div v-else class="grid">
      <div v-for="m in mapeamentosFiltrados" :key="m.uuid" class="card" @click="abrir(m.uuid)">
        <div class="preview"><MiniMapPreview :config="m" /></div>
        <div class="content">
          <div class="title">
            <h3>{{ m.nome }}</h3>
            <span v-if="m.ativo" class="badge">Ativo</span>
          </div>
          <div class="meta">
            <span>🏫 {{ m.turma?.nome }}</span>
            <span>📐 {{ m.fileiras_verticais }}x{{ m.fileiras_horizontais }}</span>
            <span>📅 {{ formatDate(m.atualizado_em) }}</span>
          </div>
        </div>
      </div>

      <div v-if="mapeamentosFiltrados.length === 0" class="empty">
        <div>📋</div>
        <h3>Nenhum mapeamento encontrado</h3>
        <button class="btn" @click="novoMapeamento">Criar Mapeamento</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MiniMapPreview from '@/components/classroom/MiniMapPreview.vue'

const router = useRouter()
const loading = ref(true)
const mapeamentos = ref<any[]>([])
const turmas = ref<any[]>([])
const turmaFiltro = ref('')
const searchQuery = ref('')

const mapeamentosFiltrados = computed(() => {
  let data = mapeamentos.value
  if (turmaFiltro.value) data = data.filter(m => String(m.turma?.id) === String(turmaFiltro.value))
  if (searchQuery.value) data = data.filter(m => m.nome?.toLowerCase().includes(searchQuery.value.toLowerCase()))
  return data
})

const carregar = async () => {
  loading.value = true
  try {
    // TODO: substituir por chamadas reais (services/classroomApi)
    turmas.value = []
    mapeamentos.value = []
  } finally {
    loading.value = false
  }
}

const novoMapeamento = () => router.push({ name: 'professor-classroom-editor' })
const abrir = (uuid: string) => router.push({ name: 'professor-classroom-editor', params: { uuid } })
const formatDate = (d: string) => (d ? new Date(d).toLocaleDateString('pt-BR') : '-')

onMounted(carregar)
</script>

<style scoped>
.mapeamentos-list { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem }
.header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem }
.btn { background: #17181c; color: #fff; border: 0; border-radius: 10px; padding: .6rem .9rem; cursor: pointer }
.controls { display: flex; gap: .75rem; margin-bottom: 1rem }
select, input[type="text"] { padding: .6rem .75rem; border: 1px solid #e5e7eb; border-radius: 8px }
.loading { display: flex; gap: .75rem; align-items: center; color: #6b7280 }
.spinner { width: 18px; height: 18px; border: 2px solid #e5e7eb; border-top-color: #2d531a; border-radius: 50%; animation: spin 1s linear infinite }
@keyframes spin { to { transform: rotate(360deg) } }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; cursor: pointer; transition: transform .15s ease, box-shadow .15s ease }
.card:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(0,0,0,.06) }
.preview { height: 160px; background: #f9fafb }
.content { padding: 1rem }
.title { display: flex; justify-content: space-between; align-items: center; margin-bottom: .5rem }
.badge { background: #d1fae5; color: #065f46; border-radius: 9999px; padding: .15rem .5rem; font-size: .75rem; font-weight: 700 }
.meta { display: grid; grid-template-columns: 1fr 1fr; gap: .25rem; color: #6b7280; font-size: .9rem }
.empty { grid-column: 1 / -1; text-align: center; padding: 3rem; color: #6b7280; display: flex; flex-direction: column; gap: .5rem; align-items: center }
</style>

