<template>
  <div class="mini-map-preview">
    <canvas ref="canvasRef" width="280" height="180" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

const props = defineProps<{ config: any }>()
const canvasRef = ref<HTMLCanvasElement>()

onMounted(() => render())
watch(() => props.config, render, { deep: true })

function render() {
  if (!canvasRef.value || !props.config) return
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')!
  const width = 280, height = 180

  ctx.clearRect(0, 0, width, height)
  ctx.fillStyle = props.config.cor_fundo || '#f5f5f5'
  ctx.fillRect(0, 0, width, height)

  const padding = 16
  const rows = props.config.fileiras_verticais || 5
  const cols = (props.config.fileiras_horizontais || 6) * (props.config.alunos_por_grupo || 1)
  const seatW = Math.min(14, (width - padding * 2) / cols - 2)
  const seatH = Math.min(14, (height - padding * 2) / rows - 2)
  const spacing = 2

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const x = padding + c * (seatW + spacing)
      const y = padding + r * (seatH + spacing)
      ctx.fillStyle = '#2d531a'
      ctx.fillRect(x, y, seatW, seatH)
    }
  }
}
</script>

<style scoped>
.mini-map-preview { width: 100%; height: 180px; display: flex; align-items: center; justify-content: center; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden }
canvas { width: 100%; height: 100%; object-fit: contain }
</style>
