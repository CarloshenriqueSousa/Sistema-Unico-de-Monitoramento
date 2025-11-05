<template>
  <div class="mini-root">
    <canvas ref="miniRef" :width="w" :height="h"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps<{
  seats: Array<{ x: number; y: number; w: number; h: number }>
  teacher: { x: number; y: number; w: number; h: number }
  sourceSize: { width: number; height: number }
}>()

const w = 220
const h = 140
const miniRef = ref<HTMLCanvasElement | null>(null)

const render = () => {
  const c = miniRef.value?.getContext('2d')
  if (!c) return
  c.clearRect(0,0,w,h)
  // bg
  c.fillStyle = '#ffffff'
  c.fillRect(0,0,w,h)
  c.strokeStyle = 'rgba(23,24,30,0.12)'
  c.strokeRect(0.5,0.5,w-1,h-1)
  const sx = w / props.sourceSize.width
  const sy = h / props.sourceSize.height
  const s = Math.min(sx, sy)
  c.save()
  c.scale(s,s)
  // seats
  c.fillStyle = '#0f1e3f'
  props.seats.forEach(sit => { c.fillRect(sit.x, sit.y, sit.w, sit.h) })
  // teacher
  c.fillStyle = '#d97706'
  c.fillRect(props.teacher.x, props.teacher.y, props.teacher.w, props.teacher.h)
  c.restore()
}

onMounted(() => {
  render()
  window.addEventListener('resize', render)
})
onUnmounted(() => window.removeEventListener('resize', render))
watch(() => [props.seats, props.teacher], render, { deep: true })
</script>

<style scoped>
.mini-root { 
  border: 1px solid rgba(23,24,30,0.08);
  border-radius: 10px;
  background: #fcfcfc;
  overflow: hidden;
}
canvas { display:block; width:100%; height:auto; }
</style>


