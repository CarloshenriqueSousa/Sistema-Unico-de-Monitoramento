<template>
  <div class="map2d-root">
    <div class="canvas-wrapper" ref="wrapperRef">
      <canvas ref="canvasRef" :width="canvasWidth" :height="canvasHeight"></canvas>
      <div class="legend">
        <div class="legend-item">
          <span class="swatch swatch-student"></span>
          <span>Aluno</span>
        </div>
        <div class="legend-item">
          <span class="swatch swatch-teacher"></span>
          <span>Professor</span>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, computed } from 'vue'

type GroupMode = 'single' | 'duo' | 'trio'

const props = defineProps<{
  rows: number
  cols: number
  groupMode: GroupMode
  seatSize?: number
  spacing?: number
  snapToGrid?: boolean
  // advanced layout
  rowsConfig?: number[] // per-row seat counts overrides
  teacherArea?: 'left'|'center'|'right'|'hidden'
  teacherLabel?: string
  backgroundColor?: string
  alternateColors?: boolean
  showNumbers?: boolean
  showBorders?: boolean
  // students list
  students?: Array<{ name: string; list?: string }>
  // edit permissions
  editable?: boolean
  // furniture/objects in room
  objects?: Array<{ id: string; type: 'locker'|'computer'|'desk'|'custom'; x: number; y: number; w: number; h: number; label?: string }>
}>()

const emit = defineEmits<{
  (e: 'update:teacher', pos: { x: number; y: number }): void
  (e: 'update:seats', seats: Array<{ id: string; x: number; y: number; label?: string; status?: string }>): void
}>()

const wrapperRef = ref<HTMLDivElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const ctx = ref<CanvasRenderingContext2D | null>(null)

const canvasWidth = 900
const canvasHeight = 520

const seatSize = computed(() => props.seatSize ?? 34)
const spacing = computed(() => props.spacing ?? 18)

type Seat = { id: string; x: number; y: number; w: number; h: number; label?: string; status?: 'ok'|'reservado'|'indisponivel' }
const seats = ref<Seat[]>([])
const teacher = ref<{ x: number; y: number; w: number; h: number }>({ x: 24, y: 24, w: 42, h: 42 })
type Furniture = { id: string; type: 'locker'|'computer'|'desk'|'custom'; x: number; y: number; w: number; h: number; label?: string }
const furniture = ref<Furniture[]>([])

const backgroundColor = ref(props.backgroundColor ?? '#ffffff')
const borderColor = 'rgba(23,24,30,0.1)'
const gridMinor = 'rgba(23,24,30,0.03)'
const seatColor = '#0f1e3f'
const seatAccent = '#2d531a'
const teacherColor = '#d97706'

let dragging: null | { type: 'seat' | 'teacher'; index: number; offsetX: number; offsetY: number } = null
let selection: number[] = []
let boxSelect: null | { x: number; y: number; w: number; h: number } = null

const buildLayout = () => {
  const s = seatSize.value
  const p = spacing.value
  const rowCounts = props.rowsConfig && props.rowsConfig.length ? props.rowsConfig : Array.from({ length: props.rows }, () => props.cols)
  const maxCols = Math.max(0, ...rowCounts)
  const totalW = maxCols * s + Math.max(0, maxCols - 1) * p
  const totalH = rowCounts.length * s + Math.max(0, rowCounts.length - 1) * p
  const originX = Math.round((canvasWidth - totalW) / 2)
  const originY = Math.round((canvasHeight - totalH) / 2)
  const newSeats: Seat[] = []
  let idCounter = 1

  for (let r = 0; r < rowCounts.length; r++) {
    const colsInRow = rowCounts[r]
    for (let c = 0; c < colsInRow; c++) {
      const baseX = originX + c * (s + p)
      const baseY = originY + r * (s + p)
      if (props.groupMode === 'single') {
        newSeats.push({ id: `${idCounter++}`, x: baseX, y: baseY, w: s, h: s })
      } else if (props.groupMode === 'duo') {
        const gap = Math.max(6, Math.floor(s * 0.15))
        newSeats.push({ id: `${idCounter++}a`, x: baseX - Math.floor((gap + s) / 2), y: baseY, w: s, h: s })
        newSeats.push({ id: `${idCounter++}b`, x: baseX + Math.floor((gap + s) / 2), y: baseY, w: s, h: s })
      } else {
        const gap = Math.max(6, Math.floor(s * 0.12))
        newSeats.push({ id: `${idCounter++}a`, x: baseX - (s + gap), y: baseY, w: s, h: s })
        newSeats.push({ id: `${idCounter++}b`, x: baseX, y: baseY, w: s, h: s })
        newSeats.push({ id: `${idCounter++}c`, x: baseX + (s + gap), y: baseY, w: s, h: s })
      }
    }
  }
  seats.value = newSeats.map((s, i) => ({ ...s, label: String(i+1), status: 'ok' }))
  emit('update:seats', seats.value.map(s => ({ id: s.id, x: s.x, y: s.y })))
}

const drawGrid = (c: CanvasRenderingContext2D) => {
  c.save()
  c.clearRect(0, 0, canvasWidth, canvasHeight)
  c.fillStyle = backgroundColor.value
  c.fillRect(0, 0, canvasWidth, canvasHeight)
  // minor grid
  c.strokeStyle = gridMinor
  c.lineWidth = 1
  for (let x = 0; x < canvasWidth; x += 16) {
    c.beginPath(); c.moveTo(x, 0); c.lineTo(x, canvasHeight); c.stroke()
  }
  for (let y = 0; y < canvasHeight; y += 16) {
    c.beginPath(); c.moveTo(0, y); c.lineTo(canvasWidth, y); c.stroke()
  }
  // border
  c.strokeStyle = borderColor
  c.lineWidth = 2
  c.strokeRect(0.5, 0.5, canvasWidth - 1, canvasHeight - 1)
  c.restore()
}

const drawSeat = (c: CanvasRenderingContext2D, s: Seat, hovered: boolean, selected: boolean, index: number) => {
  c.save()
  const alt = !!props.alternateColors && (index % 2 === 0)
  c.fillStyle = hovered || selected ? seatAccent : (alt ? '#123057' : seatColor)
  c.strokeStyle = props.showBorders === false ? 'transparent' : 'rgba(23,24,30,0.15)'
  c.lineWidth = props.showBorders === false ? 0 : 1
  const r = 6
  roundRect(c, s.x, s.y, s.w, s.h, r)
  c.fill()
  if (c.lineWidth > 0) c.stroke()
  // small label
  if (props.showNumbers !== false) {
    c.fillStyle = '#ffffff'
    c.font = 'bold 10px system-ui'
    c.textAlign = 'center'
    c.textBaseline = 'middle'
    c.fillText(s.label ?? String(index+1), s.x + s.w / 2, s.y + s.h / 2)
  }
  c.restore()
}

const drawTeacher = (c: CanvasRenderingContext2D, hovered: boolean) => {
  if (props.teacherArea === 'hidden') return
  const t = teacher.value
  c.save()
  c.fillStyle = hovered ? '#b45309' : teacherColor
  c.strokeStyle = 'rgba(23,24,30,0.18)'
  c.lineWidth = 1.5
  roundRect(c, t.x, t.y, t.w, t.h, 8)
  c.fill(); c.stroke()
  c.fillStyle = '#ffffff'
  c.font = 'bold 11px system-ui'
  c.textAlign = 'center'
  c.textBaseline = 'middle'
  c.fillText(props.teacherLabel || 'Prof', t.x + t.w / 2, t.y + t.h / 2)
  c.restore()
}

const drawFurniture = (c: CanvasRenderingContext2D, f: Furniture, hovered: boolean, selected: boolean) => {
  c.save()
  let color = '#64748b' // default
  if (f.type === 'locker') color = '#6b7280'
  if (f.type === 'computer') color = '#0ea5e9'
  if (f.type === 'desk') color = '#92400e'
  c.fillStyle = hovered || selected ? 'rgba(59,130,246,0.8)' : color
  c.strokeStyle = 'rgba(23,24,30,0.2)'
  c.lineWidth = 1
  roundRect(c, f.x, f.y, f.w, f.h, 8)
  c.fill(); c.stroke()
  if (f.label) {
    c.fillStyle = '#ffffff'
    c.font = 'bold 11px system-ui'
    c.textAlign = 'center'
    c.textBaseline = 'middle'
    c.fillText(f.label, f.x + f.w/2, f.y + f.h/2)
  }
  c.restore()
}

const isInside = (px: number, py: number, r: { x: number; y: number; w: number; h: number }) => (
  px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h
)

const snap = (val: number) => {
  if (!props.snapToGrid) return val
  const step = 8
  return Math.round(val / step) * step
}

const render = () => {
  if (!ctx.value) return
  const c = ctx.value
  drawGrid(c)
  const hover = currentHover()
  seats.value.forEach((s, i) => drawSeat(c, s, !!(hover && hover.type === 'seat' && hover.index === i), selection.includes(i), i))
  // furniture first (below seats)
  furniture.value.forEach((f, i) => drawFurniture(c, f, !!(hover && hover.type === 'object' && hover.index === i), false))
  drawTeacher(c, hover?.type === 'teacher')
  if (boxSelect) {
    c.save()
    c.strokeStyle = 'rgba(59,130,246,0.9)'
    c.setLineDash([5,3])
    c.lineWidth = 1.5
    c.strokeRect(boxSelect.x, boxSelect.y, boxSelect.w, boxSelect.h)
    c.restore()
  }
}

const currentHover = (): null | { type: 'seat' | 'teacher' | 'object'; index: number } => {
  if (!mouse) return null
  const t = teacher.value
  if (isInside(mouse.x, mouse.y, t)) return { type: 'teacher', index: 0 }
  for (let i = furniture.value.length - 1; i >= 0; i--) {
    const f = furniture.value[i]
    if (isInside(mouse.x, mouse.y, f)) return { type: 'object', index: i }
  }
  for (let i = seats.value.length - 1; i >= 0; i--) {
    if (isInside(mouse.x, mouse.y, seats.value[i])) return { type: 'seat', index: i }
  }
  return null
}

const mouse = { x: 0, y: 0, down: false }
const onMouseMove = (e: MouseEvent) => {
  const rect = canvasRef.value!.getBoundingClientRect()
  mouse.x = e.clientX - rect.left
  mouse.y = e.clientY - rect.top
  // update cursor
  const h = currentHover()
  if (canvasRef.value) {
    canvasRef.value.style.cursor = h ? 'pointer' : 'default'
  }
  if (dragging) {
    if (props.editable === false) { dragging = null; return }
    if (dragging.type === 'teacher') {
      // bound within canvas
      const nx = snap(mouse.x - dragging.offsetX)
      const ny = snap(mouse.y - dragging.offsetY)
      teacher.value.x = clamp(nx, 0, canvasWidth - teacher.value.w)
      teacher.value.y = clamp(ny, 0, canvasHeight - teacher.value.h)
      emit('update:teacher', { x: teacher.value.x, y: teacher.value.y })
    } else if (dragging.type === 'seat') {
      const s = seats.value[dragging.index]
      const nx = snap(mouse.x - dragging.offsetX)
      const ny = snap(mouse.y - dragging.offsetY)
      s.x = clamp(nx, 0, canvasWidth - s.w)
      s.y = clamp(ny, 0, canvasHeight - s.h)
      emit('update:seats', seats.value.map(se => ({ id: se.id, x: se.x, y: se.y, label: se.label, status: se.status })))
    } else if (dragging.type === 'object') {
      const f = furniture.value[dragging.index]
      const nx = snap(mouse.x - dragging.offsetX)
      const ny = snap(mouse.y - dragging.offsetY)
      f.x = clamp(nx, 0, canvasWidth - f.w)
      f.y = clamp(ny, 0, canvasHeight - f.h)
      emit('update:seats', seats.value.map(se => ({ id: se.id, x: se.x, y: se.y, label: se.label, status: se.status })))
    }
  }
  render()
}

const onMouseDown = (e: MouseEvent) => {
  onMouseMove(e)
  if (props.editable === false) return
  const hover = currentHover()
  mouse.down = true
  if (hover) {
    if (hover.type === 'teacher') {
      dragging = { type: 'teacher', index: 0, offsetX: mouse.x - teacher.value.x, offsetY: mouse.y - teacher.value.y }
    } else if (hover.type === 'seat') {
      // manage selection
      if (!selection.includes(hover.index)) {
        if (!isShift(e)) selection = []
        selection.push(hover.index)
      }
      const s = seats.value[hover.index]
      dragging = { type: 'seat', index: hover.index, offsetX: mouse.x - s.x, offsetY: mouse.y - s.y }
    } else if (hover.type === 'object') {
      const f = furniture.value[hover.index]
      dragging = { type: 'object', index: hover.index, offsetX: mouse.x - f.x, offsetY: mouse.y - f.y }
    }
  } else {
    // start box selection
    if (!isShift(e)) selection = []
    boxSelect = { x: mouse.x, y: mouse.y, w: 0, h: 0 }
  }
}

const onMouseUp = () => {
  mouse.down = false
  dragging = null
  if (boxSelect) {
    const rect = normalizeRect(boxSelect)
    seats.value.forEach((s, i) => {
      if (rectsOverlap(rect, { x: s.x, y: s.y, w: s.w, h: s.h })) {
        if (!selection.includes(i)) selection.push(i)
      }
    })
    boxSelect = null
  }
  render()
}

const onResize = () => {
  // Canvas has fixed pixels to keep scaling crisp; wrapper handles responsiveness via CSS.
  render()
}

// Utilities
const isShift = (e: MouseEvent) => e.shiftKey
const normalizeRect = (r: { x: number; y: number; w: number; h: number }) => ({
  x: Math.min(r.x, r.x + r.w),
  y: Math.min(r.y, r.y + r.h),
  w: Math.abs(r.w),
  h: Math.abs(r.h)
})
const rectsOverlap = (a: { x: number; y: number; w: number; h: number }, b: { x: number; y: number; w: number; h: number }) => (
  a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y
)
const clamp = (v:number, min:number, max:number) => Math.min(max, Math.max(min, v))

const onKeyDown = (e: KeyboardEvent) => {
  if (props.editable === false) return
  if (e.key === 'Delete' || e.key === 'Backspace') {
    if (selection.length) {
      seats.value = seats.value.filter((_, idx) => !selection.includes(idx))
      selection = []
      emit('update:seats', seats.value.map(s => ({ id: s.id, x: s.x, y: s.y, label: s.label, status: s.status })))
      render()
    }
  }
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const context = canvas.getContext('2d')
  if (!context) return
  ctx.value = context
  buildLayout()
  // load furniture from props
  furniture.value = Array.isArray(props.objects) ? props.objects.map(o => ({ ...o })) : []
  render()
  canvas.addEventListener('mousemove', onMouseMove)
  canvas.addEventListener('mousedown', onMouseDown)
  window.addEventListener('mouseup', onMouseUp)
  window.addEventListener('resize', onResize)
  window.addEventListener('keydown', onKeyDown)
})

onUnmounted(() => {
  const canvas = canvasRef.value
  if (canvas) {
    canvas.removeEventListener('mousemove', onMouseMove)
    canvas.removeEventListener('mousedown', onMouseDown)
  }
  window.removeEventListener('mouseup', onMouseUp)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('keydown', onKeyDown)
})

watch(() => [props.rows, props.cols, props.groupMode, seatSize.value, spacing.value], () => {
  buildLayout()
  render()
})
// react to objects changes
watch(() => props.objects, (v) => {
  furniture.value = Array.isArray(v) ? v.map(x => ({ ...x })) : []
  render()
}, { deep: true })


// react to prop changes for visuals and teacher area
watch(() => props.backgroundColor, (v) => { if (v) { backgroundColor.value = v; render() } })
watch(() => props.teacherLabel, () => render())
watch(() => props.teacherArea, (pos) => {
  if (!pos || pos === 'hidden') { render(); return }
  // anchor teacher near top based on position
  const t = teacher.value
  const margin = 8
  t.y = margin
  if (pos === 'left') t.x = margin
  if (pos === 'center') t.x = Math.round((canvasWidth - t.w) / 2)
  if (pos === 'right') t.x = canvasWidth - t.w - margin
  emit('update:teacher', { x: t.x, y: t.y })
  render()
})

function roundRect(c: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
  const rr = Math.min(r, w / 2, h / 2)
  c.beginPath()
  c.moveTo(x + rr, y)
  c.lineTo(x + w - rr, y)
  c.quadraticCurveTo(x + w, y, x + w, y + rr)
  c.lineTo(x + w, y + h - rr)
  c.quadraticCurveTo(x + w, y + h, x + w - rr, y + h)
  c.lineTo(x + rr, y + h)
  c.quadraticCurveTo(x, y + h, x, y + h - rr)
  c.lineTo(x, y + rr)
  c.quadraticCurveTo(x, y, x + rr, y)
  c.closePath()
}

// Exposed API for parent (toolbar actions)
function rotateSelection() {
  if (!selection.length) return
  const selectedSeats = selection.map(i => seats.value[i])
  const cx = selectedSeats.reduce((a,s)=>a+s.x+s.w/2,0)/selectedSeats.length
  const cy = selectedSeats.reduce((a,s)=>a+s.y+s.h/2,0)/selectedSeats.length
  selectedSeats.forEach(s => {
    const dx = s.x + s.w/2 - cx
    const dy = s.y + s.h/2 - cy
    // rotate 90 degrees
    const rx = -dy
    const ry = dx
    s.x = Math.round(cx + rx - s.w/2)
    s.y = Math.round(cy + ry - s.h/2)
  })
  render()
}

function deleteSelection() {
  if (!selection.length) return
  seats.value = seats.value.filter((_, idx) => !selection.includes(idx))
  selection = []
  render()
}

function saveLayout() {
  const data = { seats: seats.value, teacher: teacher.value }
  localStorage.setItem('sum-map-layout', JSON.stringify(data))
}

function loadLayout() {
  const raw = localStorage.getItem('sum-map-layout')
  if (!raw) return
  try {
    const data = JSON.parse(raw)
    if (Array.isArray(data.seats) && data.teacher) {
      seats.value = data.seats
      teacher.value = data.teacher
      render()
    }
  } catch {}
}

function exportPng() {
  const canvas = canvasRef.value
  if (!canvas) return
  const url = canvas.toDataURL('image/png')
  const a = document.createElement('a')
  a.href = url
  a.download = 'mapeamento-2d.png'
  a.click()
}

// expose consolidated at end

// Distribution APIs
function distribute(method:'random'|'alpha'|'input'|'mix', rules:any) {
  if (!props.students || props.students.length === 0) return
  let list = [...props.students]
  if (method === 'alpha') list.sort((a,b)=>a.name.localeCompare(b.name))
  if (method === 'random') list.sort(()=>Math.random()-0.5)
  // input: keep order
  if (method === 'mix') list = mixLists(list)
  applyRules(list, rules || {})
  // assign to seats in reading order
  for (let i=0; i<seats.value.length; i++) {
    const s = seats.value[i]
    const stu = list[i]
    s.label = stu ? stu.name : s.label
  }
  render()
}

function mixLists(list:Array<{ name:string; list?:string }>) {
  const groups: Record<string, { name:string; list?:string }[]> = {}
  list.forEach(x => { const k = x.list || 'default'; (groups[k] ||= []).push(x) })
  Object.values(groups).forEach(g => g.sort(()=>Math.random()-0.5))
  const keys = Object.keys(groups)
  const result: typeof list = []
  let added = true
  while (added) {
    added = false
    for (const k of keys) {
      const g = groups[k]
      if (g.length) { result.push(g.shift()!); added = true }
    }
  }
  return result
}

function applyRules(list:Array<{ name:string }>, rules:any) {
  const seatsCount = seats.value.length
  const perRow = props.rowsConfig && props.rowsConfig.length ? props.rowsConfig : Array.from({ length: props.rows }, () => props.cols)
  const rowsTotal = perRow.length
  const rowStartIndices: number[] = []
  {
    let acc = 0
    for (const rc of perRow) { rowStartIndices.push(acc); acc += rc }
  }
  const firstRowThird = Math.ceil(rowsTotal / 3)
  const lastRowThirdStart = Math.max(0, rowsTotal - firstRowThird)
  const byNameIndex = new Map(list.map((s,i)=>[s.name,i]))
  const placeAt = (name:string, seatIndex:number) => {
    const idx = byNameIndex.get(name)
    if (idx === undefined) return
    const target = list.splice(idx,1)[0]
    list.splice(Math.min(seatIndex, list.length), 0, target)
  }
  // First row
  if (Array.isArray(rules.firstRow)) {
    let cursor = 0
    const rows = Math.max(0, firstRowThird)
    for (let r=0; r<rows; r++) {
      const start = rowStartIndices[r] || 0
      const end = start + (perRow[r] || 0)
      for (let i=start; i<end && cursor < rules.firstRow.length; i++) {
        placeAt(rules.firstRow[cursor++], i)
      }
    }
  }
  // Last row
  if (Array.isArray(rules.lastRow)) {
    let cursor = 0
    for (let r=rowsTotal-1; r>=lastRowThirdStart; r--) {
      const start = rowStartIndices[r] || 0
      const end = start + (perRow[r] || 0)
      for (let i=end-1; i>=start && cursor < rules.lastRow.length; i--) {
        placeAt(rules.lastRow[cursor++], i)
      }
    }
  }
  // Distance (basic attempt: ensure not adjacent indices)
  if (Array.isArray(rules.distance)) {
    for (const pair of rules.distance) {
      const [a,b] = pair || []
      const ia = list.findIndex(s=>s.name===a)
      const ib = list.findIndex(s=>s.name===b)
      if (ia<0 || ib<0) continue
      if (Math.abs(ia-ib) < 2) {
        const target = Math.min(seatsCount-1, Math.max(0, ib+3))
        const x = list.splice(ib,1)[0]
        list.splice(target,0,x)
      }
    }
  }
  // Adjacent (try to keep together)
  if (Array.isArray(rules.adjacent)) {
    for (const pair of rules.adjacent) {
      const [a,b] = pair || []
      const ia = list.findIndex(s=>s.name===a)
      const ib = list.findIndex(s=>s.name===b)
      if (ia<0 || ib<0) continue
      if (Math.abs(ia-ib) > 1) {
        const x = list[ib]
        list.splice(ib,1)
        list.splice(Math.min(list.length, ia+1), 0, x)
      }
    }
  }
}

function exportCsv() {
  const rows: string[] = []
  rows.push('index;label;x;y;w;h')
  seats.value.forEach((s, i) => rows.push(`${i+1};${(s.label||'').replace(/;/g,',')};${s.x};${s.y};${s.w};${s.h}`))
  const blob = new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = 'mapeamento-2d.csv'; a.click()
  URL.revokeObjectURL(url)
}

function printMap() {
  const canvas = canvasRef.value
  if (!canvas) return
  const dataUrl = canvas.toDataURL('image/png')
  const win = window.open('', '_blank')
  if (!win) return
  win.document.write(`<img src="${dataUrl}" style="max-width:100%"/>`)
  win.document.close()
  win.focus()
  win.print()
}

function addObject(type:'locker'|'computer'|'desk'|'custom', w=64, h=40, label?:string) {
  if (props.editable === false) return
  const id = `${type}-${Date.now()}`
  const obj: Furniture = { id, type, x: 20, y: 20, w, h, label }
  furniture.value.push(obj)
  render()
}

function removeAllObjects() {
  if (props.editable === false) return
  furniture.value = []
  render()
}

function saveLayout() {
  const data = { seats: seats.value, teacher: teacher.value, furniture: furniture.value }
  localStorage.setItem('sum-map-layout', JSON.stringify(data))
}

function loadLayout() {
  const raw = localStorage.getItem('sum-map-layout')
  if (!raw) return
  try {
    const data = JSON.parse(raw)
    if (Array.isArray(data.seats) && data.teacher) {
      seats.value = data.seats
      teacher.value = data.teacher
      furniture.value = Array.isArray(data.furniture) ? data.furniture : []
      render()
    }
  } catch {}
}

defineExpose({ rotateSelection, deleteSelection, saveLayout, loadLayout, exportPng, exportCsv, printMap, distribute, addObject, removeAllObjects })

</script>

<style scoped>
.map2d-root {
  width: 100%;
}

.canvas-wrapper {
  position: relative;
  width: 100%;
  min-height: 320px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 14px;
  background: #fcfcfc;
  overflow: hidden;
}

canvas {
  width: 100%;
  height: auto;
  display: block;
}

.legend {
  position: absolute;
  bottom: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
  background: rgba(252, 252, 252, 0.85);
  border: 1px solid rgba(23, 24, 30, 0.1);
  backdrop-filter: blur(8px);
  padding: 6px 10px;
  border-radius: 10px;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #17181e;
}

.swatch {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.swatch-student { background: #0f1e3f; }
.swatch-teacher { background: #d97706; }

</style>


