<template>
  <div class="exams-root">
    <div class="container">
      <div class="header">
        <div>
          <h1 class="title">Provas Opcionais</h1>
          <p class="subtitle">Teste seus conhecimentos e ganhe pontos DOTS</p>
        </div>
        <div class="stats-mini">
          <div class="stat-mini">
            <i class="fas fa-trophy"></i>
            <span>225 pts</span>
          </div>
        </div>
      </div>

      <div class="content-grid">
        <div class="main-section">
          <div class="section-header">
            <h2 class="section-title">Provas Disponíveis</h2>
            <div class="filter-group">
              <button class="filter-btn active">Todas</button>
              <button class="filter-btn">Fácil</button>
              <button class="filter-btn">Médio</button>
              <button class="filter-btn">Difícil</button>
            </div>
          </div>

          <div class="exams-grid">
            <div class="exam-card">
              <div class="exam-header">
                <div class="difficulty-badge easy">Fácil</div>
                <div class="points-badge">
                  <i class="fas fa-star"></i>
                  <span>50 pts</span>
                </div>
              </div>
              <h3 class="exam-title">Matemática Básica</h3>
              <p class="exam-description">Fundamentos de álgebra e aritmética</p>
              <div class="exam-info">
                <div class="info-item">
                  <i class="fas fa-clock"></i>
                  <span>60 min</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-question-circle"></i>
                  <span>20 questões</span>
                </div>
              </div>
              <button class="start-btn">
                <span>Iniciar Prova</span>
                <i class="fas fa-arrow-right"></i>
              </button>
            </div>

            <div class="exam-card">
              <div class="exam-header">
                <div class="difficulty-badge medium">Médio</div>
                <div class="points-badge">
                  <i class="fas fa-star"></i>
                  <span>75 pts</span>
                </div>
              </div>
              <h3 class="exam-title">Literatura Brasileira</h3>
              <p class="exam-description">Movimentos literários e autores clássicos</p>
              <div class="exam-info">
                <div class="info-item">
                  <i class="fas fa-clock"></i>
                  <span>45 min</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-question-circle"></i>
                  <span>15 questões</span>
                </div>
              </div>
              <button class="start-btn">
                <span>Iniciar Prova</span>
                <i class="fas fa-arrow-right"></i>
              </button>
            </div>

            <div class="exam-card">
              <div class="exam-header">
                <div class="difficulty-badge hard">Difícil</div>
                <div class="points-badge">
                  <i class="fas fa-star"></i>
                  <span>100 pts</span>
                </div>
              </div>
              <h3 class="exam-title">Termodinâmica Avançada</h3>
              <p class="exam-description">Leis da termodinâmica e aplicações</p>
              <div class="exam-info">
                <div class="info-item">
                  <i class="fas fa-clock"></i>
                  <span>90 min</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-question-circle"></i>
                  <span>25 questões</span>
                </div>
              </div>
              <button class="start-btn">
                <span>Iniciar Prova</span>
                <i class="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <div class="panel">
            <h3 class="panel-title">Minhas Tentativas</h3>
            <div class="attempts-list">
              <div class="attempt-item">
                <div class="attempt-info">
                  <h4 class="attempt-title">Matemática Básica</h4>
                  <span class="attempt-date">20 Out, 2025</span>
                </div>
                <div class="attempt-score">85%</div>
              </div>
              <div class="attempt-item">
                <div class="attempt-info">
                  <h4 class="attempt-title">Literatura Brasileira</h4>
                  <span class="attempt-date">18 Out, 2025</span>
                </div>
                <div class="attempt-score">70%</div>
              </div>
            </div>
          </div>

          <div class="panel">
            <h3 class="panel-title">Criar Prova Personalizada</h3>
            <p class="panel-description">Monte sua própria prova com questões selecionadas</p>
            <button class="action-btn-full">
              <i class="fas fa-plus"></i>
              <span>Criar Prova</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.exams-root {
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

.stats-mini {
  display: flex;
  gap: 1rem;
}

.stat-mini {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  color: #3b82f6;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fcfcfc;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  color: #8b92a8;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filter-btn.active {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.exams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}

.exam-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.exam-card:hover {
  transform: translateY(-4px);
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
}

.exam-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.difficulty-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.difficulty-badge.easy {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.difficulty-badge.medium {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.difficulty-badge.hard {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.points-badge {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: rgba(139, 92, 246, 0.15);
  border-radius: 8px;
  color: #a78bfa;
  font-size: 0.875rem;
  font-weight: 700;
}

.exam-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 0.5rem;
}

.exam-description {
  font-size: 0.9375rem;
  color: #8b92a8;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.exam-info {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #8b92a8;
  font-weight: 600;
}

.info-item i {
  color: #3b82f6;
}

.start-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 0.875rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.panel {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
}

.panel-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #fcfcfc;
  margin-bottom: 1rem;
}

.panel-description {
  font-size: 0.875rem;
  color: #8b92a8;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.attempts-list {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.attempt-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

.attempt-info h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fcfcfc;
  margin-bottom: 0.25rem;
}

.attempt-date {
  font-size: 0.75rem;
  color: #8b92a8;
}

.attempt-score {
  font-size: 1.25rem;
  font-weight: 700;
  color: #3b82f6;
}

.action-btn-full {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  padding: 0.875rem;
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  color: #3b82f6;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn-full:hover {
  background: rgba(59, 130, 246, 0.25);
}

@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .exams-root {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .exams-grid {
    grid-template-columns: 1fr;
  }
}
</style>