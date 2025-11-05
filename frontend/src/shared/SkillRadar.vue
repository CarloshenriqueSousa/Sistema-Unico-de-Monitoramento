<template>
  <div class="skill-radar-wrapper">
    <div v-if="title" class="radar-header">
      <h3 class="radar-title">{{ title }}</h3>
      <p v-if="subtitle" class="radar-subtitle">{{ subtitle }}</p>
    </div>
    
    <div class="radar-container" ref="radarContainer">
      <svg 
        :width="size" 
        :height="size" 
        :viewBox="`0 0 ${size} ${size}`"
        class="radar-svg"
      >
        <defs>
          <linearGradient id="radarGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:0.8" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <!-- Background circles -->
        <g class="radar-grid">
          <circle 
            v-for="i in levels" 
            :key="`circle-${i}`"
            :cx="centerX" 
            :cy="centerY" 
            :r="(radius / levels) * i"
            fill="none"
            stroke="#e5e7eb"
            :stroke-width="i === levels ? 2 : 1"
          />
          
          <!-- Axes lines -->
          <line 
            v-for="(skill, index) in skills" 
            :key="`axis-${index}`"
            :x1="centerX"
            :y1="centerY"
            :x2="getPointX(index, 100)"
            :y2="getPointY(index, 100)"
            stroke="#e5e7eb"
            stroke-width="1"
            stroke-dasharray="4,4"
          />
        </g>
        
        <!-- Data polygon -->
        <polygon
          :points="polygonPoints"
          fill="url(#radarGradient)"
          stroke="#667eea"
          stroke-width="3"
          stroke-linejoin="round"
          class="radar-polygon"
          :style="{ filter: glow ? 'url(#glow)' : 'none' }"
        />
        
        <!-- Comparison polygon (if enabled) -->
        <polygon
          v-if="showComparison && comparisonPolygonPoints"
          :points="comparisonPolygonPoints"
          fill="none"
          stroke="#ef4444"
          stroke-width="2"
          stroke-dasharray="5,5"
          stroke-linejoin="round"
          class="radar-comparison"
        />
        
        <!-- Data points -->
        <g class="radar-points">
          <circle
            v-for="(skill, index) in animatedSkills"
            :key="`point-${index}`"
            :cx="getPointX(index, skill.value)"
            :cy="getPointY(index, skill.value)"
            r="6"
            :fill="getPointColor(skill.value, index)"
            stroke="white"
            stroke-width="2"
            class="radar-point"
            :class="{ 'point-hovered': hoveredSkill === index }"
            @mouseenter="handleSkillHover(index)"
            @mouseleave="hoveredSkill = null"
            @click="handleSkillClick(index)"
          >
            <title>{{ skill.name }}: {{ skill.value }}%</title>
          </circle>
        </g>
        
        <!-- Value labels -->
        <g v-if="showValues" class="radar-values">
          <text
            v-for="(skill, index) in animatedSkills"
            :key="`value-${index}`"
            :x="getPointX(index, skill.value)"
            :y="getPointY(index, skill.value) - 15"
            text-anchor="middle"
            class="radar-value"
            :class="{ 'value-hovered': hoveredSkill === index }"
          >
            {{ Math.round(skill.value) }}%
          </text>
        </g>
        
        <!-- Labels -->
        <g class="radar-labels">
          <text
            v-for="(skill, index) in skills"
            :key="`label-${index}`"
            :x="getLabelX(index)"
            :y="getLabelY(index)"
            text-anchor="middle"
            class="radar-label"
            :class="{ 'label-hovered': hoveredSkill === index }"
          >
            {{ skill.name }}
          </text>
        </g>
      </svg>
      
      <!-- Tooltip -->
      <div 
        v-if="hoveredSkill !== null" 
        class="radar-tooltip"
        :style="tooltipStyle"
      >
        <div class="tooltip-content">
          <span class="tooltip-name">{{ skills[hoveredSkill].name }}</span>
          <span class="tooltip-value">{{ skills[hoveredSkill].value }}%</span>
        </div>
      </div>
    </div>
    
    <!-- Legend -->
    <div v-if="showLegend" class="radar-legend">
      <div 
        v-for="(skill, index) in skills" 
        :key="`legend-${index}`"
        class="legend-item"
        @mouseenter="hoveredSkill = index"
        @mouseleave="hoveredSkill = null"
        :class="{ 'legend-hovered': hoveredSkill === index }"
      >
        <div class="legend-color" :style="{ background: getPointColor(skill.value) }"></div>
        <span class="legend-name">{{ skill.name }}</span>
        <span class="legend-value">{{ skill.value }}%</span>
        <div class="legend-bar">
          <div 
            class="legend-bar-fill" 
            :style="{ width: `${skill.value}%`, background: getPointColor(skill.value) }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Skill {
  name: string
  value: number
  color?: string
  description?: string
}

const props = withDefaults(defineProps<{
  skills: Skill[]
  size?: number
  levels?: number
  title?: string
  subtitle?: string
  showLegend?: boolean
  glow?: boolean
  animated?: boolean
  interactive?: boolean
  showValues?: boolean
  showTooltips?: boolean
  colorScheme?: 'default' | 'gradient' | 'custom'
  customColors?: string[]
  animationDuration?: number
  showComparison?: boolean
  comparisonData?: Skill[]
}>(), {
  size: 400,
  levels: 5,
  title: '',
  subtitle: '',
  showLegend: true,
  glow: true,
  animated: true,
  interactive: true,
  showValues: true,
  showTooltips: true,
  colorScheme: 'default',
  customColors: () => [],
  animationDuration: 1000,
  showComparison: false,
  comparisonData: () => []
})

const emit = defineEmits<{
  'skill-hover': [skill: Skill, index: number]
  'skill-click': [skill: Skill, index: number]
  'radar-ready': []
}>()

const radarContainer = ref<HTMLElement | null>(null)
const hoveredSkill = ref<number | null>(null)
const animationProgress = ref(0)
const animationFrame = ref<number | null>(null)

// Computed properties
const centerX = computed(() => props.size / 2)
const centerY = computed(() => props.size / 2)
const radius = computed(() => (props.size / 2) - 60)
const angleStep = computed(() => (2 * Math.PI) / props.skills.length)

const colorPalette = computed(() => {
  switch (props.colorScheme) {
    case 'gradient':
      return [
        '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b',
        '#f6d365', '#fda085', '#a8edea', '#fed6e3', '#d299c2'
      ]
    case 'custom':
      return props.customColors.length > 0 ? props.customColors : [
        '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'
      ]
    default:
      return [
        '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'
      ]
  }
})

const animatedSkills = computed(() => {
  if (!props.animated) return props.skills
  
  return props.skills.map(skill => ({
    ...skill,
    value: skill.value * animationProgress.value
  }))
})

const polygonPoints = computed(() => {
  return animatedSkills.value
    .map((skill, index) => `${getPointX(index, skill.value)},${getPointY(index, skill.value)}`)
    .join(' ')
})

const comparisonPolygonPoints = computed(() => {
  if (!props.showComparison || !props.comparisonData) return ''
  
  return props.comparisonData
    .map((skill, index) => `${getPointX(index, skill.value)},${getPointY(index, skill.value)}`)
    .join(' ')
})

// Helper functions
const getPointX = (index: number, value: number) => {
  const angle = angleStep.value * index - Math.PI / 2
  return centerX.value + (radius.value * (value / 100)) * Math.cos(angle)
}

const getPointY = (index: number, value: number) => {
  const angle = angleStep.value * index - Math.PI / 2
  return centerY.value + (radius.value * (value / 100)) * Math.sin(angle)
}

const getLabelX = (index: number) => {
  const angle = angleStep.value * index - Math.PI / 2
  const labelRadius = radius.value + 30
  return centerX.value + labelRadius * Math.cos(angle)
}

const getLabelY = (index: number) => {
  const angle = angleStep.value * index - Math.PI / 2
  const labelRadius = radius.value + 30
  return centerY.value + labelRadius * Math.sin(angle) + 5
}

const getPointColor = (value: number, index: number) => {
  if (props.skills[index]?.color) return props.skills[index].color
  
  if (props.colorScheme === 'gradient') {
    return colorPalette.value[index % colorPalette.value.length]
  }
  
  if (value >= 80) return '#10b981'
  if (value >= 60) return '#3b82f6'
  if (value >= 40) return '#f59e0b'
  return '#ef4444'
}

const tooltipStyle = computed(() => {
  if (hoveredSkill.value === null) return {}
  
  const skill = props.skills[hoveredSkill.value]
  const x = getPointX(hoveredSkill.value, skill.value)
  const y = getPointY(hoveredSkill.value, skill.value)
  
  return {
    left: `${x}px`,
    top: `${y - 40}px`
  }
})

// Event handlers
const handleSkillHover = (index: number) => {
  if (!props.interactive) return
  
  hoveredSkill.value = index
  emit('skill-hover', props.skills[index], index)
}

const handleSkillClick = (index: number) => {
  if (!props.interactive) return
  
  emit('skill-click', props.skills[index], index)
}

// Animation
const startAnimation = () => {
  if (!props.animated) {
    animationProgress.value = 1
    return
  }
  
  const startTime = performance.now()
  
  const animate = (currentTime: number) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / props.animationDuration, 1)
    
    // Easing function (ease-out)
    animationProgress.value = 1 - Math.pow(1 - progress, 3)
    
    if (progress < 1) {
      animationFrame.value = requestAnimationFrame(animate)
    } else {
      emit('radar-ready')
    }
  }
  
  animationFrame.value = requestAnimationFrame(animate)
}

// Lifecycle
onMounted(() => {
  startAnimation()
})

onUnmounted(() => {
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value)
  }
})
</script>

<style scoped>
.skill-radar-wrapper {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.radar-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.radar-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.radar-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.radar-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

.radar-svg {
  max-width: 100%;
  height: auto;
}

.radar-polygon {
  transition: all 0.3s ease;
  animation: fadeInPolygon 1s ease-out;
}

@keyframes fadeInPolygon {
  from {
    opacity: 0;
    transform: scale(0.5);
    transform-origin: center;
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.radar-point {
  cursor: pointer;
  transition: all 0.2s ease;
  animation: popIn 0.5s ease-out backwards;
}

.radar-point:hover {
  r: 8;
  filter: drop-shadow(0 2px 8px rgba(102, 126, 234, 0.5));
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.radar-point:nth-child(1) { animation-delay: 0.1s; }
.radar-point:nth-child(2) { animation-delay: 0.2s; }
.radar-point:nth-child(3) { animation-delay: 0.3s; }
.radar-point:nth-child(4) { animation-delay: 0.4s; }
.radar-point:nth-child(5) { animation-delay: 0.5s; }
.radar-point:nth-child(6) { animation-delay: 0.6s; }

.radar-label {
  font-size: 0.875rem;
  font-weight: 600;
  fill: #374151;
  transition: all 0.2s ease;
  pointer-events: none;
}

.radar-label.label-hovered {
  font-size: 1rem;
  fill: #667eea;
  font-weight: 700;
}

.radar-tooltip {
  position: absolute;
  transform: translate(-50%, -100%);
  pointer-events: none;
  z-index: 10;
  animation: tooltipFadeIn 0.2s ease;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -100%) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -100%) scale(1);
  }
}

.tooltip-content {
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 0.5rem 0.875rem;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
}

.tooltip-content::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid rgba(0, 0, 0, 0.9);
}

.tooltip-name {
  font-size: 0.875rem;
  font-weight: 600;
}

.tooltip-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: #667eea;
}

.radar-legend {
  margin-top: 2rem;
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.legend-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  grid-template-rows: auto auto;
  gap: 0.5rem;
  align-items: center;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.legend-item:hover,
.legend-item.legend-hovered {
  background: #f9fafb;
  transform: translateX(4px);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  grid-row: 1 / 2;
}

.legend-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  grid-row: 1 / 2;
}

.legend-value {
  font-size: 0.875rem;
  font-weight: 700;
  color: #667eea;
  grid-row: 1 / 2;
}

.legend-bar {
  grid-column: 1 / 4;
  grid-row: 2 / 3;
  height: 4px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.legend-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease;
}

@media (max-width: 768px) {
  .skill-radar-wrapper {
    padding: 1rem;
  }
  
  .radar-legend {
    grid-template-columns: 1fr;
  }
}
</style>