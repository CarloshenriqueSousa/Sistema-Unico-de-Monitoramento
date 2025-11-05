<template>
  <div class="student-card">
    <div class="card-glow"></div>
    
    <div class="card-header">
      <div class="avatar-wrapper">
        <div class="avatar">
          {{ getInitials(student?.name) }}
        </div>
        <div class="status-indicator" :class="getStatusClass()"></div>
      </div>
      
      <div class="student-info">
        <h4 class="student-name">{{ student?.name }}</h4>
        <p class="student-email">{{ student?.email }}</p>
      </div>
    </div>
    
    <div class="card-divider"></div>
    
    <div class="card-stats">
      <div class="stat-item">
        <div class="stat-label">Média Geral</div>
        <div class="stat-value" :class="getScoreClass(student?.averageScore)">
          {{ student?.averageScore?.toFixed(1) || '0.0' }}
        </div>
        <div class="stat-bar">
          <div 
            class="stat-fill" 
            :class="getScoreClass(student?.averageScore)"
            :style="{ width: `${(student?.averageScore || 0)}%` }"
          ></div>
        </div>
      </div>
      
      <div class="stat-grid">
        <div class="stat-mini">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="stat-icon">
            <path d="M10.75 10.818v2.614A3.13 3.13 0 0011.888 13c.482-.315.612-.648.612-.875 0-.227-.13-.56-.612-.875a3.13 3.13 0 00-1.138-.432zM8.33 8.62c.053.055.115.11.184.164.208.16.46.284.736.363V6.603a2.45 2.45 0 00-.35.13c-.14.065-.27.143-.386.233-.377.292-.514.627-.514.909 0 .184.058.39.202.592.037.051.08.102.128.152z" />
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-6a.75.75 0 01.75.75v.316a3.78 3.78 0 011.653.713c.426.33.744.74.925 1.2a.75.75 0 01-1.395.55 1.35 1.35 0 00-.447-.563 2.187 2.187 0 00-.736-.363V9.3c.698.093 1.383.32 1.959.696.787.514 1.29 1.27 1.29 2.13 0 .86-.504 1.616-1.29 2.13-.576.377-1.261.603-1.96.696v.299a.75.75 0 11-1.5 0v-.3c-.697-.092-1.382-.318-1.958-.695-.482-.315-.857-.717-1.078-1.188a.75.75 0 111.359-.636c.08.173.245.376.54.569.313.205.706.353 1.138.432v-2.748a3.782 3.782 0 01-1.653-.713C6.9 9.433 6.5 8.681 6.5 7.875c0-.805.4-1.558 1.097-2.096a3.78 3.78 0 011.653-.713V4.75A.75.75 0 0110 4z" clip-rule="evenodd" />
          </svg>
          <span>{{ student?.attendanceRate || 95 }}%</span>
        </div>
        
        <div class="stat-mini">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="stat-icon">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm.75-13a.75.75 0 00-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 000-1.5h-3.25V5z" clip-rule="evenodd" />
          </svg>
          <span>{{ student?.tasksCompleted || 12 }}/15</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ 
  student?: { 
    name: string; 
    email: string; 
    averageScore: number;
    attendanceRate?: number;
    tasksCompleted?: number;
    active?: boolean;
  } 
}>()

const getInitials = (name: string = '') => {
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
}

const getStatusClass = () => {
  return props.student?.active !== false ? 'status-active' : 'status-inactive';
}

const getScoreClass = (score: number = 0) => {
  if (score >= 80) return 'score-excellent';
  if (score >= 60) return 'score-good';
  return 'score-needs-improvement';
}
</script>

<style scoped>
.student-card {
  position: relative;
  background: #ffffff;
  border-radius: 1rem;
  padding: 1.5rem;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(45, 83, 26, 0.1);
}

.student-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(31, 29, 32, 0.12);
  border-color: rgba(45, 83, 26, 0.3);
}

.card-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, rgba(225, 212, 194, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  border-radius: 1rem;
}

.student-card:hover .card-glow {
  opacity: 1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 700;
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 0.875rem;
  height: 0.875rem;
  border-radius: 50%;
  border: 2px solid #ffffff;
}

.status-active {
  background: #2d531a;
}

.status-inactive {
  background: #9ca3af;
}

.student-info {
  flex: 1;
  min-width: 0;
}

.student-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f1d20;
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
}

.student-email {
  font-size: 0.8125rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(45, 83, 26, 0.2), transparent);
  margin-bottom: 1.25rem;
}

.card-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
}

.score-excellent {
  color: #2d531a;
}

.score-good {
  color: #0f1e3f;
}

.score-needs-improvement {
  color: #dc2626;
}

.stat-bar {
  height: 0.5rem;
  background: #e1d4c2;
  border-radius: 0.25rem;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-fill.score-excellent {
  background: linear-gradient(90deg, #2d531a, #166534);
}

.stat-fill.score-good {
  background: linear-gradient(90deg, #0f1e3f, #1e3a8a);
}

.stat-fill.score-needs-improvement {
  background: linear-gradient(90deg, #dc2626, #991b1b);
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.stat-mini {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f1d20;
}

.stat-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: #2d531a;
}

@media (max-width: 640px) {
  .student-card {
    padding: 1.25rem;
  }
  
  .stat-value {
    font-size: 1.75rem;
  }
}
</style>