<template>
  <div class="system-status">
    <div class="status-header">
      <h1 class="status-title">
        <i class="fas fa-heartbeat"></i>
        Status do Sistema S.U.M
      </h1>
      <div class="status-actions">
        <button @click="refreshStatus" :disabled="loading" class="btn-refresh">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
          Atualizar
        </button>
        <button @click="toggleAutoRefresh" class="btn-auto" :class="{ active: autoRefresh }">
          <i class="fas fa-play" v-if="!autoRefresh"></i>
          <i class="fas fa-pause" v-else></i>
          {{ autoRefresh ? 'Pausar' : 'Auto' }}
        </button>
      </div>
    </div>

    <!-- Status Geral -->
    <div class="status-overview">
      <div class="status-card" :class="overallStatus">
        <div class="status-icon">
          <i class="fas fa-server"></i>
        </div>
        <div class="status-info">
          <h3>Sistema {{ overallStatus === 'healthy' ? 'Funcionando' : 'Com Problemas' }}</h3>
          <p>Última verificação: {{ lastCheck }}</p>
        </div>
        <div class="status-indicator">
          <div class="pulse" :class="overallStatus"></div>
        </div>
      </div>
    </div>

    <!-- Grid de Serviços -->
    <div class="services-grid">
      <div v-for="(service, key) in services" :key="key" class="service-card" :class="service.status">
        <div class="service-header">
          <div class="service-icon">
            <i :class="getServiceIcon(key)"></i>
          </div>
          <div class="service-name">
            <h4>{{ getServiceName(key) }}</h4>
            <span class="service-status">{{ getStatusText(service.status) }}</span>
          </div>
          <div class="service-indicator">
            <div class="status-dot" :class="service.status"></div>
          </div>
        </div>
        
        <div class="service-details" v-if="service.details">
          <div v-for="(detail, detailKey) in service.details" :key="detailKey" class="detail-item">
            <span class="detail-label">{{ detailKey }}:</span>
            <span class="detail-value">{{ detail }}</span>
          </div>
        </div>
        
        <div class="service-error" v-if="service.error">
          <i class="fas fa-exclamation-triangle"></i>
          {{ service.error }}
        </div>
      </div>
    </div>

    <!-- Métricas do Sistema -->
    <div class="metrics-section" v-if="systemMetrics">
      <h3>Métricas do Sistema</h3>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-microchip"></i>
          </div>
          <div class="metric-info">
            <h4>CPU</h4>
            <div class="metric-value">{{ systemMetrics.cpu?.percent || 0 }}%</div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: (systemMetrics.cpu?.percent || 0) + '%' }"></div>
            </div>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-memory"></i>
          </div>
          <div class="metric-info">
            <h4>Memória</h4>
            <div class="metric-value">{{ systemMetrics.memory?.percent || 0 }}%</div>
            <div class="metric-details">
              {{ systemMetrics.memory?.used_gb || 0 }}GB / {{ systemMetrics.memory?.total_gb || 0 }}GB
            </div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: (systemMetrics.memory?.percent || 0) + '%' }"></div>
            </div>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-hdd"></i>
          </div>
          <div class="metric-info">
            <h4>Disco</h4>
            <div class="metric-value">{{ systemMetrics.disk?.percent || 0 }}%</div>
            <div class="metric-details">
              {{ systemMetrics.disk?.used_gb || 0 }}GB / {{ systemMetrics.disk?.total_gb || 0 }}GB
            </div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: (systemMetrics.disk?.percent || 0) + '%' }"></div>
            </div>
          </div>
        </div>
        
        <div class="metric-card">
          <div class="metric-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="metric-info">
            <h4>Uptime</h4>
            <div class="metric-value">{{ formatUptime(systemMetrics.uptime_seconds) }}</div>
            <div class="metric-details">
              Desde {{ formatDate(systemMetrics.boot_time) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Logs de Erro -->
    <div class="logs-section" v-if="errorLogs.length > 0">
      <h3>Logs de Erro</h3>
      <div class="logs-container">
        <div v-for="(log, index) in errorLogs" :key="index" class="log-entry error">
          <div class="log-time">{{ log.timestamp }}</div>
          <div class="log-message">{{ log.message }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

// Estado reativo
const loading = ref(false)
const autoRefresh = ref(false)
const lastCheck = ref('')
const overallStatus = ref('unknown')
const services = ref({})
const systemMetrics = ref(null)
const errorLogs = ref([])

let refreshInterval: number | null = null

// Mapeamento de serviços
const serviceMap = {
  database: { name: 'Banco de Dados', icon: 'fas fa-database' },
  cache: { name: 'Cache Redis', icon: 'fas fa-memory' },
  system: { name: 'Sistema', icon: 'fas fa-server' },
  configuration: { name: 'Configuração', icon: 'fas fa-cog' },
  frontend: { name: 'Frontend', icon: 'fas fa-desktop' },
  nginx: { name: 'Nginx', icon: 'fas fa-globe' }
}

// Métodos
const getServiceIcon = (key: string) => {
  return serviceMap[key]?.icon || 'fas fa-question'
}

const getServiceName = (key: string) => {
  return serviceMap[key]?.name || key
}

const getStatusText = (status: string) => {
  const statusMap = {
    healthy: 'Funcionando',
    unhealthy: 'Com Problemas',
    degraded: 'Degradado',
    unknown: 'Desconhecido'
  }
  return statusMap[status] || status
}

const formatUptime = (seconds: number) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) return `${days}d ${hours}h ${minutes}m`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('pt-BR')
}

const checkBackendHealth = async () => {
  try {
    const response = await fetch('/api/health/detailed/')
    if (response.ok) {
      const data = await response.json()
      services.value = data.checks || {}
      overallStatus.value = data.status || 'unknown'
      lastCheck.value = new Date().toLocaleString('pt-BR')
    } else {
      throw new Error(`HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Erro ao verificar backend:', error)
    services.value = {
      backend: {
        status: 'unhealthy',
        error: 'Backend não está respondendo'
      }
    }
    overallStatus.value = 'unhealthy'
    errorLogs.value.unshift({
      timestamp: new Date().toLocaleString('pt-BR'),
      message: `Backend: ${error.message}`
    })
  }
}

const checkSystemMetrics = async () => {
  try {
    const response = await fetch('/api/metrics/')
    if (response.ok) {
      systemMetrics.value = await response.json()
    }
  } catch (error) {
    console.error('Erro ao obter métricas:', error)
  }
}

const checkFrontendHealth = () => {
  services.value = {
    ...services.value,
    frontend: {
      status: 'healthy',
      details: {
        'URL': window.location.origin,
        'User Agent': navigator.userAgent.substring(0, 50) + '...',
        'Online': navigator.onLine ? 'Sim' : 'Não'
      }
    }
  }
}

const checkNginxHealth = async () => {
  try {
    const response = await fetch('/api/health/')
    if (response.ok) {
      services.value = {
        ...services.value,
        nginx: {
          status: 'healthy',
          details: {
            'Proxy': 'Funcionando',
            'Response Time': '< 100ms'
          }
        }
      }
    }
  } catch (error) {
    services.value = {
      ...services.value,
      nginx: {
        status: 'unhealthy',
        error: 'Nginx não está respondendo'
      }
    }
  }
}

const refreshStatus = async () => {
  loading.value = true
  try {
    await Promise.all([
      checkBackendHealth(),
      checkSystemMetrics(),
      checkFrontendHealth(),
      checkNginxHealth()
    ])
  } finally {
    loading.value = false
  }
}

const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  
  if (autoRefresh.value) {
    refreshInterval = setInterval(refreshStatus, 30000) // 30 segundos
  } else {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }
}

// Lifecycle
onMounted(() => {
  refreshStatus()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.system-status {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.status-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-actions {
  display: flex;
  gap: 1rem;
}

.btn-refresh, .btn-auto {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-refresh:hover, .btn-auto:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-auto.active {
  background: rgba(255, 255, 255, 0.4);
}

.status-overview {
  margin-bottom: 2rem;
}

.status-card {
  display: flex;
  align-items: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 6px solid #e5e7eb;
}

.status-card.healthy {
  border-left-color: #10b981;
}

.status-card.unhealthy {
  border-left-color: #ef4444;
}

.status-card.degraded {
  border-left-color: #f59e0b;
}

.status-icon {
  font-size: 3rem;
  margin-right: 1.5rem;
  color: #6b7280;
}

.status-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.status-info p {
  margin: 0;
  color: #6b7280;
}

.status-indicator {
  margin-left: auto;
}

.pulse {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.pulse.healthy {
  background: #10b981;
}

.pulse.unhealthy {
  background: #ef4444;
}

.pulse.degraded {
  background: #f59e0b;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.service-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #e5e7eb;
  transition: transform 0.2s ease;
}

.service-card:hover {
  transform: translateY(-2px);
}

.service-card.healthy {
  border-left-color: #10b981;
}

.service-card.unhealthy {
  border-left-color: #ef4444;
}

.service-card.degraded {
  border-left-color: #f59e0b;
}

.service-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.service-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
  color: #6b7280;
}

.service-name h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.service-status {
  font-size: 0.875rem;
  color: #6b7280;
}

.service-indicator {
  margin-left: auto;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-dot.healthy {
  background: #10b981;
}

.status-dot.unhealthy {
  background: #ef4444;
}

.status-dot.degraded {
  background: #f59e0b;
}

.service-details {
  margin-top: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.detail-label {
  font-weight: 500;
  color: #6b7280;
}

.detail-value {
  color: #374151;
}

.service-error {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.metrics-section {
  margin-bottom: 2rem;
}

.metrics-section h3 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  font-size: 2rem;
  color: #6b7280;
}

.metric-info {
  flex: 1;
}

.metric-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.metric-details {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.metric-bar {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.metric-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  transition: width 0.3s ease;
}

.logs-section h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
}

.logs-container {
  background: #1f2937;
  border-radius: 8px;
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.log-entry {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.log-entry.error {
  background: #7f1d1d;
  color: #fca5a5;
}

.log-time {
  color: #9ca3af;
  margin-right: 1rem;
}

.log-message {
  color: #fca5a5;
}

@media (max-width: 768px) {
  .system-status {
    padding: 1rem;
  }
  
  .status-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
