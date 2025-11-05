<template>
  <div class="dashboard-root">
    <header class="header">
      <div class="header-content">
        <div>
          <h1 class="title">Dashboard</h1>
          <p class="subtitle">Bem-vindo de volta! Aqui está seu progresso</p>
        </div>
        <div class="header-actions">
          <div class="date-display">
            <i class="fas fa-calendar"></i>
            <span>30 Out, 2025</span>
          </div>
          <div class="avatar-wrap">
            <img class="avatar" src="/src/assets/logo.png" alt="Perfil" />
          </div>
        </div>
      </div>
    </header>

    <section class="stats-grid">
      <div class="stat-card primary-card">
        <div class="stat-header">
          <div class="stat-icon-wrap primary">
            <i class="fas fa-tasks"></i>
          </div>
          <span class="stat-label">Atividades Pendentes</span>
        </div>
        <div class="stat-value">5</div>
        <div class="stat-footer">
          <span class="stat-trend positive">+2 esta semana</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon-wrap">
            <i class="fas fa-clipboard-check"></i>
          </div>
          <span class="stat-label">Próxima Prova</span>
        </div>
        <div class="stat-value">02/12</div>
        <div class="stat-footer">
          <span class="stat-trend">Matemática Avançada</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon-wrap">
            <i class="fas fa-chart-line"></i>
          </div>
          <span class="stat-label">Desempenho Geral</span>
        </div>
        <div class="stat-value">85<span class="percent">%</span></div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: 85%"></div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <div class="stat-icon-wrap">
            <i class="fas fa-clock"></i>
          </div>
          <span class="stat-label">Tempo de Estudo</span>
        </div>
        <div class="stat-value">4h 20m</div>
        <div class="stat-footer">
          <span class="stat-trend positive">+1h vs semana passada</span>
        </div>
      </div>
    </section>

    <section class="content-grid">
      <div class="panel shortcuts-panel">
        <div class="panel-header">
          <h3 class="panel-title">Acesso Rápido</h3>
          <button class="icon-btn">
            <i class="fas fa-ellipsis-h"></i>
          </button>
        </div>
        <div class="shortcuts-grid">
          <router-link to="/aluno/activities" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-file-alt"></i>
            </div>
            <span class="shortcut-label">Atividades</span>
          </router-link>
          <router-link to="/aluno/exams" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-graduation-cap"></i>
            </div>
            <span class="shortcut-label">Provas</span>
          </router-link>
          <router-link to="/aluno/notes" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-sticky-note"></i>
            </div>
            <span class="shortcut-label">Anotações</span>
          </router-link>
          <router-link to="/aluno/classroom" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-chalkboard"></i>
            </div>
            <span class="shortcut-label">Minha Sala</span>
          </router-link>
          <router-link to="/aluno/chat" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-comments"></i>
            </div>
            <span class="shortcut-label">Chat</span>
          </router-link>
          <router-link to="/aluno/dots" class="shortcut-item">
            <div class="shortcut-icon">
              <i class="fas fa-trophy"></i>
            </div>
            <span class="shortcut-label">DOTS</span>
          </router-link>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">Resumo Semanal</h3>
          <button class="icon-btn">
            <i class="fas fa-sync-alt"></i>
          </button>
        </div>
        <div class="summary-list">
          <div class="summary-item">
            <div class="summary-info">
              <div class="summary-icon-wrap">
                <i class="fas fa-check-circle"></i>
              </div>
              <div>
                <p class="summary-label">Atividades Entregues</p>
                <p class="summary-sublabel">Esta semana</p>
              </div>
            </div>
            <span class="summary-value">7</span>
          </div>
          <div class="summary-item">
            <div class="summary-info">
              <div class="summary-icon-wrap">
                <i class="fas fa-book-open"></i>
              </div>
              <div>
                <p class="summary-label">Tempo de Estudo</p>
                <p class="summary-sublabel">Acumulado</p>
              </div>
            </div>
            <span class="summary-value">4h 20m</span>
          </div>
          <div class="summary-item">
            <div class="summary-info">
              <div class="summary-icon-wrap">
                <i class="fas fa-comments"></i>
              </div>
              <div>
                <p class="summary-label">Mensagens no Chat</p>
                <p class="summary-sublabel">Interações</p>
              </div>
            </div>
            <span class="summary-value">12</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.dashboard-root {
  min-height: 100vh;
  background: #17181e;
  color: #fcfcfc;
  padding: 2rem;
}

.header {
  margin-bottom: 2.5rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fcfcfc;
}

.date-display i {
  color: #3b82f6;
}

.avatar-wrap {
  position: relative;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  border: 2px solid #3b82f6;
  object-fit: cover;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.1);
}

.primary-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
  border-color: rgba(59, 130, 246, 0.3);
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-icon-wrap {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  font-size: 1.125rem;
  color: #3b82f6;
}

.stat-icon-wrap.primary {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.stat-label {
  font-size: 0.875rem;
  color: #8b92a8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 800;
  color: #fcfcfc;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.percent {
  font-size: 1.5rem;
  color: #8b92a8;
}

.stat-footer {
  margin-top: 0.5rem;
}

.stat-trend {
  font-size: 0.8125rem;
  color: #8b92a8;
  font-weight: 500;
}

.stat-trend.positive {
  color: #10b981;
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 0.75rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.panel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.panel-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #fcfcfc;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #8b92a8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fcfcfc;
}

.shortcuts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.shortcut-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.shortcut-item:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-2px);
}

.shortcut-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
  border-radius: 12px;
  font-size: 1.25rem;
  color: #3b82f6;
}

.shortcut-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #fcfcfc;
  text-align: center;
}

.summary-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.summary-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.summary-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.summary-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.summary-icon-wrap {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.15);
  border-radius: 10px;
  font-size: 1rem;
  color: #3b82f6;
}

.summary-label {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fcfcfc;
  margin-bottom: 0.25rem;
}

.summary-sublabel {
  font-size: 0.75rem;
  color: #8b92a8;
  font-weight: 500;
}

.summary-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #3b82f6;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .shortcuts-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .shortcuts-panel {
    order: 1;
  }
}
</style>