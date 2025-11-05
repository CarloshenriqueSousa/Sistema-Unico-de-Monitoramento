<template>
  <div class="chart-wrapper">
    <div v-if="title || $slots.actions" class="chart-header">
      <div class="chart-title-section">
        <h3 v-if="title" class="chart-title">{{ title }}</h3>
        <p v-if="subtitle" class="chart-subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.actions" class="chart-actions">
        <slot name="actions"></slot>
      </div>
    </div>
    
    <div class="chart-controls" v-if="chartTypes.length > 1">
      <button 
        v-for="type in chartTypes" 
        :key="type"
        @click="currentType = type"
        :class="['control-btn', { active: currentType === type }]"
      >
        <svg v-if="type === 'line'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
        <svg v-else-if="type === 'bar'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="18"/>
          <rect x="14" y="8" width="7" height="13"/>
        </svg>
        <svg v-else-if="type === 'pie'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 2v10l6 6"/>
        </svg>
        <span>{{ type }}</span>
      </button>
    </div>
    
    <div class="chart-container" ref="chartContainer">
      <canvas ref="chartCanvas"></canvas>
      
      <div v-if="loading" class="chart-loading">
        <div class="spinner"></div>
        <p>Carregando dados...</p>
      </div>
      
      <div v-if="!loading && (!data || data.datasets?.length === 0)" class="chart-empty">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <line x1="9" y1="9" x2="15" y2="15"/>
          <line x1="15" y1="9" x2="9" y2="15"/>
        </svg>
        <p>Nenhum dado disponível</p>
      </div>
    </div>
    
    <div v-if="showLegend && data?.datasets" class="chart-legend">
      <div 
        v-for="(dataset, index) in data.datasets" 
        :key="index"
        class="legend-item"
        @click="toggleDataset(index)"
        :class="{ 'legend-disabled': hiddenDatasets.includes(index) }"
      >
        <span 
          class="legend-color" 
          :style="{ background: dataset.backgroundColor || dataset.borderColor }"
        ></span>
        <span class="legend-label">{{ dataset.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed, onUnmounted } from 'vue'

interface ChartData {
  labels: string[]
  datasets: Array<{
    label: string
    data: number[]
    backgroundColor?: string | string[]
    borderColor?: string | string[]
    borderWidth?: number
    fill?: boolean
    tension?: number
  }>
}

interface ChartOptions {
  responsive?: boolean
  maintainAspectRatio?: boolean
  aspectRatio?: number
  plugins?: any
  animation?: any
  scales?: any
}

const props = withDefaults(defineProps<{
  data: ChartData
  type?: 'line' | 'bar' | 'pie' | 'doughnut' | 'radar' | 'area' | 'scatter'
  chartTypes?: string[]
  options?: ChartOptions
  title?: string
  subtitle?: string
  showLegend?: boolean
  loading?: boolean
  responsive?: boolean
  animated?: boolean
  realTime?: boolean
  updateInterval?: number
  showTooltip?: boolean
  showGrid?: boolean
  gradientFill?: boolean
}>(), {
  type: 'line',
  chartTypes: () => [],
  options: () => ({}),
  title: '',
  subtitle: '',
  showLegend: true,
  loading: false,
  responsive: true,
  animated: true,
  realTime: false,
  updateInterval: 1000,
  showTooltip: true,
  showGrid: true,
  gradientFill: false
})

const chartCanvas = ref<HTMLCanvasElement | null>(null)
const chartContainer = ref<HTMLElement | null>(null)
const currentType = ref(props.type)
const hiddenDatasets = ref<number[]>([])
const chart = ref<any>(null)
const animationFrame = ref<number | null>(null)
const realTimeInterval = ref<NodeJS.Timeout | null>(null)
const hoveredPoint = ref<{ x: number; y: number; dataset: number; index: number } | null>(null)
const isAnimating = ref(false)

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 2,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      enabled: props.showTooltip,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      borderRadius: 8,
      titleFont: {
        size: 14,
        weight: 'bold'
      },
      bodyFont: {
        size: 13
      }
    }
  },
  animation: {
    duration: props.animated ? 750 : 0,
    easing: 'easeInOutQuart'
  },
  scales: props.showGrid ? {
    x: {
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.1)'
      }
    },
    y: {
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.1)'
      }
    }
  } : {
    x: { grid: { display: false } },
    y: { grid: { display: false } }
  }
}

// Computed properties
const chartData = computed(() => {
  if (!props.data?.datasets) return null
  
  return {
    ...props.data,
    datasets: props.data.datasets.map((dataset, index) => ({
      ...dataset,
      hidden: hiddenDatasets.value.includes(index),
      backgroundColor: props.gradientFill ? createGradient(dataset.backgroundColor as string) : dataset.backgroundColor,
      borderColor: dataset.borderColor || dataset.backgroundColor,
      borderWidth: dataset.borderWidth || 2,
      fill: currentType.value === 'area' || dataset.fill,
      tension: dataset.tension || (currentType.value === 'line' ? 0.4 : 0)
    }))
  }
})

const chartOptions = computed(() => ({
  ...defaultOptions,
  ...props.options,
  animation: {
    ...defaultOptions.animation,
    ...props.options.animation,
    duration: props.animated ? (props.options.animation?.duration || 750) : 0
  }
}))

// Lifecycle hooks
onMounted(() => {
  if (props.data && !props.loading) {
    renderChart()
  }
  
  if (props.realTime) {
    startRealTimeUpdates()
  }
  
  setupCanvasEvents()
})

onUnmounted(() => {
  stopRealTimeUpdates()
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value)
  }
})

// Watchers
watch(() => props.data, () => {
  if (!props.loading) {
    renderChart()
  }
}, { deep: true })

watch(() => props.loading, (newVal) => {
  if (!newVal && props.data) {
    nextTick(() => renderChart())
  }
})

watch(currentType, () => {
  renderChart()
})

watch(() => props.realTime, (newVal) => {
  if (newVal) {
    startRealTimeUpdates()
  } else {
    stopRealTimeUpdates()
  }
})

// Helper functions
const createGradient = (color: string) => {
  if (!chartCanvas.value) return color
  
  const ctx = chartCanvas.value.getContext('2d')
  const gradient = ctx.createLinearGradient(0, 0, 0, chartCanvas.value.height)
  gradient.addColorStop(0, color + '80')
  gradient.addColorStop(1, color + '20')
  return gradient
}

const setupCanvasEvents = () => {
  if (!chartCanvas.value) return
  
  chartCanvas.value.addEventListener('mousemove', handleMouseMove)
  chartCanvas.value.addEventListener('mouseleave', handleMouseLeave)
  chartCanvas.value.addEventListener('click', handleCanvasClick)
}

const handleMouseMove = (event: MouseEvent) => {
  if (!chartCanvas.value || !props.showTooltip) return
  
  const rect = chartCanvas.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // Find closest data point
  const point = findClosestPoint(x, y)
  hoveredPoint.value = point
}

const handleMouseLeave = () => {
  hoveredPoint.value = null
}

const handleCanvasClick = (event: MouseEvent) => {
  if (!chartCanvas.value) return
  
  const rect = chartCanvas.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  const point = findClosestPoint(x, y)
  if (point) {
    // Emit click event with point data
    emit('point-click', {
      dataset: point.dataset,
      index: point.index,
      value: props.data.datasets[point.dataset].data[point.index],
      label: props.data.labels[point.index]
    })
  }
}

const findClosestPoint = (x: number, y: number) => {
  if (!chartCanvas.value || !props.data?.datasets) return null
  
  const width = chartCanvas.value.width
  const height = chartCanvas.value.height
  const padding = 40
  const graphWidth = width - padding * 2
  const graphHeight = height - padding * 2
  
  let closestPoint = null
  let minDistance = Infinity
  
  props.data.datasets.forEach((dataset, datasetIndex) => {
    if (hiddenDatasets.value.includes(datasetIndex)) return
    
    dataset.data.forEach((value, index) => {
      const pointX = padding + (graphWidth / (dataset.data.length - 1)) * index
      const pointY = height - padding - (value / 100) * graphHeight
      
      const distance = Math.sqrt(Math.pow(x - pointX, 2) + Math.pow(y - pointY, 2))
      
      if (distance < minDistance && distance < 20) {
        minDistance = distance
        closestPoint = { x: pointX, y: pointY, dataset: datasetIndex, index }
      }
    })
  })
  
  return closestPoint
}

const startRealTimeUpdates = () => {
  if (realTimeInterval.value) return
  
  realTimeInterval.value = setInterval(() => {
    if (props.data?.datasets) {
      // Simulate real-time data updates
      props.data.datasets.forEach(dataset => {
        dataset.data = dataset.data.map(value => {
          const change = (Math.random() - 0.5) * 10
          return Math.max(0, Math.min(100, value + change))
        })
      })
      renderChart()
    }
  }, props.updateInterval)
}

const stopRealTimeUpdates = () => {
  if (realTimeInterval.value) {
    clearInterval(realTimeInterval.value)
    realTimeInterval.value = null
  }
}

const emit = defineEmits<{
  'point-click': [data: { dataset: number; index: number; value: number; label: string }]
  'chart-ready': []
}>()

const renderChart = () => {
  if (!chartCanvas.value || props.loading) return
  
  if (isAnimating.value) {
    if (animationFrame.value) {
      cancelAnimationFrame(animationFrame.value)
    }
  }
  
  isAnimating.value = true
  
  const ctx = chartCanvas.value.getContext('2d')
  if (!ctx) return
  
  // Set canvas size
  const containerWidth = chartContainer.value?.clientWidth || 400
  const containerHeight = chartContainer.value?.clientHeight || 300
  
  chartCanvas.value.width = containerWidth * window.devicePixelRatio
  chartCanvas.value.height = containerHeight * window.devicePixelRatio
  
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio)
  chartCanvas.value.style.width = containerWidth + 'px'
  chartCanvas.value.style.height = containerHeight + 'px'
  
  // Clear canvas
  ctx.clearRect(0, 0, containerWidth, containerHeight)
  
  // Render based on chart type
  if (currentType.value === 'line' || currentType.value === 'area') {
    drawLineOrArea(ctx, containerWidth, containerHeight)
  } else if (currentType.value === 'bar') {
    drawBar(ctx, containerWidth, containerHeight)
  } else if (currentType.value === 'pie' || currentType.value === 'doughnut') {
    drawPie(ctx, containerWidth, containerHeight)
  } else if (currentType.value === 'radar') {
    drawRadar(ctx, containerWidth, containerHeight)
  } else if (currentType.value === 'scatter') {
    drawScatter(ctx, containerWidth, containerHeight)
  }
  
  // Draw hovered point
  if (hoveredPoint.value && props.showTooltip) {
    drawHoveredPoint(ctx, hoveredPoint.value)
  }
  
  isAnimating.value = false
  emit('chart-ready')
}

const drawLineOrArea = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const padding = 40
  const graphWidth = width - padding * 2
  const graphHeight = height - padding * 2
  
  // Draw grid
  if (props.showGrid) {
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)'
    ctx.lineWidth = 1
    
    // Vertical grid lines
    for (let i = 0; i <= 5; i++) {
      const x = padding + (graphWidth / 5) * i
      ctx.beginPath()
      ctx.moveTo(x, padding)
      ctx.lineTo(x, height - padding)
      ctx.stroke()
    }
    
    // Horizontal grid lines
    for (let i = 0; i <= 5; i++) {
      const y = padding + (graphHeight / 5) * i
      ctx.beginPath()
      ctx.moveTo(padding, y)
      ctx.lineTo(width - padding, y)
      ctx.stroke()
    }
  }
  
  // Draw axes
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, height - padding)
  ctx.lineTo(width - padding, height - padding)
  ctx.stroke()
  
  if (chartData.value?.datasets) {
    chartData.value.datasets.forEach((dataset, datasetIndex) => {
      if (hiddenDatasets.value.includes(datasetIndex)) return
      
      const data = dataset.data || []
      const color = dataset.borderColor || dataset.backgroundColor || '#667eea'
      
      if (currentType.value === 'line' || currentType.value === 'area') {
        // Draw area fill for area charts
        if (currentType.value === 'area') {
          ctx.fillStyle = props.gradientFill ? createGradient(color) : color + '20'
          ctx.beginPath()
          ctx.moveTo(padding, height - padding)
          
          data.forEach((value, index) => {
            const x = padding + (graphWidth / (data.length - 1)) * index
            const y = height - padding - (value / 100) * graphHeight
            ctx.lineTo(x, y)
          })
          
          ctx.lineTo(width - padding, height - padding)
          ctx.closePath()
          ctx.fill()
        }
        
        // Draw line
        ctx.strokeStyle = color
        ctx.lineWidth = 3
        ctx.beginPath()
        
        data.forEach((value, index) => {
          const x = padding + (graphWidth / (data.length - 1)) * index
          const y = height - padding - (value / 100) * graphHeight
          
          if (index === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        })
        
        ctx.stroke()
        
        // Draw points
        data.forEach((value, index) => {
          const x = padding + (graphWidth / (data.length - 1)) * index
          const y = height - padding - (value / 100) * graphHeight
          
          ctx.fillStyle = color
          ctx.beginPath()
          ctx.arc(x, y, 5, 0, Math.PI * 2)
          ctx.fill()
          
          // Draw point border
          ctx.strokeStyle = '#ffffff'
          ctx.lineWidth = 2
          ctx.stroke()
        })
      }
    })
  }
}

const drawBar = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const padding = 40
  const graphWidth = width - padding * 2
  const graphHeight = height - padding * 2
  
  // Draw grid
  if (props.showGrid) {
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)'
    ctx.lineWidth = 1
    
    // Horizontal grid lines
    for (let i = 0; i <= 5; i++) {
      const y = padding + (graphHeight / 5) * i
      ctx.beginPath()
      ctx.moveTo(padding, y)
      ctx.lineTo(width - padding, y)
      ctx.stroke()
    }
  }
  
  // Draw axes
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, height - padding)
  ctx.lineTo(width - padding, height - padding)
  ctx.stroke()
  
  if (chartData.value?.datasets) {
    const datasetCount = chartData.value.datasets.filter((_, i) => !hiddenDatasets.value.includes(i)).length
    const barWidth = (graphWidth / (chartData.value.labels.length * datasetCount)) * 0.8
    
    chartData.value.datasets.forEach((dataset, datasetIndex) => {
      if (hiddenDatasets.value.includes(datasetIndex)) return
      
      const data = dataset.data || []
      const color = dataset.backgroundColor || dataset.borderColor || '#667eea'
      
      data.forEach((value, index) => {
        const x = padding + (graphWidth / data.length) * index + (datasetIndex * barWidth)
        const barHeight = (value / 100) * graphHeight
        const y = height - padding - barHeight
        
        // Draw bar with gradient
        const gradient = ctx.createLinearGradient(0, y, 0, height - padding)
        gradient.addColorStop(0, color)
        gradient.addColorStop(1, color + '80')
        
        ctx.fillStyle = gradient
        ctx.fillRect(x, y, barWidth, barHeight)
        
        // Draw bar border
        ctx.strokeStyle = color
        ctx.lineWidth = 1
        ctx.strokeRect(x, y, barWidth, barHeight)
      })
    })
  }
}

const drawPie = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const centerX = width / 2
  const centerY = height / 2
  const radius = Math.min(width, height) / 2 - 40
  
  if (chartData.value?.datasets && chartData.value.datasets[0]?.data) {
    const data = chartData.value.datasets[0].data
    const total = data.reduce((sum, val) => sum + val, 0)
    const colors = chartData.value.datasets[0].backgroundColor || [
      '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'
    ]
    
    let startAngle = -Math.PI / 2
    
    data.forEach((value, index) => {
      if (hiddenDatasets.value.includes(index)) return
      
      const sliceAngle = (value / total) * Math.PI * 2
      const color = Array.isArray(colors) ? colors[index] : colors
      
      // Draw slice
      ctx.fillStyle = color
      ctx.beginPath()
      ctx.moveTo(centerX, centerY)
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle)
      ctx.closePath()
      ctx.fill()
      
      // Draw slice border
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = 2
      ctx.stroke()
      
      startAngle += sliceAngle
    })
    
    // Draw hole for doughnut
    if (currentType.value === 'doughnut') {
      ctx.fillStyle = '#ffffff'
      ctx.beginPath()
      ctx.arc(centerX, centerY, radius * 0.6, 0, Math.PI * 2)
      ctx.fill()
    }
  }
}

const drawRadar = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const centerX = width / 2
  const centerY = height / 2
  const radius = Math.min(width, height) / 2 - 60
  
  if (chartData.value?.datasets && chartData.value.datasets[0]?.data) {
    const data = chartData.value.datasets[0].data
    const labels = chartData.value.labels
    const color = chartData.value.datasets[0].borderColor || '#667eea'
    
    // Draw radar grid
    for (let i = 1; i <= 5; i++) {
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.arc(centerX, centerY, (radius / 5) * i, 0, Math.PI * 2)
      ctx.stroke()
    }
    
    // Draw axes
    labels.forEach((_, index) => {
      const angle = (2 * Math.PI / labels.length) * index - Math.PI / 2
      const x = centerX + radius * Math.cos(angle)
      const y = centerY + radius * Math.sin(angle)
      
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)'
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(centerX, centerY)
      ctx.lineTo(x, y)
      ctx.stroke()
    })
    
    // Draw data polygon
    ctx.fillStyle = color + '20'
    ctx.strokeStyle = color
    ctx.lineWidth = 3
    ctx.beginPath()
    
    data.forEach((value, index) => {
      const angle = (2 * Math.PI / data.length) * index - Math.PI / 2
      const x = centerX + (radius * (value / 100)) * Math.cos(angle)
      const y = centerY + (radius * (value / 100)) * Math.sin(angle)
      
      if (index === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    })
    
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
    
    // Draw data points
    data.forEach((value, index) => {
      const angle = (2 * Math.PI / data.length) * index - Math.PI / 2
      const x = centerX + (radius * (value / 100)) * Math.cos(angle)
      const y = centerY + (radius * (value / 100)) * Math.sin(angle)
      
      ctx.fillStyle = color
      ctx.beginPath()
      ctx.arc(x, y, 6, 0, Math.PI * 2)
      ctx.fill()
      
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = 2
      ctx.stroke()
    })
  }
}

const drawScatter = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const padding = 40
  const graphWidth = width - padding * 2
  const graphHeight = height - padding * 2
  
  // Draw grid
  if (props.showGrid) {
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)'
    ctx.lineWidth = 1
    
    for (let i = 0; i <= 5; i++) {
      const x = padding + (graphWidth / 5) * i
      const y = padding + (graphHeight / 5) * i
      
      ctx.beginPath()
      ctx.moveTo(x, padding)
      ctx.lineTo(x, height - padding)
      ctx.stroke()
      
      ctx.beginPath()
      ctx.moveTo(padding, y)
      ctx.lineTo(width - padding, y)
      ctx.stroke()
    }
  }
  
  // Draw axes
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, height - padding)
  ctx.lineTo(width - padding, height - padding)
  ctx.stroke()
  
  if (chartData.value?.datasets) {
    chartData.value.datasets.forEach((dataset, datasetIndex) => {
      if (hiddenDatasets.value.includes(datasetIndex)) return
      
      const data = dataset.data || []
      const color = dataset.backgroundColor || dataset.borderColor || '#667eea'
      
      data.forEach((value, index) => {
        const x = padding + (graphWidth / 100) * value
        const y = height - padding - (graphHeight / 100) * value
        
        ctx.fillStyle = color
        ctx.beginPath()
        ctx.arc(x, y, 8, 0, Math.PI * 2)
        ctx.fill()
        
        ctx.strokeStyle = '#ffffff'
        ctx.lineWidth = 2
        ctx.stroke()
      })
    })
  }
}

const drawHoveredPoint = (ctx: CanvasRenderingContext2D, point: { x: number; y: number; dataset: number; index: number }) => {
  if (!point) return
  
  // Draw highlight circle
  ctx.strokeStyle = '#667eea'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.arc(point.x, point.y, 12, 0, Math.PI * 2)
  ctx.stroke()
  
  // Draw tooltip
  const dataset = props.data.datasets[point.dataset]
  const value = dataset.data[point.index]
  const label = props.data.labels[point.index]
  
  const tooltipText = `${dataset.label}: ${value}`
  const tooltipWidth = tooltipText.length * 8 + 20
  const tooltipHeight = 30
  
  const tooltipX = Math.min(point.x, ctx.canvas.width - tooltipWidth - 10)
  const tooltipY = point.y - tooltipHeight - 20
  
  // Draw tooltip background
  ctx.fillStyle = 'rgba(0, 0, 0, 0.9)'
  ctx.fillRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight)
  
  // Draw tooltip text
  ctx.fillStyle = '#ffffff'
  ctx.font = '12px Arial'
  ctx.textAlign = 'center'
  ctx.fillText(tooltipText, tooltipX + tooltipWidth / 2, tooltipY + tooltipHeight / 2 + 4)
}

const toggleDataset = (index: number) => {
  const idx = hiddenDatasets.value.indexOf(index)
  if (idx > -1) {
    hiddenDatasets.value.splice(idx, 1)
  } else {
    hiddenDatasets.value.push(index)
  }
  renderChart()
}
</script>

<style scoped>
.chart-wrapper {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.chart-title-section {
  flex: 1;
}

.chart-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.chart-subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.chart-actions {
  display: flex;
  gap: 0.5rem;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem;
  background: #f9fafb;
  border-radius: 0.75rem;
  flex-wrap: wrap;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border: 2px solid transparent;
  background: white;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  color: #6b7280;
  text-transform: capitalize;
}

.control-btn:hover {
  background: #f3f4f6;
}

.control-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.control-btn svg {
  width: 20px;
  height: 20px;
}

.chart-container {
  position: relative;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

canvas {
  max-width: 100%;
  height: auto;
}

.chart-loading,
.chart-empty {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #9ca3af;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.legend-item:hover {
  background: #f9fafb;
}

.legend-item.legend-disabled {
  opacity: 0.4;
}

.legend-item.legend-disabled .legend-color {
  background: #d1d5db !important;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 0.25rem;
  flex-shrink: 0;
}

.legend-label {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

@media (max-width: 768px) {
  .chart-wrapper {
    padding: 1rem;
  }
  
  .chart-header {
    flex-direction: column;
  }
  
  .chart-controls {
    overflow-x: auto;
    flex-wrap: nowrap;
  }
}
</style>