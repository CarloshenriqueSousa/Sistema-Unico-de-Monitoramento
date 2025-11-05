<template>
  <div class="showcase-view">
    <!-- Subtle Background -->
    <div class="subtle-bg">
      <div class="grid-overlay"></div>
    </div>

    <!-- Header -->
    <header :class="['header', { 'header-scrolled': scrolled }]">
      <nav class="nav-container">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#17181e" />
              <path d="M2 17L12 22L22 17" stroke="#17181e" stroke-width="2" />
            </svg>
          </div>
          <span class="logo-text">S.U.M</span>
        </div>
        
        <button @click="menuOpen = !menuOpen" class="menu-toggle">
          <span class="menu-line" :class="{ 'open': menuOpen }"></span>
          <span class="menu-line" :class="{ 'open': menuOpen }"></span>
          <span class="menu-line" :class="{ 'open': menuOpen }"></span>
        </button>
        
        <div class="nav-links">
          <a href="#features" class="nav-link">Funcionalidades</a>
          <a href="#profiles" class="nav-link">Dashboards</a>
          <a href="#about" class="nav-link">Sistema</a>
          <button class="btn-primary" @click="goToEntrar">
            <span>Acessar Sistema</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14m-7-7l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="status-dot"></span>
          <span>Sistema de Gestão Escolar Completo</span>
        </div>
        
        <h1 class="hero-title">
          Transforme sua
          <span class="highlight-text">Escola</span>
        </h1>
        
        <p class="hero-description">
          Gerencie alunos, professores e recursos com dashboards inteligentes, 
          mapeamento de salas e análises de produtividade em tempo real
        </p>
        
        <div class="hero-buttons">
          <button class="btn-primary btn-large" @click="goToEntrar">
            <span>Acessar Dashboard</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14m-7-7l7 7-7 7"/>
            </svg>
          </button>
          <button class="btn-secondary btn-large">
            <span>Ver Mapeamento 3D</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </button>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
          <div v-for="stat in stats" :key="stat.label" class="stat-card">
            <div class="stat-icon">
              <component :is="stat.icon" />
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="section-container">
        <div class="section-header">
          <div class="section-badge">Funcionalidades</div>
          <h2 class="section-title">Gestão Escolar Completa</h2>
          <p class="section-description">
            Dashboards inteligentes e mapeamento 3D para máxima produtividade
          </p>
        </div>

        <div class="features-grid">
          <div v-for="(feature, index) in features" :key="feature.title" class="feature-card">
            <div class="feature-number">{{ String(index + 1).padStart(2, '0') }}</div>
            <div class="feature-icon">
              <component :is="feature.icon" />
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
            <button class="feature-link">
              <span>Explorar</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14m-7-7l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section: Demos interativas do sistema -->
    <section id="demos" class="features-section">
      <div class="section-container">
        <div class="section-header">
          <div class="section-badge">Demonstrações</div>
          <h2 class="section-title">Mapeamento 3D e Dashboards</h2>
          <p class="section-description">
            Visualize o mapeamento 3D das salas, indicadores de produtividade e dados acadêmicos
          </p>
        </div>

        <div class="features-grid">
          <div class="feature-card three-beta-card">
            <div class="feature-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3h18v12H3z"/>
                <path d="M7 21h10"/>
              </svg>
            </div>
            <h3 class="feature-title">Mapeamento 2D (Beta)</h3>
            <p class="feature-description">Arraste e solte carteiras, defina grupos (1/2/3) e posicione o professor</p>

            <div class="three-container">
              <div style="display:flex; align-items:center; justify-content:space-between; gap: 0.75rem; margin-bottom: 0.5rem;">
                <MapToolbar :tool="tool"
                  @set-tool="(t: 'select'|'move')=> tool = t"
                  @rotate="actionRotate"
                  @delete="actionDelete"
                  @save="actionSave"
                  @load="actionLoad"
                  @export="actionExport"
                />
                <div style="display:flex; align-items:center; gap:0.5rem;">
                  <MapMini :seats="miniSeats" :teacher="miniTeacher" :sourceSize="{ width: 900, height: 520 }" />
                </div>
              </div>
              <div style="display:flex; gap:0.75rem; align-items:flex-start; margin-bottom: 0.5rem;">
                <MapConfig
                  :rows="rowsArray"
                  :teacherPos="teacherPos"
                  :teacherLabel="teacherLabel"
                  :background="mapBg"
                  :alternate="altColors"
                  :showNumbers="showNumbers"
                  :showBorders="showBorders"
                  @update:rows="(v: number[])=>{ rowsArray = v; syncRowsConfig() }"
                  @update:teacher-pos="(v: 'left'|'center'|'right'|'hidden')=>{ teacherPos = v }"
                  @update:teacher-label="(v: string)=>{ teacherLabel = v }"
                  @update:background="(v: string)=>{ mapBg = v }"
                  @update:alternate="(v: boolean)=>{ altColors = v }"
                  @update:show-numbers="(v: boolean)=>{ showNumbers = v }"
                  @update:show-borders="(v: boolean)=>{ showBorders = v }"
                  @distribute="(m: 'random'|'alpha'|'input'|'mix')=> mapRef?.distribute(m, rules)"
                  @apply-rules="(r: any)=> { rules = r; }"
                  @save-defaults="saveDefaults"
                  @load-defaults="loadDefaults"
                  @reset-layout="resetLayout"
                />
                <div style="display:flex; flex-direction:column; gap:0.5rem; min-width: 260px;">
                  <label class="overlay-label" style="margin-bottom:4px;">Lista de Alunos</label>
                  <textarea
                    class="students-box"
                    v-model="studentsRaw"
                    placeholder="Digite um aluno por linha. Opcional: use list:A para misturar listas.\nEx.:\nAna\nBruno list:A\nCarla list:B"
                  ></textarea>
                  <div style="display:flex; gap:0.5rem; flex-wrap: wrap;">
                    <button class="overlay-btn" @click="applyDistribution('random')">Aleatória</button>
                    <button class="overlay-btn" @click="applyDistribution('alpha')">Alfabética</button>
                    <button class="overlay-btn" @click="applyDistribution('input')">Entrada</button>
                    <button class="overlay-btn" @click="applyDistribution('mix')">Misturar Listas</button>
                  </div>
                  <button class="overlay-btn" @click="mapRef?.exportCsv()">Exportar CSV</button>
                  <button class="overlay-btn" @click="mapRef?.printMap()">Imprimir</button>
                </div>
              </div>
              <ClassroomMap2D
                ref="mapRef"
                :rows="rows2D"
                :cols="cols2D"
                :groupMode="groupMode2D"
                :snapToGrid="snap2D"
                :rowsConfig="rowsArray"
                :teacherArea="teacherPos"
                :teacherLabel="teacherLabel"
                :backgroundColor="mapBg"
                :alternateColors="altColors"
                :showNumbers="showNumbers"
                :showBorders="showBorders"
                :students="students"
                @update:teacher="(p)=>{ handleTeacherUpdate(p); miniTeacher = { x:p.x, y:p.y, w:42, h:42 } }"
                @update:seats="(s)=>{ handleSeatsUpdate(s); updateMini(s) }"
              />
            </div>
          </div>
          

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3v18h18"/>
                <path d="M7 15l4-4 4 4 5-5"/>
              </svg>
            </div>
            <h3 class="feature-title">Produtividade</h3>
            <p class="feature-description">Evolução de produtividade por período</p>
            <InteractiveChart
              :title="'Produtividade'"
              :subtitle="'Visão geral semanal'"
              type="line"
              :chartTypes="['line','bar','area']"
              :data="productivityChart"
              :options="{}"
              :showLegend="false"
              :realTime="true"
              :updateInterval="2000"
              :gradientFill="true"
              :showGrid="true"
              :animated="true"
              @point-click="handleChartClick"
            />
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            </div>
            <h3 class="feature-title">Competências</h3>
            <p class="feature-description">Radar de competências acadêmicas</p>
            <SkillRadar
              :title="'Desempenho por Competência'"
              :skills="radarSkills"
              :size="340"
              :levels="5"
              :showLegend="false"
              :animated="true"
              :interactive="true"
              :showValues="true"
              :colorScheme="'gradient'"
              :glow="true"
              @skill-click="handleSkillClick"
            />
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M3 12h18M3 18h18"/>
              </svg>
            </div>
            <h3 class="feature-title">Turmas e Salas</h3>
            <p class="feature-description">Tabela dinâmica de turmas e professores</p>
            <DynamicTable
              :title="'Turmas'"
              :columns="tableColumns"
              :data="tableData"
              :searchable="true"
              :paginated="true"
              :perPage="5"
              :selectable="true"
              :multiSelect="true"
              :exportable="true"
              :refreshable="true"
              :striped="true"
              :hoverable="true"
              :showSummary="true"
              :summaryColumns="['students']"
              @row-click="handleTableRowClick"
              @selection-change="handleTableSelection"
              @export="handleTableExport"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Profiles Section -->
    <section id="profiles" class="profiles-section">
      <div class="section-container">
        <div class="section-header">
          <div class="section-badge">Perfis</div>
          <h2 class="section-title">Dashboards Personalizados</h2>
          <p class="section-description">
            Cada perfil tem acesso a funcionalidades específicas de gestão
          </p>
        </div>

        <div class="profiles-grid">
          <div 
            v-for="profile in profiles" 
            :key="profile.id"
            class="profile-card"
            :class="{ 'active': activeProfile === profile.id }"
            @mouseenter="activeProfile = profile.id"
            @mouseleave="activeProfile = null"
          >
            <div class="profile-content">
              <div class="profile-header">
                <div class="profile-icon">
                  <component :is="profile.icon" />
                </div>
                <div class="profile-badge">{{ profile.badge }}</div>
              </div>
              
              <h3 class="profile-name">{{ profile.name }}</h3>
              <p class="profile-description">{{ profile.description }}</p>
              
              <div class="profile-stats">
                <div v-for="stat in profile.stats" :key="stat.label" class="profile-stat">
                  <div class="stat-icon-small">
                    <component :is="stat.icon" />
                  </div>
                  <div class="stat-info">
                    <span class="stat-label-small">{{ stat.label }}</span>
                    <span class="stat-value-small">{{ stat.value }}</span>
                  </div>
                </div>
              </div>
              
              <button class="profile-button">
                <span>Ver Dashboard</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14m-7-7l7 7-7 7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <div class="cta-badge">
          <span class="status-dot"></span>
          <span>Comece Hoje</span>
        </div>
        
        <h2 class="cta-title">
          Pronto para revolucionar a gestão da sua escola?
        </h2>
        
        <p class="cta-description">
          Aumente a produtividade e eficiência com dashboards inteligentes e mapeamento 3D
        </p>
        
        <div class="cta-buttons">
          <button class="btn-cta">
            <span>Testar Sistema</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14m-7-7l7 7-7 7"/>
            </svg>
          </button>
          <button class="btn-cta-secondary">
            <span>Ver Mapeamento 3D</span>
          </button>
        </div>

        <div class="cta-features">
          <div class="cta-feature">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Gestão completa</span>
          </div>
          <div class="cta-feature">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Mapeamento 3D</span>
          </div>
          <div class="cta-feature">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Dashboards inteligentes</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-top">
          <div class="footer-brand">
            <div class="logo-section">
              <div class="logo-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="#17181e" />
                  <path d="M2 17L12 22L22 17" stroke="#17181e" stroke-width="2" />
                </svg>
              </div>
              <span class="logo-text">S.U.M</span>
            </div>
            <p class="footer-description">
              Sistema de Gestão Escolar<br/>
              Dashboards e mapeamento 3D
            </p>
          </div>

          <div class="footer-links-group">
            <div class="footer-column">
              <h4>Sistema</h4>
              <a href="#">Dashboards</a>
              <a href="#">Mapeamento 3D</a>
              <a href="#">Gestão</a>
              <a href="#">Relatórios</a>
            </div>
            <div class="footer-column">
              <h4>Escola</h4>
              <a href="#">Professores</a>
              <a href="#">Alunos</a>
              <a href="#">Turmas</a>
              <a href="#">Calendário</a>
            </div>
            <div class="footer-column">
              <h4>Suporte</h4>
              <a href="#">Documentação</a>
              <a href="#">Tutorial</a>
              <a href="#">Contato</a>
              <a href="#">FAQ</a>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; 2025 S.U.M. Todos os direitos reservados.</p>
          <div class="social-links">
            <a href="#" class="social-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="#" class="social-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a href="#" class="social-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, defineComponent, h } from 'vue'
import { useRouter } from 'vue-router'
// @ts-ignore
// 2D mapping demo component
import ClassroomMap2D from '@/components/classroom/ClassroomMap2D.vue'
import MapToolbar from '@/components/classroom/MapToolbar.vue'
import MapMini from '@/components/classroom/MapMini.vue'
import InteractiveChart from '@/shared/InteractiveChart.vue'
import MapConfig from '@/components/classroom/MapConfig.vue'
import SkillRadar from '@/shared/SkillRadar.vue'
import DynamicTable from '@/shared/DynamicTable.vue'

// Icons - Minimalistas
const BarChartIcon = defineComponent({
  render: () => h('svg', { width: 22, height: 22, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('line', { x1: 12, y1: 20, x2: 12, y2: 10 }),
    h('line', { x1: 18, y1: 20, x2: 18, y2: 4 }),
    h('line', { x1: 6, y1: 20, x2: 6, y2: 16 })
  ])
})

const FileTextIcon = defineComponent({
  render: () => h('svg', { width: 22, height: 22, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
    h('polyline', { points: '14 2 14 8 20 8' })
  ])
})

const TrendingUpIcon = defineComponent({
  render: () => h('svg', { width: 22, height: 22, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polyline', { points: '23 6 13.5 15.5 8.5 10.5 1 18' }),
    h('polyline', { points: '17 6 23 6 23 12' })
  ])
})

const CalendarIcon = defineComponent({
  render: () => h('svg', { width: 22, height: 22, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('rect', { x: 3, y: 4, width: 18, height: 18, rx: 2, ry: 2 }),
    h('line', { x1: 16, y1: 2, x2: 16, y2: 6 }),
    h('line', { x1: 8, y1: 2, x2: 8, y2: 6 })
  ])
})

const BookOpenIcon = defineComponent({
  render: () => h('svg', { width: 26, height: 26, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z' }),
    h('path', { d: 'M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z' })
  ])
})

const UsersIcon = defineComponent({
  render: () => h('svg', { width: 26, height: 26, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: 9, cy: 7, r: 4 })
  ])
})

const SchoolIcon = defineComponent({
  render: () => h('svg', { width: 26, height: 26, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M22 10v6M2 10l10-5 10 5-10 5z' }),
    h('path', { d: 'M6 12v5c3 3 9 3 12 0v-5' })
  ])
})

const SettingsIcon = defineComponent({
  render: () => h('svg', { width: 26, height: 26, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('circle', { cx: 12, cy: 12, r: 3 }),
    h('path', { d: 'M12 1v6m0 6v6' })
  ])
})

const SmallFileIcon = defineComponent({
  render: () => h('svg', { width: 14, height: 14, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' })
  ])
})

const SmallTrendIcon = defineComponent({
  render: () => h('svg', { width: 14, height: 14, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polyline', { points: '23 6 13.5 15.5 8.5 10.5 1 18' })
  ])
})

const SmallUsersIcon = defineComponent({
  render: () => h('svg', { width: 14, height: 14, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('circle', { cx: 9, cy: 7, r: 4 })
  ])
})

// removed UsersGroupIcon (unused)

const CheckIcon = defineComponent({
  render: () => h('svg', { width: 18, height: 18, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polyline', { points: '20 6 9 17 4 12' })
  ])
})

const ClockIcon = defineComponent({
  render: () => h('svg', { width: 18, height: 18, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('circle', { cx: 12, cy: 12, r: 10 }),
    h('polyline', { points: '12 6 12 12 16 14' })
  ])
})

const scrolled = ref(false)
const menuOpen = ref(false)
const activeProfile = ref<string | null>(null)
const router = useRouter()
const goToEntrar = () => router.push('/entrar')

// Demo data for InteractiveChart
const productivityChart = {
  labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],
  datasets: [
    { 
      label: 'Produtividade', 
      data: [62, 68, 75, 80, 88], 
      borderColor: '#2d531a', 
      backgroundColor: '#2d531a',
      fill: true,
      tension: 0.4
    },
    { 
      label: 'Meta', 
      data: [70, 70, 70, 70, 70], 
      borderColor: '#e1d4c2', 
      backgroundColor: '#e1d4c2',
      borderDash: [5, 5],
      fill: false
    }
  ]
}

// Demo data for SkillRadar
const radarSkills = [
  { name: 'Frequência', value: 85, color: '#2d531a' },
  { name: 'Entrega', value: 78, color: '#0f1e3f' },
  { name: 'Participação', value: 72, color: '#e1d4c2' },
  { name: 'Notas', value: 80, color: '#2d531a' },
  { name: 'Evolução', value: 90, color: '#0f1e3f' },
  { name: 'Colaboração', value: 75, color: '#e1d4c2' }
]

// Removed 3D sim controls

// Demo data for DynamicTable
const tableColumns = [
  { key: 'turma', label: 'Turma', sortable: true, type: 'text' },
  { key: 'professor', label: 'Professor', sortable: true, type: 'text' },
  { key: 'sala', label: 'Sala', sortable: true, type: 'text' },
  { key: 'horario', label: 'Horário', sortable: true, type: 'text' },
  { key: 'students', label: 'Alunos', sortable: true, type: 'number' },
  { key: 'status', label: 'Status', sortable: true, type: 'text' }
]

const tableData = [
  { turma: '9º A', professor: 'Prof. Silva', sala: 'Sala 12', horario: '08:00', students: 30, status: 'Ativa' },
  { turma: '8º B', professor: 'Prof. Costa', sala: 'Sala 08', horario: '09:00', students: 28, status: 'Ativa' },
  { turma: '7º C', professor: 'Prof. Santos', sala: 'Sala 05', horario: '10:00', students: 32, status: 'Inativa' },
  { turma: '6º A', professor: 'Profª. Lima', sala: 'Sala 02', horario: '11:00', students: 25, status: 'Ativa' },
  { turma: '5º B', professor: 'Prof. Rocha', sala: 'Sala 01', horario: '13:00', students: 27, status: 'Ativa' },
  { turma: '4º A', professor: 'Profª. Oliveira', sala: 'Sala 03', horario: '14:00', students: 24, status: 'Ativa' },
  { turma: '3º B', professor: 'Prof. Ferreira', sala: 'Sala 06', horario: '15:00', students: 26, status: 'Ativa' },
  { turma: '2º A', professor: 'Profª. Almeida', sala: 'Sala 04', horario: '16:00', students: 23, status: 'Ativa' }
]

// Event handlers
const handleChartClick = (data: any) => {
  console.log('Chart point clicked:', data)
  // Add any chart interaction logic here
}

const handleSkillClick = (skill: any, index: number) => {
  console.log('Skill clicked:', skill, index)
  // Add any skill interaction logic here
}

const handleTableRowClick = (row: any, index: number) => {
  console.log('Table row clicked:', row, index)
  // Add any table row interaction logic here
}

const handleTableSelection = (selectedRows: any[]) => {
  console.log('Table selection changed:', selectedRows)
  // Add any selection logic here
}

const handleTableExport = (format: string) => {
  console.log('Table export requested:', format)
  // Add export logic here
}

const stats = [
  { value: '+40%', label: 'Produtividade', icon: TrendingUpIcon },
  { value: '95%', label: 'Gestão Eficiente', icon: CheckIcon },
  { value: '100%', label: 'Controle Total', icon: ClockIcon },
  { value: '24h', label: 'Monitoramento', icon: SchoolIcon }
]

const features = [
  {
    title: 'Dashboard de Gestão',
    description: 'Controle total da escola com métricas de produtividade, frequência e desempenho em tempo real',
    icon: BarChartIcon
  },
  {
    title: 'Mapeamento 3D de Salas',
    description: 'Visualize e gerencie o layout das salas de aula com tecnologia 3D interativa',
    icon: FileTextIcon
  },
  {
    title: 'Gestão de Professores',
    description: 'Monitore carga horária, planejamentos e produtividade dos educadores',
    icon: TrendingUpIcon
  },
  {
    title: 'Controle de Alunos',
    description: 'Acompanhe frequência, notas e desenvolvimento acadêmico de cada estudante',
    icon: CalendarIcon
  }
]

const profiles = [
  {
    id: 'aluno',
    name: 'Aluno',
    icon: BookOpenIcon,
    description: 'Acompanhe suas notas, frequência e atividades em tempo real',
    badge: 'Estudante',
    stats: [
      { label: 'Notas', value: 'A+', icon: SmallFileIcon },
      { label: 'Frequência', value: '95%', icon: SmallTrendIcon }
    ]
  },
  {
    id: 'professor',
    name: 'Professor',
    icon: UsersIcon,
    description: 'Gerencie suas turmas, planejamentos e produtividade',
    badge: 'Educador',
    stats: [
      { label: 'Turmas', value: '4', icon: SmallUsersIcon },
      { label: 'Alunos', value: '120', icon: SmallFileIcon }
    ]
  },
  {
    id: 'coordenador',
    name: 'Coordenador',
    icon: SchoolIcon,
    description: 'Monitore professores e alunos com dashboards de gestão',
    badge: 'Gestão',
    stats: [
      { label: 'Professores', value: '25', icon: SmallUsersIcon },
      { label: 'Turmas', value: '15', icon: SmallTrendIcon }
    ]
  },
  {
    id: 'diretor',
    name: 'Diretor',
    icon: SettingsIcon,
    description: 'Controle total da escola com métricas de produtividade',
    badge: 'Administração',
    stats: [
      { label: 'Escola', value: '1', icon: SmallUsersIcon },
      { label: 'Alunos', value: '500+', icon: SmallTrendIcon }
    ]
  }
]

const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// 2D Mapping State (controls wired in Showcase)
const rows2D = ref(5)
const cols2D = ref(8)
const groupMode2D = ref<'single'|'duo'|'trio'>('single')
const snap2D = ref(true)
const lastTeacherPos = ref<{ x: number; y: number } | null>(null)
const handleTeacherUpdate = (p: { x: number; y: number }) => lastTeacherPos.value = p
const handleSeatsUpdate = (_: any) => {}

const mapRef = ref<InstanceType<typeof ClassroomMap2D> | null>(null)
const tool = ref<'select'|'move'>('select')
const actionRotate = () => mapRef.value?.rotateSelection()
const actionDelete = () => mapRef.value?.deleteSelection()
const actionSave = () => mapRef.value?.saveLayout()
const actionLoad = () => mapRef.value?.loadLayout()
const actionExport = () => mapRef.value?.exportPng()
const miniSeats = ref<Array<{ x:number;y:number;w:number;h:number }>>([])
const miniTeacher = ref<{ x:number;y:number;w:number;h:number }>({ x:0,y:0,w:0,h:0 })
const updateMini = (seats:any[]) => { miniSeats.value = seats.map(s=>({ x:s.x,y:s.y,w:s.w,h:s.h })) }

// Advanced config state
let rowsArray = ref<number[]>([8,8,8,8,8])
let teacherPos = ref<'left'|'center'|'right'|'hidden'>('center')
let teacherLabel = ref('Professor')
let mapBg = ref('#ffffff')
let altColors = ref(true)
let showNumbers = ref(true)
let showBorders = ref(true)
let rules = {} as any

// Students input and parsing
const studentsRaw = ref('')
const students = ref<Array<{ name:string; list?:string }>>([])
function parseStudents(raw:string) {
  const lines = (raw || '').split(/\r?\n/)
  const res: Array<{ name:string; list?:string }> = []
  for (const line of lines) {
    const t = line.trim()
    if (!t) continue
    const m = t.match(/^(.*?)(?:\s+list:([A-Za-z0-9_-]+))?$/)
    if (m) {
      const name = m[1].trim()
      const list = m[2]?.trim()
      if (name) res.push(list ? { name, list } : { name })
    }
  }
  return res
}
function applyDistribution(method:'random'|'alpha'|'input'|'mix') {
  students.value = parseStudents(studentsRaw.value)
  mapRef.value?.distribute(method, rules)
}

function syncRowsConfig() {
  // keep rows2D in sync with number of configured rows if needed
  rows2D.value = rowsArray.value.length
}

function saveDefaults() {
  const data = {
    rowsArray: rowsArray.value,
    teacherPos: teacherPos.value,
    teacherLabel: teacherLabel.value,
    mapBg: mapBg.value,
    altColors: altColors.value,
    showNumbers: showNumbers.value,
    showBorders: showBorders.value,
  }
  localStorage.setItem('sum-map-defaults', JSON.stringify(data))
}

function loadDefaults() {
  const raw = localStorage.getItem('sum-map-defaults')
  if (!raw) return
  try {
    const d = JSON.parse(raw)
    if (Array.isArray(d.rowsArray)) rowsArray.value = d.rowsArray
    if (d.teacherPos) teacherPos.value = d.teacherPos
    if (d.teacherLabel) teacherLabel.value = d.teacherLabel
    if (d.mapBg) mapBg.value = d.mapBg
    if (typeof d.altColors === 'boolean') altColors.value = d.altColors
    if (typeof d.showNumbers === 'boolean') showNumbers.value = d.showNumbers
    if (typeof d.showBorders === 'boolean') showBorders.value = d.showBorders
    syncRowsConfig()
  } catch {}
}

function resetLayout() {
  rowsArray.value = [8,8,8,8,8]
  teacherPos.value = 'center'
  teacherLabel.value = 'Professor'
  mapBg.value = '#ffffff'
  altColors.value = true
  showNumbers.value = true
  showBorders.value = true
  syncRowsConfig()
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.showcase-view {
  min-height: 100vh;
  background: #fcfcfc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  overflow-x: hidden;
}

/* Subtle Background */
.subtle-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  background: #fcfcfc;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(23, 24, 30, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(23, 24, 30, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* Header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(252, 252, 252, 0.8);
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
}

.header-scrolled {
  border-bottom: 1px solid rgba(23, 24, 30, 0.08);
  box-shadow: 0 1px 3px rgba(23, 24, 30, 0.04);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo-section:hover {
  opacity: 0.7;
}

.logo-icon {
  width: 38px;
  height: 38px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.logo-section:hover .logo-icon {
  border-color: rgba(23, 24, 30, 0.2);
}

.logo-text {
  font-size: 1.35rem;
  font-weight: 700;
  color: #17181e;
  letter-spacing: -0.01em;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.menu-line {
  width: 24px;
  height: 2px;
  background: #17181e;
  transition: all 0.3s;
  border-radius: 2px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.nav-link {
  color: #6b6b6b;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  position: relative;
  transition: color 0.2s;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 1.5px;
  background: #17181e;
  transition: width 0.3s;
}

.nav-link:hover {
  color: #17181e;
}

.nav-link:hover::after {
  width: 100%;
}

.btn-primary {
  padding: 0.7rem 1.5rem;
  background: #17181e;
  color: #fcfcfc;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(23, 24, 30, 0.15);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  padding: 0.7rem 1.5rem;
  background: #fcfcfc;
  color: #17181e;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: rgba(23, 24, 30, 0.25);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(23, 24, 30, 0.08);
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 0.95rem;
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  padding: 10rem 2rem 6rem;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 1200px;
  width: 100%;
  position: relative;
  z-index: 10;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: #fcfcfc;
  padding: 0.6rem 1.2rem;
  border-radius: 100px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  margin-bottom: 2.5rem;
  font-size: 0.85rem;
  color: #6b6b6b;
  transition: all 0.2s;
}

.hero-badge:hover {
  border-color: rgba(23, 24, 30, 0.15);
}

.status-dot {
  width: 7px;
  height: 7px;
  background: #10b981;
  border-radius: 50%;
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 800;
  color: #17181e;
  margin-bottom: 2rem;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.highlight-text {
  display: block;
  color: #17181e;
  position: relative;
}

.highlight-text::after {
  content: '';
  position: absolute;
  bottom: 8px;
  left: 0;
  right: 0;
  height: 12px;
  background: rgba(59, 130, 246, 0.12);
  z-index: -1;
}

.hero-description {
  font-size: 1.2rem;
  color: #6b6b6b;
  max-width: 700px;
  margin: 0 auto 3rem;
  line-height: 1.7;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 5rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  max-width: 1100px;
  margin: 0 auto;
}

.stat-card {
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(23, 24, 30, 0.15);
  box-shadow: 0 8px 24px rgba(23, 24, 30, 0.08);
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: #17181e;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  flex-shrink: 0;
  transition: transform 0.3s;
}

.stat-card:hover .stat-icon {
  transform: scale(1.05);
}

.stat-content {
  flex: 1;
  text-align: left;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #17181e;
  margin-bottom: 0.25rem;
  line-height: 1;
}

.stat-label {
  font-size: 0.85rem;
  color: #6b6b6b;
  font-weight: 500;
}

/* Features Section */
.features-section {
  padding: 6rem 2rem;
  background: #fcfcfc;
  position: relative;
  z-index: 10;
}

.section-container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 100px;
  color: #17181e;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  color: #17181e;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-description {
  font-size: 1.1rem;
  color: #6b6b6b;
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.7;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: #fcfcfc;
  padding: 2.5rem;
  border-radius: 20px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-6px);
  border-color: rgba(23, 24, 30, 0.15);
  box-shadow: 0 12px 32px rgba(23, 24, 30, 0.1);
}

.feature-number {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  font-size: 2.5rem;
  font-weight: 800;
  color: rgba(23, 24, 30, 0.04);
  line-height: 1;
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: #17181e;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  margin-bottom: 2rem;
  transition: transform 0.3s;
}

.feature-card:hover .feature-icon {
  transform: scale(1.05);
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #17181e;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.feature-description {
  color: #6b6b6b;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.feature-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  background: none;
  border: none;
  color: #17181e;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.feature-link:hover {
  gap: 0.75rem;
}

/* Three.js Beta Preview */
.three-beta-card {
  grid-column: span 2;
}

.three-container {
  position: relative;
  width: 100%;
  height: 420px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 14px;
  overflow: hidden;
  background: #fcfcfc;
}

.overlay-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(252, 252, 252, 0.8);
  border: 1px solid rgba(23, 24, 30, 0.08);
  border-radius: 12px;
  padding: 6px 8px;
  backdrop-filter: blur(12px);
}

.overlay-label {
  font-size: 0.75rem;
  color: #6b6b6b;
  padding: 4px 8px;
}

.overlay-group {
  display: flex;
  gap: 6px;
}

.overlay-btn {
  padding: 6px 10px;
  font-size: 0.8rem;
  border-radius: 10px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  color: #17181e;
  cursor: pointer;
  transition: all 0.2s;
}

.overlay-btn:hover {
  border-color: rgba(23, 24, 30, 0.25);
  transform: translateY(-1px);
}

.overlay-btn.active {
  background: #17181e;
  color: #fcfcfc;
  border-color: #17181e;
}

.overlay-select {
  padding: 6px 10px;
  font-size: 0.8rem;
  border-radius: 10px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  color: #17181e;
}

.students-box {
  width: 100%;
  min-height: 100px;
  padding: 8px 10px;
  border-radius: 10px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85rem;
  color: #17181e;
}

.three-fallback {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(23, 24, 30, 0.02), rgba(23, 24, 30, 0));
}

.fallback-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.1);
  border-radius: 12px;
  padding: 0.8rem 1rem;
}

.fallback-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
}

.fallback-title {
  font-weight: 700;
  color: #17181e;
  font-size: 0.95rem;
}

.fallback-desc {
  color: #6b6b6b;
  font-size: 0.8rem;
}

/* Profiles Section */
.profiles-section {
  padding: 6rem 2rem;
  background: #f8f8f8;
  position: relative;
  z-index: 10;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.profile-card {
  background: #fcfcfc;
  border-radius: 20px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.profile-card:hover,
.profile-card.active {
  transform: translateY(-6px);
  border-color: rgba(23, 24, 30, 0.15);
  box-shadow: 0 12px 32px rgba(23, 24, 30, 0.1);
}

.profile-content {
  padding: 2.5rem;
  position: relative;
  z-index: 2;
}

.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.profile-icon {
  width: 64px;
  height: 64px;
  background: #17181e;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  transition: transform 0.3s;
}

.profile-card:hover .profile-icon,
.profile-card.active .profile-icon {
  transform: scale(1.05);
}

.profile-badge {
  padding: 0.35rem 0.8rem;
  background: rgba(23, 24, 30, 0.06);
  border-radius: 100px;
  color: #17181e;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.profile-name {
  font-size: 1.6rem;
  font-weight: 800;
  color: #17181e;
  margin-bottom: 1rem;
  letter-spacing: -0.01em;
}

.profile-description {
  color: #6b6b6b;
  margin-bottom: 2rem;
  line-height: 1.7;
  font-size: 0.9rem;
}

.profile-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(23, 24, 30, 0.02);
  border-radius: 12px;
}

.profile-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon-small {
  width: 36px;
  height: 36px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #17181e;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.stat-label-small {
  font-size: 0.75rem;
  color: #6b6b6b;
  font-weight: 500;
}

.stat-value-small {
  font-size: 1rem;
  font-weight: 700;
  color: #17181e;
}

.profile-button {
  width: 100%;
  padding: 1rem;
  background: #17181e;
  color: #fcfcfc;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.profile-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(23, 24, 30, 0.2);
}

/* CTA Section */
.cta-section {
  padding: 6rem 2rem;
  background: #fcfcfc;
  position: relative;
  z-index: 10;
}

.cta-content {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
}

.cta-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background: #fcfcfc;
  padding: 0.6rem 1.2rem;
  border-radius: 100px;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  margin-bottom: 2rem;
  font-size: 0.85rem;
  color: #6b6b6b;
}

.cta-title {
  font-size: 3rem;
  font-weight: 800;
  color: #17181e;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 1.15rem;
  color: #6b6b6b;
  margin-bottom: 2.5rem;
  line-height: 1.7;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.btn-cta {
  padding: 1.1rem 2.2rem;
  background: #17181e;
  color: #fcfcfc;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(23, 24, 30, 0.2);
}

.btn-cta-secondary {
  padding: 1.1rem 2.2rem;
  background: #fcfcfc;
  color: #17181e;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cta-secondary:hover {
  border-color: rgba(23, 24, 30, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(23, 24, 30, 0.08);
}

.cta-features {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: #6b6b6b;
  font-size: 0.9rem;
  font-weight: 500;
}

.cta-feature svg {
  color: #10b981;
  flex-shrink: 0;
}

/* Footer */
.footer {
  padding: 4rem 2rem 2rem;
  background: #f8f8f8;
  border-top: 1.5px solid rgba(23, 24, 30, 0.06);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-top {
  display: grid;
  grid-template-columns: 1.5fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand .logo-section {
  margin-bottom: 1rem;
}

.footer-description {
  color: #6b6b6b;
  font-size: 0.9rem;
  line-height: 1.7;
}

.footer-links-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-column h4 {
  color: #17181e;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.footer-column a {
  display: block;
  color: #6b6b6b;
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  transition: color 0.2s;
}

.footer-column a:hover {
  color: #17181e;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1.5px solid rgba(23, 24, 30, 0.06);
}

.footer-bottom p {
  color: #6b6b6b;
  font-size: 0.85rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.08);
  border-radius: 8px;
  color: #6b6b6b;
  transition: all 0.2s;
}

.social-link:hover {
  color: #17181e;
  border-color: rgba(23, 24, 30, 0.15);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
  }
  
  .nav-links {
    display: none;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .section-title {
    font-size: 2.2rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
  
  .footer-top {
    grid-template-columns: 1fr;
  }
  
  .footer-links-group {
    grid-template-columns: 1fr;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
}
</style>