Classroom
<template>
  <div class="classroom-root">
    <div class="container">
      <div class="header">
        <div>
          <h1 class="title">Minha Sala de Aula</h1>
          <p class="subtitle">Sala 1A - Professora Mariana Silva</p>
        </div>
        <div class="class-stats">
          <div class="stat-item">
            <i class="fas fa-users"></i>
            <span>32 alunos</span>
          </div>
        </div>
      </div>

      <div class="classroom-container">
        <div class="map-section">
          <div class="map-header">
            <h2 class="map-title">Mapa da Sala</h2>
            <div class="map-controls">
              <button class="control-btn">
                <i class="fas fa-search-plus"></i>
              </button>
              <button class="control-btn">
                <i class="fas fa-search-minus"></i>
              </button>
              <button class="control-btn">
                <i class="fas fa-sync-alt"></i>
              </button>
            </div>
          </div>

          <div class="map-wrapper">
            <ClassroomMap2D 
              :rows="6"
              :cols="6"
              groupMode="single"
              :rowsConfig="[6,6,6,6,6,6]"
              teacherArea="center"
              teacherLabel="Prof"
              backgroundColor="#f8fafc"
              :alternateColors="true"
              :showNumbers="true"
              :showBorders="true"
              :students="studentNames"
              :editable="false"
            />
          </div>
        </div>

        <div class="info-section">
          <div class="info-panel">
            <h3 class="info-title">Informações da Turma</h3>
            <div class="info-list">
              <div class="info-row">
                <span class="info-label">Turno</span>
                <span class="info-value">Manhã</span>
              </div>
              <div class="info-row">
                <span class="info-label">Horário</span>
                <span class="info-value">7:30 - 12:00</span>
              </div>
              <div class="info-row">
                <span class="info-label">Sala</span>
                <span class="info-value">201</span>
              </div>
              <div class="info-row">
                <span class="info-label">Total de Alunos</span>
                <span class="info-value">32</span>
              </div>
            </div>
          </div>

          <div class="info-panel">
            <h3 class="info-title">Colegas Próximos</h3>
            <div class="nearby-students">
              <div class="student-item">
                <div class="student-avatar">JM</div>
                <div class="student-info">
                  <span class="student-name">João Miguel</span>
                  <span class="student-position">À sua esquerda</span>
                </div>
              </div>
              <div class="student-item">
                <div class="student-avatar">AS</div>
                <div class="student-info">
                  <span class="student-name">Ana Silva</span>
                  <span class="student-position">À sua direita</span>
                </div>
              </div>
              <div class="student-item">
                <div class="student-avatar">CO</div>
                <div class="student-info">
                  <span class="student-name">Carlos Oliveira</span>
                  <span class="student-position">Atrás de você</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ClassroomMap2D from '@components/classroom/ClassroomMap2D.vue'
import { computed } from 'vue'

// Nome dos alunos apenas para exibição do mapa (somente visualização)
const studentNames = computed(() =>
  Array.from({ length: 36 }).map((_, i) => ({ name: `Aluno ${i+1}` }))
)
</script>

<style scoped>
.classroom-root {
  min-height: 100vh;
  background: #17181e;
  color: #fcfcfc;
  padding: 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fcfcfc;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1rem;
  color: #8b92a8;
  font-weight: 500;
}

.class-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.75rem 1.25rem;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #3b82f6;
}

.classroom-container {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
}

.map-section {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
}

.map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.map-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fcfcfc;
}

.map-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #8b92a8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.map-wrapper {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 2rem;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.classroom-legend {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 0.875rem;
  color: #fcfcfc;
  font-weight: 600;
}

.legend-color {
  width: 24px;
  height: 24px;
  border-radius: 6px;
}

.legend-color.teacher {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
}

.legend-color.student {
  background: rgba(139, 92, 246, 0.4);
  border: 2px solid #a78bfa;
}

.legend-color.empty {
  background: rgba(255, 255, 255, 0.08);
  border: 1px dashed rgba(255, 255, 255, 0.2);
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-panel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
}

.info-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 1.25rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}

.info-label {
  font-size: 0.875rem;
  color: #8b92a8;
  font-weight: 600;
}

.info-value {
  font-size: 0.9375rem;
  color: #fcfcfc;
  font-weight: 700;
}

.nearby-students {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.student-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(59, 130, 246, 0.2);
}

.student-avatar {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
}

.student-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.student-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fcfcfc;
}

.student-position {
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .classroom-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .classroom-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }
}
</style>