<template>
  <button 
    :class="[
      'btn',
      `btn-${variant}`,
      `btn-${size}`,
      { 'btn-loading': loading, 'btn-icon-only': iconOnly }
    ]" 
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="spinner"></span>
    <slot v-else></slot>
  </button>
</template>

<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'ghost', 'outline'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  iconOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  white-space: nowrap;
  user-select: none;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn:not(:disabled):active {
  transform: translateY(0);
}

/* Sizes */
.btn-sm {
  padding: 0.375rem 0.875rem;
  font-size: 0.875rem;
  border-radius: 0.375rem;
}

.btn-md {
  padding: 0.625rem 1.25rem;
  font-size: 0.9375rem;
}

.btn-lg {
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
}

.btn-xl {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}

.btn-icon-only {
  aspect-ratio: 1;
  padding: 0.625rem;
}

.btn-icon-only.btn-sm {
  padding: 0.5rem;
}

.btn-icon-only.btn-lg {
  padding: 0.875rem;
}

/* Variants */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-primary:not(:disabled):hover {
  background: linear-gradient(135deg, #5568d3 0%, #63408a 100%);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.3);
}

.btn-secondary:not(:disabled):hover {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
}

.btn-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.btn-success:not(:disabled):hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.btn-danger:not(:disabled):hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.btn-warning:not(:disabled):hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
}

.btn-ghost {
  background: transparent;
  color: #4b5563;
}

.btn-ghost:not(:disabled):hover {
  background: rgba(107, 114, 128, 0.1);
  box-shadow: none;
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  box-shadow: none;
}

.btn-outline:not(:disabled):hover {
  background: #667eea;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Loading State */
.btn-loading {
  pointer-events: none;
}

.spinner {
  width: 1em;
  height: 1em;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>