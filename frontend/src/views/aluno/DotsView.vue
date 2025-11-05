<template>
  <div v-if="isLoading" class="loading-screen">
    <div class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i>
    </div>
  </div>
  
  <div v-else class="dots-root">
    <div class="container">
      <div class="header">
        <div>
          <h1 class="title">Perfil DOTS</h1>
          <p class="subtitle">Desenvolvimento Técnico e Social</p>
        </div>
        <div class="points-display">
          <div class="points-icon">
            <i class="fas fa-trophy"></i>
          </div>
          <div class="points-info">
            <span class="points-label">Pontuação Total</span>
            <span class="points-value">{{ totalPoints }}</span>
          </div>
        </div>
      </div>

      <div class="content-layout">
        <div class="main-content">
          <div class="skills-section">
            <div class="section-header">
              <h2 class="section-title">Minhas Habilidades</h2>
              <div class="progress-overview">
                <div class="progress-ring-small">
                  <svg viewBox="0 0 36 36" class="circular-chart">
                    <path
                      class="circle-bg"
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      class="circle"
                      :stroke-dasharray="`${overallProgress}, 100`"
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <text x="18" y="20.35" class="percentage">{{ overallProgress }}%</text>
                  </svg>
                </div>
                <span class="progress-label">Progresso Geral</span>
              </div>
            </div>

            <div class="skills-grid">
              <div v-for="(skill, index) in skills" :key="index" class="skill-card">
                <div class="skill-header">
                  <div class="skill-icon" :style="{ background: skillColors[index % skillColors.length] + '30' }">
                    <i class="fas fa-code"></i>
                  </div>
                  <h3 class="skill-name">{{ skill.name }}</h3>
                </div>
                <div class="skill-progress">
                  <div class="progress-bar-wrapper">
                    <div class="progress-bar-track">
                      <div 
                        class="progress-bar-fill" 
                        :style="{ width: skill.value + '%', background: skillColors[index % skillColors.length] }">
                      </div>
                    </div>
                    <span class="progress-value">{{ skill.value }}%</span>
                  </div>
                </div>
                <div class="skill-stats">
                  <div class="stat-item">
                    <i class="fas fa-project-diagram"></i>
                    <span>{{ skill.projects }} projetos</span>
                  </div>
                  <div class="stat-item">
                    <i class="fas fa-certificate"></i>
                    <span>{{ skill.certifications }} certificações</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="analysis-section">
            <div class="analysis-panel">
              <h2 class="section-title">Análise de Desenvolvimento</h2>
              <div class="analysis-content" v-html="analysis"></div>
            </div>

            <div class="comparison-panel">
              <h2 class="section-title">Comparação com a Turma</h2>
              <div class="chart-container">
                <!-- Aqui você pode inserir o componente InteractiveChart -->
                <div class="chart-placeholder">
                  <p>Gráfico de comparação radar</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="sidebar-content">
          <div class="achievements-panel">
            <div class="panel-header">
              <h2 class="panel-title">Conquistas</h2>
              <span class="achievements-count">{{ achievements.length }}</span>
            </div>

            <div class="achievements-list">
              <div v-for="achievement in achievements" :key="achievement.id" class="achievement-item">
                <div class="achievement-icon">
                  <i :class="achievement.icon || 'fas fa-award'"></i>
                </div>
                <div class="achievement-info">
                  <h3 class="achievement-title">{{ achievement.title }}</h3>
                  <p class="achievement-description">{{ achievement.description }}</p>
                  <div class="achievement-footer">
                    <span class="achievement-points">
                      <i class="fas fa-star"></i>
                      {{ achievement.points }} pts
                    </span>
                    <span class="achievement-date">{{ formatDate(achievement.date) }}</span>
                  </div>
                  <div v-if="achievement.badges && achievement.badges.length" class="achievement-badges">
                    <span v-for="(badge, i) in achievement.badges" :key="i" class="badge-tag">
                      {{ badge }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useDots } from '@/composables/useDots';

export default defineComponent({
  name: 'DotsView',
  setup() {
    const { profile, isLoading } = useDots();
    
    const skillColors = ['#9b59b6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'];
    
    const totalPoints = computed(() => profile.value?.totalPoints || 0);
    
    const overallProgress = computed(() => {
      const total = Object.values(profile.value?.skills || {}).reduce((sum: number, val: unknown) => sum + (typeof val === 'number' ? val : 0), 0);
      return Math.min(100, Math.floor(total / 500 * 100));
    });
    
    const skills = computed(() => {
      if (!profile.value) return [];
      return Object.entries(profile.value.skills)
        .map(([name, skillData]) => ({
          name: name as string,
          value: (skillData as any).value ?? 0,
          skills: (skillData as any).skills ?? [],
          projects: (skillData as any).projects ?? 0,
          certifications: (skillData as any).certifications ?? 0
        }))
        .sort((a, b) => b.value - a.value);
    });
    
    const achievements = computed(() => {
      return profile.value?.achievements || [];
    });
    
    const analysis = ref(`
      <h3>Pontos Fortes</h3>
      <ul>
        <li>Excelente desempenho em Linguagens e Comunicação</li>
        <li>Participação ativa em projetos colaborativos</li>
        <li>Bom desenvolvimento em atividades práticas</li>
      </ul>
      
      <h3>Áreas para Desenvolvimento</h3>
      <ul>
        <li>Raciocínio lógico pode ser aprimorado</li>
        <li>Maior dedicação em disciplinas exatas</li>
      </ul>
      
      <h3>Recomendações</h3>
      <p>Participe das atividades extras de matemática e do clube de programação para fortalecer suas habilidades técnicas.</p>
    `);

    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat('pt-BR', { 
        day: '2-digit', 
        month: 'short',
        year: 'numeric'
      }).format(date);
    };
    
    return { 
      profile, 
      isLoading,
      skillColors,
      totalPoints,
      overallProgress,
      skills,
      achievements,
      analysis,
      formatDate
    };
  }
});
</script>

<style scoped>
.loading-screen {
  min-height: 100vh;
  background: #17181e;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner i {
  font-size: 3rem;
  color: #3b82f6;
}

.dots-root {
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
  margin-bottom: 2.5rem;
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

.points-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 16px;
}

.points-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 12px;
  font-size: 1.5rem;
  color: #fff;
}

.points-info {
  display: flex;
  flex-direction: column;
}

.points-label {
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.points-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: #3b82f6;
  letter-spacing: -0.02em;
}

.content-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fcfcfc;
}

.progress-overview {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-ring-small {
  width: 60px;
  height: 60px;
}

.circular-chart {
  display: block;
  max-width: 100%;
  max-height: 100%;
}

.circle-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
  stroke-width: 2.8;
}

.circle {
  fill: none;
  stroke: #3b82f6;
  stroke-width: 2.8;
  stroke-linecap: round;
  animation: progress 1s ease-out forwards;
}

.percentage {
  fill: #fcfcfc;
  font-size: 0.4em;
  font-weight: 700;
  text-anchor: middle;
}

@keyframes progress {
  0% {
    stroke-dasharray: 0 100;
  }
}

.progress-label {
  font-size: 0.875rem;
  color: #8b92a8;
  font-weight: 600;
}

.skills-section {
  margin-bottom: 2rem;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}

.skill-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.skill-card:hover {
  transform: translateY(-4px);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
}

.skill-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.skill-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 1.25rem;
  color: #fcfcfc;
}

.skill-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #fcfcfc;
}

.skill-progress {
  margin-bottom: 1rem;
}

.progress-bar-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar-track {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.progress-value {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #fcfcfc;
  min-width: 48px;
  text-align: right;
}

.skill-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 600;
}

.stat-item i {
  color: #3b82f6;
}

.analysis-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.analysis-panel,
.comparison-panel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
}

.analysis-content {
  color: #fcfcfc;
  line-height: 1.7;
}

.analysis-content h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.75rem;
  margin-top: 1.25rem;
}

.analysis-content h3:first-child {
  margin-top: 0;
}

.analysis-content ul {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.analysis-content li {
  margin-bottom: 0.5rem;
  color: #8b92a8;
  font-size: 0.9375rem;
}

.analysis-content p {
  color: #8b92a8;
  font-size: 0.9375rem;
}

.chart-container {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #8b92a8;
  font-size: 1rem;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
}

.achievements-panel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  max-height: calc(100vh - 200px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fcfcfc;
}

.achievements-count {
  padding: 0.25rem 0.75rem;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 700;
  color: #3b82f6;
}

.achievements-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.achievement-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.achievement-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(59, 130, 246, 0.2);
}

.achievement-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.3) 0%, rgba(251, 191, 36, 0.1) 100%);
  border-radius: 12px;
  font-size: 1.5rem;
  color: #fbbf24;
}

.achievement-info {
  flex: 1;
  min-width: 0;
}

.achievement-title {
  font-size: 1rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 0.375rem;
}

.achievement-description {
  font-size: 0.8125rem;
  color: #8b92a8;
  line-height: 1.5;
  margin-bottom: 0.625rem;
}

.achievement-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.achievement-points {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 700;
  color: #fbbf24;
}

.achievement-date {
  font-size: 0.75rem;
  color: #8b92a8;
  font-weight: 500;
}

.achievement-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.badge-tag {
  padding: 0.25rem 0.625rem;
  background: rgba(59, 130, 246, 0.15);
  border-radius: 6px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: #3b82f6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

@media (max-width: 1200px) {
  .content-layout {
    grid-template-columns: 1fr;
  }

  .achievements-panel {
    max-height: 600px;
  }
}

@media (max-width: 768px) {
  .dots-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .skills-grid {
    grid-template-columns: 1fr;
  }

  .analysis-section {
    grid-template-columns: 1fr;
  }
}
</style>