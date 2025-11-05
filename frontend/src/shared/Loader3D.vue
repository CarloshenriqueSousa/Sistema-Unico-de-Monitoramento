<template>
  <div class="loader-wrapper" :class="{ 'loader-fullscreen': fullscreen }">
    <div class="loader-container">
      <div :class="['loader', `loader-${type}`]">
        <div v-if="type === 'cube'" class="cube">
          <div class="cube-face cube-front"></div>
          <div class="cube-face cube-back"></div>
          <div class="cube-face cube-right"></div>
          <div class="cube-face cube-left"></div>
          <div class="cube-face cube-top"></div>
          <div class="cube-face cube-bottom"></div>
        </div>
        
        <div v-else-if="type === 'dots'" class="dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        
        <div v-else-if="type === 'ring'" class="ring">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
        
        <div v-else-if="type === 'pulse'" class="pulse">
          <div></div>
          <div></div>
          <div></div>
        </div>
        
        <div v-else-if="type === 'spinner'" class="spinner">
          <div></div>
        </div>
      </div>
      
      <div v-if="message || $slots.default" class="loader-content">
        <slot>
          <p class="loader-message">{{ message }}</p>
        </slot>
        <div v-if="showProgress" class="loader-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          </div>
          <span class="progress-text">{{ progress }}%</span>
        </div>
      </div>
    </div>
    
    <div v-if="overlay" class="loader-overlay"></div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'cube',
    validator: (value) => ['cube', 'dots', 'ring', 'pulse', 'spinner'].includes(value)
  },
  message: {
    type: String,
    default: ''
  },
  fullscreen: {
    type: Boolean,
    default: false
  },
  overlay: {
    type: Boolean,
    default: false
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})
</script>

<style scoped>
.loader-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  position: relative;
}

.loader-fullscreen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
}

.loader-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  z-index: 1;
}

.loader {
  position: relative;
}

/* CUBE LOADER */
.cube {
  width: 60px;
  height: 60px;
  transform-style: preserve-3d;
  animation: rotateCube 3s infinite ease-in-out;
}

.cube-face {
  position: absolute;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: 2px solid rgba(255, 255, 255, 0.3);
  opacity: 0.9;
}

.cube-front  { transform: rotateY(0deg) translateZ(30px); }
.cube-back   { transform: rotateY(180deg) translateZ(30px); }
.cube-right  { transform: rotateY(90deg) translateZ(30px); }
.cube-left   { transform: rotateY(-90deg) translateZ(30px); }
.cube-top    { transform: rotateX(90deg) translateZ(30px); }
.cube-bottom { transform: rotateX(-90deg) translateZ(30px); }

@keyframes rotateCube {
  0% { transform: rotateX(0deg) rotateY(0deg); }
  50% { transform: rotateX(180deg) rotateY(180deg); }
  100% { transform: rotateX(360deg) rotateY(360deg); }
}

/* DOTS LOADER */
.dots {
  display: flex;
  gap: 0.75rem;
}

.dots span {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  animation: bounceDots 1.4s infinite ease-in-out both;
}

.dots span:nth-child(1) { animation-delay: -0.32s; }
.dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounceDots {
  0%, 80%, 100% { 
    transform: scale(0);
    opacity: 0.5;
  }
  40% { 
    transform: scale(1);
    opacity: 1;
  }
}

/* RING LOADER */
.ring {
  display: inline-block;
  position: relative;
  width: 64px;
  height: 64px;
}

.ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 51px;
  height: 51px;
  margin: 6px;
  border: 6px solid;
  border-radius: 50%;
  animation: rotateRing 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #667eea transparent transparent transparent;
}

.ring div:nth-child(1) { animation-delay: -0.45s; }
.ring div:nth-child(2) { animation-delay: -0.3s; }
.ring div:nth-child(3) { animation-delay: -0.15s; }

@keyframes rotateRing {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* PULSE LOADER */
.pulse {
  display: flex;
  gap: 0.5rem;
}

.pulse div {
  width: 14px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 7px;
  animation: scalePulse 1s infinite ease-in-out;
}

.pulse div:nth-child(1) { animation-delay: 0s; }
.pulse div:nth-child(2) { animation-delay: 0.15s; }
.pulse div:nth-child(3) { animation-delay: 0.3s; }

@keyframes scalePulse {
  0%, 100% { transform: scaleY(0.4); opacity: 0.6; }
  50% { transform: scaleY(1); opacity: 1; }
}

/* SPINNER LOADER */
.spinner {
  width: 64px;
  height: 64px;
}

.spinner div {
  width: 100%;
  height: 100%;
  border: 6px solid #f3f4f6;
  border-top-color: #667eea;
  border-right-color: #764ba2;
  border-radius: 50%;
  animation: rotateSpinner 1s linear infinite;
}

@keyframes rotateSpinner {
  to { transform: rotate(360deg); }
}

/* CONTENT */
.loader-content {
  text-align: center;
  max-width: 300px;
}

.loader-message {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  line-height: 1.5;
}

.loader-progress {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 999px;
  transition: width 0.3s ease;
  position: relative;
  overflow: hidden;
}

.progress-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.3), 
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  align-self: flex-end;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .cube {
    width: 50px;
    height: 50px;
  }
  
  .cube-face {
    width: 50px;
    height: 50px;
  }
  
  .cube-front, .cube-back, .cube-right, 
  .cube-left, .cube-top, .cube-bottom {
    transform-origin: center;
  }
  
  .cube-front  { transform: rotateY(0deg) translateZ(25px); }
  .cube-back   { transform: rotateY(180deg) translateZ(25px); }
  .cube-right  { transform: rotateY(90deg) translateZ(25px); }
  .cube-left   { transform: rotateY(-90deg) translateZ(25px); }
  .cube-top    { transform: rotateX(90deg) translateZ(25px); }
  .cube-bottom { transform: rotateX(-90deg) translateZ(25px); }
}
</style>