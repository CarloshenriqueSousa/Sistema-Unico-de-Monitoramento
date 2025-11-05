<template>
  <div 
    :class="[
      'glass-card',
      `glass-${variant}`,
      `blur-${blur}`,
      { 'glass-hover': hover, 'glass-bordered': bordered }
    ]"
  >
    <div v-if="$slots.header || title" class="glass-card-header">
      <slot name="header">
        <h3 v-if="title" class="glass-card-title">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="glass-card-body">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="glass-card-footer">
      <slot name="footer"></slot>
    </div>
    
    <div class="glass-shine"></div>
  </div>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'light',
    validator: (value) => ['light', 'dark', 'gradient', 'colorful'].includes(value)
  },
  blur: {
    type: String,
    default: 'medium',
    validator: (value) => ['light', 'medium', 'strong'].includes(value)
  },
  hover: {
    type: Boolean,
    default: true
  },
  bordered: {
    type: Boolean,
    default: true
  },
  title: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.glass-card {
  position: relative;
  border-radius: 1.25rem;
  padding: 1.5rem;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.05));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.glass-bordered::before {
  opacity: 1;
}

.glass-card:not(.glass-bordered)::before {
  opacity: 0;
}

/* Variants */
.glass-light {
  background: rgba(255, 255, 255, 0.7);
  color: #1f2937;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
}

.glass-dark {
  background: rgba(30, 30, 46, 0.7);
  color: #f3f4f6;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.glass-gradient {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #1f2937;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.glass-colorful {
  background: linear-gradient(135deg, 
    rgba(236, 72, 153, 0.1) 0%, 
    rgba(239, 68, 68, 0.1) 25%,
    rgba(245, 158, 11, 0.1) 50%,
    rgba(16, 185, 129, 0.1) 75%,
    rgba(59, 130, 246, 0.1) 100%
  );
  color: #1f2937;
  box-shadow: 0 8px 32px rgba(147, 51, 234, 0.2);
}

/* Blur levels */
.blur-light {
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.blur-medium {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.blur-strong {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Hover effect */
.glass-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(31, 38, 135, 0.25);
}

.glass-dark.glass-hover:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
}

/* Shine effect */
.glass-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent
  );
  transition: left 0.5s;
  pointer-events: none;
}

.glass-hover:hover .glass-shine {
  left: 100%;
}

/* Card sections */
.glass-card-header {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-dark .glass-card-header {
  border-bottom-color: rgba(255, 255, 255, 0.05);
}

.glass-card-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.glass-dark .glass-card-title {
  background: linear-gradient(135deg, #a5b4fc 0%, #c4b5fd 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.glass-card-body {
  position: relative;
  z-index: 1;
}

.glass-card-footer {
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-dark .glass-card-footer {
  border-top-color: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 768px) {
  .glass-card {
    padding: 1.25rem;
    border-radius: 1rem;
  }
  
  .glass-card-title {
    font-size: 1.25rem;
  }
}
</style>