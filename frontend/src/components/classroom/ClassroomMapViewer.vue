<template>
  <div class="classroom-viewer">
    <canvas ref="canvasRef" :width="canvasWidth" :height="canvasHeight" />
    <div v-if="hoveredStudent" class="tooltip" :style="tooltipStyle">
      <div class="avatar">{{ getInitials(hoveredStudent.nome) }}</div>
      <div class="info">
        <strong>{{ hoveredStudent.nome }}</strong>
        <span v-if="hoveredStudent.numero_grupo">Grupo {{ hoveredStudent.numero_grupo }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

type Config = {
  fileiras_verticais: number
  fileiras_horizontais: number
  alunos_por_grupo: number
  cor_fundo?: string
  mostrar_grade?: boolean
  mostrar_numeros?: boolean
  objetos_sala?: Array<{ x:number; y:number; width:number; height:number; rotacao:number; cor?:string; label?:string }>
}

type Position = {
  estudante_id: number
  estudante?: { nome: string }
  linha: number
  coluna: number
  numero_grupo?: number|null
}

const props = defineProps<{ config: Config; positions: Position[]; highlightStudent?: number }>()

const canvasRef = ref<HTMLCanvasElement>()
const canvasWidth = 900
const canvasHeight = 600
const hoveredStudent = ref<{ nome: string } | null>(null)
const tooltipStyle = ref<Record<string, string>>({})

onMounted(() => {
  render()
  canvasRef.value?.addEventListener('mousemove', handleMouseMove)
})

watch(() => [props.config, props.positions], render, { deep: true })

function render() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!

  ctx.clearRect(0, 0, canvasWidth, canvasHeight)
  ctx.fillStyle = props.config.cor_fundo || '#f5f5f5'
  ctx.fillRect(0, 0, canvasWidth, canvasHeight)

  // objetos simples
  props.config.objetos_sala?.forEach(o => {
    ctx.fillStyle = o.cor || '#64748b'
    ctx.fillRect(o.x, o.y, o.width, o.height)
  })

  drawSeats(ctx)
}

function drawSeats(ctx: CanvasRenderingContext2D) {
  const padding = 50
  const seat = 40
  const spacing = 10
  const totalCols = props.config.fileiras_horizontais * (props.config.alunos_por_grupo || 1)
  const totalRows = props.config.fileiras_verticais

  for (let linha = 0; linha < totalRows; linha++) {
    for (let coluna = 0; coluna < totalCols; coluna++) {
      const x = padding + coluna * (seat + spacing)
      const y = padding + linha * (seat + spacing)

      const pos = props.positions.find(p => p.linha === linha && p.coluna === coluna)
      const isCurrent = !!pos && pos.estudante_id === props.highlightStudent
      ctx.fillStyle = isCurrent ? '#fbbf24' : (pos ? '#2d531a' : '#e5e7eb')
      ctx.beginPath()
      roundRect(ctx, x, y, seat, seat, 8)
      ctx.fill()

      ctx.strokeStyle = isCurrent ? '#f59e0b' : '#d1d5db'
      ctx.lineWidth = 2
      ctx.stroke()

      if (props.config.mostrar_numeros) {
        ctx.fillStyle = pos ? '#ffffff' : '#6b7280'
        ctx.font = '12px Arial'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        const num = linha * totalCols + coluna + 1
        ctx.fillText(String(num), x + seat/2, y + seat/2)
      }

      if (pos?.estudante) {
        ctx.fillStyle = '#ffffff'
        ctx.font = 'bold 13px Arial'
        ctx.fillText(getInitials(pos.estudante.nome), x + seat/2, y + seat/2)
      }
    }
  }
}

function handleMouseMove(e: MouseEvent) {
  const canvas = canvasRef.value!
  const rect = canvas.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top

  const padding = 50
  const seat = 40
  const spacing = 10

  let found: { nome: string } | null = null
  props.positions.forEach(pos => {
    const px = padding + pos.coluna * (seat + spacing)
    const py = padding + pos.linha * (seat + spacing)
    if (x >= px && x <= px + seat && y >= py && y <= py + seat) {
      if (pos.estudante) found = pos.estudante
    }
  })
  hoveredStudent.value = found
  if (found) {
    tooltipStyle.value = { left: `${e.clientX + 10}px`, top: `${e.clientY + 10}px` }
  }
}

function getInitials(name: string) {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0,2)
}

function roundRect(ctx: CanvasRenderingContext2D, x:number, y:number, w:number, h:number, r:number) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}
</script>

<style scoped>
.classroom-viewer { position: relative; display: flex; align-items: center; justify-content: center; padding: 1rem }
canvas { border: 1px solid #e5e7eb; border-radius: 8px; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,.04) }
.tooltip { position: fixed; background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: .5rem .75rem; box-shadow: 0 8px 24px rgba(0,0,0,.08); display: flex; gap: .5rem; align-items: center; pointer-events: none; z-index: 1000 }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg,#2d531a,#1a3810); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700 }
.info { display:flex; flex-direction:column; gap:2px; font-size: .85rem }
</style>
