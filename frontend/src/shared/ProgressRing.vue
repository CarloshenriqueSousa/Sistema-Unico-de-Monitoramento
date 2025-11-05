<template>
  <div class="progress-ring-wrapper" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg 
      class="progress-ring-svg" 
      :width="size" 
      :height="size"
      :viewBox="`0 0 ${size} ${size}`"
    >
      <defs>
        <linearGradient :id="`gradient-${uid}`" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" :style="{ stopColor: gradientStart }" />
          <stop offset="100%" :style="{ stopColor: gradientEnd }" />
        </linearGradient>
        <filter :id="`shadow-${uid}`">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
        </filter>
      </defs>
      
      <!-- Background Circle -->
      <circle
        class="progress-ring-circle-bg"
        :stroke-width="strokeWidth"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
        fill="none"
        :stroke="backgroundColor"
      />
      
      <!-- Progress Circle -->
      <circle
        class="progress-ring-circle"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
        fill="none"
        :stroke="gradient ? `url(#gradient-${uid})` : color"
        :style="{ filter: animated ? `url(#shadow-${uid})` : 'none' }"
      />
      
      <!-- Glow Effect -->
      <circle
        v-if="glow"
        class="progress-ring-glow"
        :stroke-width="strokeWidth + 4"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
        fill="none"
        :stroke="gradient ? `url(#gradient-${uid})` : color"
        opacity="0.2"
      />
    </svg>
    
    <div class="progress-ring-content">
      <slot>
        <div class="progress-ring-text">
          <span class="progress-percentage">{{ displayPercentage }}%</span>
          <span v-if="label" class="progress-label">{{ label }}</span>
        </div>
      </slot>
    </div>
    
    <div v-if="showDots" class="progress-dots">
      <span 
        v-for="i in 4" 
        :key="i" 
        class="dot"
        :class="{ active: percentage >= (i * 25) }"
      ></span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  percentage: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  size: {
    type: Number,
    default: 120
  },
  strokeWidth: {
    type: Number,
    default: 8
  },
  color: {
    type: String,
    default: '#667eea'
  },
  backgroundColor: {
    type: String,
    default: '#e5e7eb'
  },
  gradient: {
    type: Boolean,
    default: true
  },
  gradientStart: {
    type: String,
    default: '#667eea'
  },
  gradientEnd: {
    type: String,
    default: '#764ba2'
  },
  animated: {
    type: Boolean,
    default: true
  },
  glow: {
    type: Boolean,
    default: true
  },
  showDots: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 1
  }
})

const uid = ref(`ring-${Math.random().toString(36).substr(2, 9)}`)

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const offset = computed(() => {
  const pct = Math.max(0, Math.min(100, props.percentage))
  return circumference.value - (pct / 100) * circumference.value
})

const displayPercentage = computed(() => Math.round(props.percentage))
</script>

<style scoped>
.progress-ring-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.progress-ring-svg {
  transform: rotate(-90deg);
}

.progress-ring-circle-bg {
  transition: stroke 0.3s ease;
}

.progress-ring-circle {
  stroke-linecap: round;
  transition: stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fillProgress 1s ease-out;
}

.progress-ring-glow {
  stroke-linecap: round;
  transition: all 0.3s ease;
  filter: blur(8px);
}

@keyframes fillProgress {
  from {
    stroke-dashoffset: var(--circumference, 377);
  }
}

.progress-ring-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.progress-ring-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  text-align: center;
}

.progress-percentage {
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  animation: countUp 1s ease-out;
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.progress-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.progress-dots {
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e5e7eb;
  transition: all 0.3s ease;
}

.dot.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
  transform: scale(1.2);
}

/* Size Variants */
.progress-ring-wrapper[style*="width: 80px"] .progress-percentage {
  font-size: 1.25rem;
}

.progress-ring-wrapper[style*="width: 80px"] .progress-label {
  font-size: 0.75rem;
}

.progress-ring-wrapper[style*="width: 150px"] .progress-percentage {
  font-size: 2.5rem;
}

.progress-ring-wrapper[style*="width: 150px"] .progress-label {
  font-size: 1rem;
}

/* Hover Effect */
.progress-ring-wrapper:hover .progress-ring-circle {
  filter: drop-shadow(0 4px 12px rgba(102, 126, 234, 0.4));
}

.progress-ring-wrapper:hover .progress-percentage {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}
</style>