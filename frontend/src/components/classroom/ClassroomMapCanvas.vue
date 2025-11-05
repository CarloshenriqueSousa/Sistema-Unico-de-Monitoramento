<template>
  <div 
    ref="containerRef"
    class="classroom-canvas-container relative"
    @drop.prevent="handleDrop"
    @dragover.prevent
  >
    <canvas
      ref="canvasRef"
      :width="canvasWidth"
      :height="canvasHeight"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseUp"
    />
    
    <!-- Loading Overlay -->
    <div v-if="loading" class="absolute inset-0 bg-white/50 flex items-center justify-center z-10">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-[#2d531a] border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-sm text-gray-600">Carregando...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import type { MapeamentoConfig, PosicaoAluno, ObjetoSala, Estudante } from '@/types/classroom'

interface Props {
  config: MapeamentoConfig
  positions?: PosicaoAluno[]
  objects?: ObjetoSala[]
  editable?: boolean
  currentTool?: 'select' | 'move'
  zoom?: number
  highlightStudent?: number | null
  mode?: 'demo' | 'student' | 'teacher'
}

const props = withDefaults(defineProps<Props>(), {
  positions: () => [],
  objects: () => [],
  editable: false,
  currentTool: 'select',
  zoom: 1,
  highlightStudent: null,
  mode: 'teacher'
})

const emit = defineEmits<{
  'position-change': [posicao: PosicaoAluno]
  'object-move': [id: string, x: number, y: number]
  'object-select': [obj: ObjetoSala]
  'drop': [linha: number, coluna: number, student: Estudante]
}>()

const containerRef = ref<HTMLDivElement>()
const canvasRef = ref<HTMLCanvasElement>()
const ctx = ref<CanvasRenderingContext2D | null>(null)

const loading = ref(false)
const canvasWidth = 1200
const canvasHeight = 800
const padding = 60

const seatSize = computed(() => {
  const cols = (props.config.fileiras_horizontais || props.config.colunas || 6) * (props.config.alunos_por_grupo || 1)
  return Math.min(50, (canvasWidth - padding * 2) / cols - 10)
})

const spacing = 12

const draggingObject = ref<ObjetoSala | null>(null)
const dragOffset = ref({ x: 0, y: 0 })
const hoveredSeat = ref<{ linha: number; coluna: number } | null>(null)

// Inicialização
onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  ctx.value = canvas.getContext('2d')
  render()
})

// Watch para re-renderizar
watch(() => [props.config, props.positions, props.objects, props.zoom], () => {
  render()
}, { deep: true })

// Renderização
const render = () => {
  if (!ctx.value) return
  
  const c = ctx.value
  
  // Limpa canvas
  c.clearRect(0, 0, canvasWidth, canvasHeight)
  
  // Fundo
  c.fillStyle = props.config.cor_fundo || '#f5f5f5'
  c.fillRect(0, 0, canvasWidth, canvasHeight)
  
  // Grade (se habilitado)
  if (props.config.mostrar_grade) {
    renderGrid(c)
  }
  
  // Objetos da sala
  props.objects.forEach(obj => {
    renderObject(c, obj)
  })
  
  // Assentos e alunos
  renderSeats(c)
}

const renderGrid = (c: CanvasRenderingContext2D) => {
  c.strokeStyle = '#e5e7eb'
  c.lineWidth = 1
  
  const totalCols = (props.config.fileiras_horizontais || props.config.colunas || 6) * (props.config.alunos_por_grupo || 1)
  const totalRows = props.config.fileiras_verticais || props.config.linhas || 5
  
  for (let row = 0; row <= totalRows; row++) {
    const y = padding + row * (seatSize.value + spacing)
    c.beginPath()
    c.moveTo(padding, y)
    c.lineTo(canvasWidth - padding, y)
    c.stroke()
  }
  
  for (let col = 0; col <= totalCols; col++) {
    const x = padding + col * (seatSize.value + spacing)
    c.beginPath()
    c.moveTo(x, padding)
    c.lineTo(x, canvasHeight - padding)
    c.stroke()
  }
}

const renderSeats = (c: CanvasRenderingContext2D) => {
  const totalCols = (props.config.fileiras_horizontais || props.config.colunas || 6) * (props.config.alunos_por_grupo || 1)
  const totalRows = props.config.fileiras_verticais || props.config.linhas || 5
  
  for (let linha = 0; linha < totalRows; linha++) {
    for (let coluna = 0; coluna < totalCols; coluna++) {
      const x = padding + coluna * (seatSize.value + spacing)
      const y = padding + linha * (seatSize.value + spacing)
      
      // Verifica se tem aluno nesta posição
      const position = props.positions.find(
        p => p.linha === linha && p.coluna === coluna
      )
      
      // Determina cor baseado no grupo e no aluno destacado
      let color = '#e5e7eb' // Vazio
      if (position) {
        const isHighlighted = position.estudante_id === props.highlightStudent
        
        if (isHighlighted) {
          color = '#fbbf24' // Amarelo para aluno destacado
        } else if (position.numero_grupo !== null) {
          const groupColors = [
            '#2d531a', '#0f1e3f', '#7c2d12', '#581c87', '#164e63'
          ]
          color = groupColors[position.numero_grupo % groupColors.length]
        } else {
          color = '#2d531a'
        }
        
        // Cores especiais para dificuldades
        if (position.estudante?.dificuldade_visao && position.estudante.dificuldade_visao !== 'NENHUMA') {
          color = '#a855f7' // Roxo para dificuldade visual
        }
        
        if (position.estudante?.eh_lider) {
          color = '#f59e0b' // Laranja para líder
        }
      }
      
      // Hover effect
      if (hoveredSeat.value?.linha === linha && hoveredSeat.value?.coluna === coluna && props.editable) {
        color = '#fbbf24'
      }
      
      // Desenha assento
      c.fillStyle = color
      c.fillRect(x, y, seatSize.value, seatSize.value)
      
      // Borda
      c.strokeStyle = position ? '#ffffff' : '#d1d5db'
      c.lineWidth = position ? 3 : 2
      c.strokeRect(x, y, seatSize.value, seatSize.value)
      
      // Número (se habilitado)
      if (props.config.mostrar_numeros) {
        c.fillStyle = position ? '#ffffff' : '#6b7280'
        c.font = '12px Arial'
        c.textAlign = 'center'
        c.textBaseline = 'middle'
        const num = linha * totalCols + coluna + 1
        c.fillText(num.toString(), x + seatSize.value / 2, y + seatSize.value / 2)
      }
      
      // Iniciais do aluno (se posicionado)
      if (position && position.estudante) {
        c.fillStyle = '#ffffff'
        c.font = 'bold 14px Arial'
        c.textAlign = 'center'
        c.textBaseline = 'middle'
        const initials = getInitials(position.estudante.usuario?.nome || '')
        c.fillText(initials, x + seatSize.value / 2, y + seatSize.value / 2)
      }
    }
  }
}

const renderObject = (c: CanvasRenderingContext2D, obj: ObjetoSala) => {
  c.save()
  
  // Aplica rotação
  const centerX = obj.x + obj.width / 2
  const centerY = obj.y + obj.height / 2
  c.translate(centerX, centerY)
  c.rotate((obj.rotacao * Math.PI) / 180)
  c.translate(-centerX, -centerY)
  
  // Desenha objeto baseado no tipo
  switch (obj.tipo) {
    case 'cadeira_professor':
    case 'mesa_professor':
      c.fillStyle = obj.cor || '#d97706'
      c.fillRect(obj.x, obj.y, obj.width, obj.height)
      c.strokeStyle = '#92400e'
      c.lineWidth = 3
      c.strokeRect(obj.x, obj.y, obj.width, obj.height)
      break
      
    case 'armario':
      c.fillStyle = '#4b5563'
      c.fillRect(obj.x, obj.y, obj.width, obj.height)
      c.strokeStyle = '#1f2937'
      c.lineWidth = 2
      c.strokeRect(obj.x, obj.y, obj.width, obj.height)
      // Portas
      c.strokeStyle = '#9ca3af'
      c.beginPath()
      c.moveTo(obj.x + obj.width / 2, obj.y)
      c.lineTo(obj.x + obj.width / 2, obj.y + obj.height)
      c.stroke()
      break
      
    case 'computador':
      // Monitor
      c.fillStyle = '#1f2937'
      c.fillRect(obj.x, obj.y, obj.width * 0.8, obj.height * 0.7)
      c.strokeStyle = '#9ca3af'
      c.strokeRect(obj.x, obj.y, obj.width * 0.8, obj.height * 0.7)
      // Base
      c.fillStyle = '#4b5563'
      c.fillRect(obj.x + obj.width * 0.3, obj.y + obj.height * 0.7, obj.width * 0.2, obj.height * 0.3)
      break
      
    case 'quadro':
      c.fillStyle = '#1e293b'
      c.fillRect(obj.x, obj.y, obj.width, obj.height)
      c.strokeStyle = '#94a3b8'
      c.lineWidth = 4
      c.strokeRect(obj.x, obj.y, obj.width, obj.height)
      break
      
    case 'estante':
      c.fillStyle = '#78350f'
      c.fillRect(obj.x, obj.y, obj.width, obj.height)
      // Prateleiras
      const shelves = 4
      c.strokeStyle = '#451a03'
      c.lineWidth = 2
      for (let i = 1; i < shelves; i++) {
        const y = obj.y + (obj.height / shelves) * i
        c.beginPath()
        c.moveTo(obj.x, y)
        c.lineTo(obj.x + obj.width, y)
        c.stroke()
      }
      break
      
    default:
      c.fillStyle = obj.cor || '#64748b'
      c.fillRect(obj.x, obj.y, obj.width, obj.height)
  }
  
  // Label
  if (obj.label) {
    c.fillStyle = '#ffffff'
    c.font = 'bold 12px Arial'
    c.textAlign = 'center'
    c.textBaseline = 'middle'
    c.fillText(obj.label, obj.x + obj.width / 2, obj.y + obj.height / 2)
  }
  
  // Borda de seleção
  if (obj.selected) {
    c.strokeStyle = '#fbbf24'
    c.lineWidth = 3
    c.strokeRect(obj.x - 2, obj.y - 2, obj.width + 4, obj.height + 4)
  }
  
  c.restore()
}

// Drag and Drop de Alunos
const handleDrop = (event: DragEvent) => {
  if (!props.editable) return
  
  const canvas = canvasRef.value
  if (!canvas) return
  
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // Converte coordenadas para linha/coluna
  const totalCols = (props.config.fileiras_horizontais || props.config.colunas || 6) * (props.config.alunos_por_grupo || 1)
  const coluna = Math.floor((x - padding) / (seatSize.value + spacing))
  const linha = Math.floor((y - padding) / (seatSize.value + spacing))
  
  // Valida posição
  if (
    linha >= 0 &&
    linha < (props.config.fileiras_verticais || props.config.linhas || 5) &&
    coluna >= 0 &&
    coluna < totalCols
  ) {
    // Verifica se já tem aluno
    const existente = props.positions.find(
      p => p.linha === linha && p.coluna === coluna
    )
    
    if (!existente) {
      const studentData = event.dataTransfer?.getData('student')
      if (studentData) {
        const estudante: Estudante = JSON.parse(studentData)
        emit('drop', linha, coluna, estudante)
      }
    }
  }
}

// Mouse Events para Objetos
const handleMouseDown = (event: MouseEvent) => {
  if (!props.editable || props.currentTool !== 'move') return
  
  const canvas = canvasRef.value
  if (!canvas) return
  
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // Verifica se clicou em algum objeto
  for (let i = props.objects.length - 1; i >= 0; i--) {
    const obj = props.objects[i]
    if (
      x >= obj.x &&
      x <= obj.x + obj.width &&
      y >= obj.y &&
      y <= obj.y + obj.height
    ) {
      draggingObject.value = obj
      dragOffset.value = {
        x: x - obj.x,
        y: y - obj.y
      }
      emit('object-select', obj)
      break
    }
  }
}

const handleMouseMove = (event: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // Drag de objeto
  if (draggingObject.value) {
    const newX = Math.max(0, Math.min(canvasWidth - draggingObject.value.width, x - dragOffset.value.x))
    const newY = Math.max(0, Math.min(canvasHeight - draggingObject.value.height, y - dragOffset.value.y))
    
    emit('object-move', draggingObject.value.id, newX, newY)
    return
  }
  
  // Hover sobre assentos
  if (props.editable) {
    const totalCols = (props.config.fileiras_horizontais || props.config.colunas || 6) * (props.config.alunos_por_grupo || 1)
    const coluna = Math.floor((x - padding) / (seatSize.value + spacing))
    const linha = Math.floor((y - padding) / (seatSize.value + spacing))
    
    if (
      linha >= 0 &&
      linha < (props.config.fileiras_verticais || props.config.linhas || 5) &&
      coluna >= 0 &&
      coluna < totalCols
    ) {
      hoveredSeat.value = { linha, coluna }
    } else {
      hoveredSeat.value = null
    }
    render()
  }
}

const handleMouseUp = () => {
  draggingObject.value = null
}

// Utilitários
const getInitials = (nome: string) => {
  if (!nome) return ''
  return nome.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

// Expose métodos
defineExpose({
  render,
  exportPNG: () => {
    return canvasRef.value?.toDataURL('image/png')
  }
})
</script>

<style scoped>
.classroom-canvas-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

canvas {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: white;
  cursor: crosshair;
  max-width: 100%;
  height: auto;
}

canvas:active {
  cursor: grabbing;
}
</style>

