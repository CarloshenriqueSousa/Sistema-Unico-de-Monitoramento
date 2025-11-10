 

<style scoped>
/* Reset & Base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.showcase-container {
  min-height: 100vh;
  background: #fcfcfc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif;
  overflow-x: hidden;
  position: relative;
}

/* Animated Background */
.animated-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #fcfcfc 0%, #f5f5f5 100%);
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  top: -250px;
  right: -250px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #10b981, #059669);
  bottom: -200px;
  left: -200px;
  animation-delay: 5s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  top: 50%;
  left: 50%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 20px) scale(0.9); }
  75% { transform: translate(20px, 30px) scale(1.05); }
}

.mesh-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(23, 24, 28, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(23, 24, 28, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* Navigation */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(252, 252, 252, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-bar.scrolled {
  background: rgba(252, 252, 252, 0.9);
  border-bottom-color: rgba(23, 24, 28, 0.1);
  box-shadow: 0 4px 24px rgba(23, 24, 28, 0.06);
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-badge {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #17181c 0%, #2d2f36 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.12);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.logo-badge:hover {
  transform: translateY(-2px) scale(1.05);
}

.logo-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #17181c;
  letter-spacing: -0.02em;
}

.logo-tag {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
  background: rgba(23, 24, 28, 0.05);
  border-radius: 6px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.nav-link {
  position: relative;
  color: #6b7280;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-link span {
  position: relative;
  z-index: 1;
}

.link-indicator {
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #10b981);
  border-radius: 2px;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover {
  color: #17181c;
}

.nav-link:hover .link-indicator {
  width: 100%;
}

.btn-access {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #17181c 0%, #2d2f36 100%);
  color: #fcfcfc;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.15);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-access:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(23, 24, 28, 0.25);
}

.mobile-menu {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-menu span {
  width: 24px;
  height: 2px;
  background: #17181c;
  border-radius: 2px;
  transition: all 0.3s;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  padding: 10rem 2rem 6rem;
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1400px;
  margin: 0 auto;
  align-items: center;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.75rem 1.5rem;
  border-radius: 100px;
  border: 1px solid rgba(23, 24, 28, 0.1);
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 600;
  width: fit-content;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.06);
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.hero-title {
  font-size: 5rem;
  font-weight: 900;
  color: #17181c;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.gradient-text {
  display: block;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.hero-desc {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.7;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 1.25rem 2.5rem;
  background: linear-gradient(135deg, #17181c 0%, #2d2f36 100%);
  color: #fcfcfc;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 8px 24px rgba(23, 24, 28, 0.2);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(23, 24, 28, 0.3);
}

.btn-primary.large {
  padding: 1.5rem 3rem;
  font-size: 1.1rem;
}

.btn-secondary {
  padding: 1.25rem 2.5rem;
  background: rgba(255, 255, 255, 0.9);
  color: #17181c;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-secondary:hover {
  background: #ffffff;
  border-color: rgba(23, 24, 28, 0.25);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(23, 24, 28, 0.12);
}

.btn-secondary.large {
  padding: 1.5rem 3rem;
  font-size: 1.1rem;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 2rem;
}

.metric-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.06);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(23, 24, 28, 0.12);
  border-color: rgba(23, 24, 28, 0.2);
}

.metric-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.metric-data {
  flex: 1;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: #17181c;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 600;
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 600px;
}

.visual-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 20px;
  box-shadow: 0 12px 48px rgba(23, 24, 28, 0.12);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.visual-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 64px rgba(23, 24, 28, 0.18);
}

.main-card {
  width: 100%;
  height: 400px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 2rem;
  overflow: hidden;
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.card-content {
  position: relative;
  z-index: 1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  font-weight: 600;
  color: #17181c;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.live {
  background: #10b981;
  animation: pulse 2s ease-in-out infinite;
}

.mini-chart {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  height: 200px;
  padding: 1rem;
  background: linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
  border-radius: 12px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(180deg, #3b82f6 0%, #10b981 100%);
  border-radius: 4px 4px 0 0;
  animation: growBar 1.5s ease-out;
}

@keyframes growBar {
  from { height: 0; }
}

.side-card-1,
.side-card-2 {
  width: 200px;
  height: 140px;
  padding: 1.5rem;
}

.side-card-1 {
  top: 10%;
  right: 0;
  animation: floatSide 6s ease-in-out infinite;
}

.side-card-2 {
  bottom: 10%;
  left: 0;
  animation: floatSide 6s ease-in-out infinite 3s;
}

@keyframes floatSide {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.card-mini {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mini-icon {
  font-size: 2.5rem;
}

.mini-stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.mini-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: #17181c;
  line-height: 1;
}

.mini-label {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 600;
}

/* Sections */
.section-features,
.section-demos,
.section-profiles {
  padding: 6rem 2rem;
  position: relative;
  z-index: 10;
}

.section-features {
  background: linear-gradient(180deg, #fcfcfc 0%, #f8f9fa 100%);
}

.section-demos {
  background: #fcfcfc;
}

.section-profiles {
  background: linear-gradient(180deg, #f8f9fa 0%, #fcfcfc 100%);
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.section-tag {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  color: #fcfcfc;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.section-title {
  font-size: 3.5rem;
  font-weight: 900;
  color: #17181c;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  line-height: 1.7;
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  padding: 3rem;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 64px rgba(23, 24, 28, 0.15);
  border-color: rgba(23, 24, 28, 0.2);
}

.feature-number {
  position: absolute;
  top: 2rem;
  right: 2rem;
  font-size: 4rem;
  font-weight: 900;
  color: rgba(23, 24, 28, 0.04);
  line-height: 1;
}

.feature-icon-wrapper {
  margin-bottom: 2rem;
}

.feature-icon {
  width: 68px;
  height: 68px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #17181c;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.feature-desc {
  color: #6b7280;
  line-height: 1.7;
  margin-bottom: 2rem;
  font-size: 1rem;
}


/* Demos Grid */
.demos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.demo-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(23, 24, 28, 0.08);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.demo-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(23, 24, 28, 0.14);
}

.demo-card.featured {
  grid-column: span 2;
}

.demo-header {
  padding: 2rem;
  border-bottom: 1px solid rgba(23, 24, 28, 0.08);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  background: linear-gradient(180deg, rgba(59, 130, 246, 0.02) 0%, transparent 100%);
}

.demo-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
}

.demo-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #17181c;
  margin-bottom: 0.25rem;
}

.demo-subtitle {
  font-size: 0.9rem;
  color: #6b7280;
}

.demo-body {
  padding: 2rem;
}

.demo-controls,
.demo-config {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.students-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  min-width: 300px;
}

.input-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #17181c;
}

.students-textarea {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 12px;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 0.9rem;
  color: #17181c;
  background: #fcfcfc;
  resize: vertical;
  transition: all 0.2s;
}

.students-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.65rem 1.25rem;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 28, 0.15);
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  color: #17181c;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #17181c;
  color: #fcfcfc;
  border-color: #17181c;
  transform: translateY(-2px);
}

/* Profiles Grid */
.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.profile-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 24px;
  padding: 3rem;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.profile-card:hover,
.profile-card.active {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 24px 64px rgba(23, 24, 28, 0.18);
  border-color: transparent;
}

.profile-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  opacity: 0;
  transition: opacity 0.4s;
  filter: blur(60px);
}

.profile-card:hover .profile-glow,
.profile-card.active .profile-glow {
  opacity: 0.15;
}

.profile-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.profile-icon {
  width: 68px;
  height: 68px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fcfcfc;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.profile-card:hover .profile-icon {
  transform: scale(1.15) rotate(10deg);
}

.profile-badge {
  padding: 0.5rem 1rem;
  background: rgba(23, 24, 28, 0.06);
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #17181c;
}

.profile-name {
  font-size: 2rem;
  font-weight: 900;
  color: #17181c;
  margin-bottom: 1rem;
  letter-spacing: -0.01em;
}

.profile-desc {
  color: #6b7280;
  line-height: 1.7;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.profile-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(23, 24, 28, 0.03);
  border-radius: 16px;
  margin-bottom: 2rem;
}

.profile-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 40px;
  height: 40px;
  padding: 0.5rem;
  background: #fcfcfc;
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 10px;
  color: #17181c;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #17181c;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 600;
}

.profile-btn {
  width: 100%;
  padding: 1.25rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  color: #fcfcfc;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.profile-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

/* CTA Section */
.section-cta {
  padding: 8rem 2rem;
  background: linear-gradient(135deg, #17181c 0%, #2d2f36 100%);
  position: relative;
  z-index: 10;
  overflow: hidden;
}

.section-cta::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  animation: rotate 30s linear infinite;
}

.cta-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.cta-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 0.75rem 1.5rem;
  border-radius: 100px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.85rem;
  color: #fcfcfc;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.cta-title {
  font-size: 3.5rem;
  font-weight: 900;
  color: #fcfcfc;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.cta-desc {
  font-size: 1.25rem;
  color: rgba(252, 252, 252, 0.7);
  line-height: 1.7;
  margin-bottom: 3rem;
}

.cta-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

.cta-features {
  display: flex;
  gap: 2.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(252, 252, 252, 0.8);
  font-size: 1rem;
  font-weight: 600;
}

.cta-feature svg {
  color: #10b981;
  flex-shrink: 0;
}

/* Footer */
.footer {
  padding: 4rem 2rem 2rem;
  background: #f8f9fa;
  position: relative;
  z-index: 10;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.5fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.footer-desc {
  color: #6b7280;
  line-height: 1.7;
  font-size: 0.95rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-column h4 {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #17181c;
  margin-bottom: 1.25rem;
}

.footer-column a {
  display: block;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.95rem;
  margin-bottom: 0.85rem;
  transition: all 0.2s;
}

.footer-column a:hover {
  color: #17181c;
  transform: translateX(3px);
}

.footer-bottom {
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 2rem;
  border-top: 1px solid rgba(23, 24, 28, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-bottom p {
  color: #6b7280;
  font-size: 0.9rem;
}

.footer-social {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcfcfc;
  border: 1px solid rgba(23, 24, 28, 0.1);
  border-radius: 10px;
  color: #6b7280;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.social-link:hover {
  color: #17181c;
  border-color: rgba(23, 24, 28, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(23, 24, 28, 0.1);
}

/* Responsive */
@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .hero-visual {
    height: 400px;
  }
  
  .hero-title {
    font-size: 4rem;
  }
  
  .section-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .mobile-menu {
    display: flex;
  }
  
  .nav-links {
    display: none;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .cta-title {
    font-size: 2.5rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
  }
  
  .footer-links {
    grid-template-columns: 1fr;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .demos-grid {
    grid-template-columns: 1fr;
  }
  
  .demo-card.featured {
    grid-column: span 1;
  }
}
</style><template>
  <div class="showcase-container">
    <!-- Animated Background -->
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="mesh-grid"></div>
    </div>

    <!-- Navigation -->
    <nav :class="['nav-bar', { 'scrolled': scrolled }]">
      <div class="nav-content">
        <div class="logo-group">
          <div class="logo-badge">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" />
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" />
            </svg>
          </div>
          <span class="logo-name">S.U.M</span>
          <span class="logo-tag">Sistema Unificado de Gestão</span>
        </div>
        
        <div class="nav-links">
          <a href="#features" class="nav-link">
            <span>Funcionalidades</span>
            <div class="link-indicator"></div>
          </a>
          <a href="#demos" class="nav-link">
            <span>Demonstrações</span>
            <div class="link-indicator"></div>
          </a>
          <a href="#profiles" class="nav-link">
            <span>Perfis</span>
            <div class="link-indicator"></div>
          </a>
          <button @click="goToEntrar" class="btn-access">
            <span>Acessar Sistema</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
        </div>

        <button class="mobile-menu" @click="menuOpen = !menuOpen">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="pulse-dot"></span>
          <span>Sistema de Gestão Escolar Completo</span>
        </div>
        
        <h1 class="hero-title">
          Transforme sua
          <span class="gradient-text">Instituição</span>
        </h1>
        
        <p class="hero-desc">
          Dashboards inteligentes, mapeamento 3D de salas e análises em tempo real 
          para máxima produtividade educacional
        </p>
        
        <div class="hero-actions">
          <button class="btn-primary" @click="goToEntrar">
            <span>Começar Agora</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
          <button class="btn-secondary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            <span>Ver Demo</span>
          </button>
        </div>

        <!-- Metrics Cards -->
        <div class="metrics-grid">
          <div v-for="metric in metrics" :key="metric.label" class="metric-card">
            <div class="metric-icon" :style="{ background: metric.color }">
              <component :is="metric.icon" />
            </div>
            <div class="metric-data">
              <div class="metric-value">{{ metric.value }}</div>
              <div class="metric-label">{{ metric.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hero Visual -->
      <div class="hero-visual">
        <div class="visual-card main-card">
          <div class="card-glow"></div>
          <div class="card-content">
            <div class="card-header">
              <div class="status-indicator live"></div>
              <span>Dashboard em Tempo Real</span>
            </div>
            <div class="mini-chart" aria-label="Mini gráfico de atividade">
              <div v-for="(v, i) in miniChartBars" :key="i" class="chart-bar" :style="{ height: `${v}%` }"></div>
            </div>
          </div>
        </div>
        
        <div class="visual-card side-card-1">
          <div class="card-mini">
            <div class="mini-icon">📊</div>
            <div class="mini-stat">
              <span class="mini-value">95%</span>
              <span class="mini-label">Eficiência</span>
            </div>
          </div>
        </div>
        
        <div class="visual-card side-card-2">
          <div class="card-mini">
            <div class="mini-icon">🎯</div>
            <div class="mini-stat">
              <span class="mini-value">500+</span>
              <span class="mini-label">Alunos</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="section-features">
      <div class="section-header">
        <span class="section-tag">Funcionalidades</span>
        <h2 class="section-title">Sistema Completo de Gestão</h2>
        <p class="section-subtitle">
          Tudo que você precisa para gerir sua instituição de forma inteligente
        </p>
      </div>

      <div class="features-grid">
        <div v-for="(feature, idx) in features" :key="idx" class="feature-card">
          <div class="feature-number">{{ String(idx + 1).padStart(2, '0') }}</div>
          <div class="feature-icon-wrapper">
            <div class="feature-icon" :style="{ background: feature.color }">
              <component :is="feature.icon" />
            </div>
          </div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-desc">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Demos Section -->
    <section id="demos" class="section-demos">
      <div class="section-header">
        <span class="section-tag">Demonstrações</span>
        <h2 class="section-title">Visualize o Sistema em Ação</h2>
        <p class="section-subtitle">
          Componentes interativos prontos para uso imediato
        </p>
      </div>

      <div class="demos-grid">
        <!-- Mapeamento 2D -->
        <div class="demo-card featured">
          <div class="demo-header">
            <div class="demo-icon">🗺️</div>
            <div>
              <h3 class="demo-title">Mapeamento 2D de Salas</h3>
              <p class="demo-subtitle">Organize carteiras e defina grupos dinamicamente</p>
            </div>
          </div>
          
          <div class="demo-body">
            <div class="demo-controls">
              <MapToolbar :tool="tool"
                @set-tool="setTool"
                @rotate="actionRotate"
                @delete="actionDelete"
                @save="actionSave"
                @load="actionLoad"
                @export="actionExport"
              />
              <MapMini :seats="miniSeats" :teacher="miniTeacher" :sourceSize="{ width: 900, height: 520 }" />
            </div>

            <div class="demo-config">
              <MapConfig
                :rows="rowsArray"
                :teacherPos="teacherPos"
                :teacherLabel="teacherLabel"
                :background="mapBg"
                :alternate="altColors"
                :showNumbers="showNumbers"
                :showBorders="showBorders"
                @update:rows="updateRows"
                @update:teacher-pos="updateTeacherPos"
                @update:teacher-label="updateTeacherLabel"
                @update:background="updateBackground"
                @update:alternate="updateAltColors"
                @update:show-numbers="updateShowNumbers"
                @update:show-borders="updateShowBorders"
                @distribute="distributeFromConfig"
                @apply-rules="applyRules"
                @save-defaults="saveDefaults"
                @load-defaults="loadDefaults"
                @reset-layout="resetLayout"
              />
              
              <div class="students-panel">
                <label class="input-label">Lista de Alunos</label>
                <textarea
                  class="students-textarea"
                  v-model="studentsRaw"
                  placeholder="Digite um aluno por linha..."
                ></textarea>
                <div class="action-buttons">
                  <button class="action-btn" @click="applyDistribution('random')">Aleatória</button>
                  <button class="action-btn" @click="applyDistribution('alpha')">Alfabética</button>
                  <button class="action-btn" @click="applyDistribution('input')">Entrada</button>
                  <button class="action-btn" @click="applyDistribution('mix')">Misturar</button>
                </div>
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
              @update:teacher="handleTeacherUpdate"
              @update:seats="handleSeatsUpdate"
            />
          </div>
        </div>

        <!-- Chart Demo -->
        <div class="demo-card">
          <div class="demo-header">
            <div class="demo-icon">📈</div>
            <div>
              <h3 class="demo-title">Gráficos de Produtividade</h3>
              <p class="demo-subtitle">Visualização em tempo real</p>
            </div>
          </div>
          <div class="demo-body">
            <Suspense>
              <template #default>
                <InteractiveChart
              :title="'Produtividade Semanal'"
              :subtitle="'Evolução do desempenho'"
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
              </template>
              <template #fallback>
                <div style="height:220px;display:flex;align-items:center;justify-content:center;color:#6b7280">Carregando gráfico...</div>
              </template>
            </Suspense>
          </div>
        </div>

        <!-- Radar Demo -->
        <div class="demo-card">
          <div class="demo-header">
            <div class="demo-icon">🎯</div>
            <div>
              <h3 class="demo-title">Radar de Competências</h3>
              <p class="demo-subtitle">Análise multidimensional</p>
            </div>
          </div>
          <div class="demo-body">
            <Suspense>
              <template #default>
                <SkillRadar
              :title="'Desempenho Acadêmico'"
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
              </template>
              <template #fallback>
                <div style="height:220px;display:flex;align-items:center;justify-content:center;color:#6b7280">Carregando radar...</div>
              </template>
            </Suspense>
          </div>
        </div>

        <!-- Table Demo -->
        <div class="demo-card">
          <div class="demo-header">
            <div class="demo-icon">📋</div>
            <div>
              <h3 class="demo-title">Gestão de Turmas</h3>
              <p class="demo-subtitle">Tabela dinâmica e filtros avançados</p>
            </div>
          </div>
          <div class="demo-body">
            <Suspense>
              <template #default>
                <DynamicTable
              :title="'Turmas Ativas'"
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
              </template>
              <template #fallback>
                <div style="height:220px;display:flex;align-items:center;justify-content:center;color:#6b7280">Carregando tabela...</div>
              </template>
            </Suspense>
          </div>
        </div>
      </div>
    </section>

    <!-- Profiles Section -->
    <section id="profiles" class="section-profiles">
      <div class="section-header">
        <span class="section-tag">Perfis de Acesso</span>
        <h2 class="section-title">Dashboards Personalizados</h2>
        <p class="section-subtitle">
          Cada usuário tem acesso a ferramentas específicas para seu perfil
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
          <div class="profile-glow" :style="{ background: profile.color }"></div>
          <div class="profile-icon-wrapper">
            <div class="profile-icon" :style="{ background: profile.color }">
              <component :is="profile.icon" />
            </div>
            <div class="profile-badge">{{ profile.badge }}</div>
          </div>
          <h3 class="profile-name">{{ profile.name }}</h3>
          <p class="profile-desc">{{ profile.description }}</p>
          
          <div class="profile-stats">
            <div v-for="stat in profile.stats" :key="stat.label" class="profile-stat">
              <component :is="stat.icon" class="stat-icon" />
              <div class="stat-info">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
              </div>
            </div>
          </div>
          
          <button class="profile-btn" :style="{ background: profile.color }">
            <span>Acessar Dashboard</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="section-cta">
      <div class="cta-container">
        <div class="cta-badge">
          <span class="pulse-dot"></span>
          <span>Comece Hoje Mesmo</span>
        </div>
        
        <h2 class="cta-title">
          Pronto para revolucionar a gestão da sua escola?
        </h2>
        
        <p class="cta-desc">
          Junte-se a centenas de instituições que já transformaram 
          sua gestão com o S.U.M
        </p>
        
        <div class="cta-actions">
          <button class="btn-primary large">
            <span>Iniciar Gratuitamente</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
          <button class="btn-secondary large">
            <span>Agendar Demo</span>
          </button>
        </div>

        <div class="cta-features">
          <div class="cta-feature">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Sem cartão de crédito</span>
          </div>
          <div class="cta-feature">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Suporte 24/7</span>
          </div>
          <div class="cta-feature">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Dados seguros</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="logo-group">
            <div class="logo-badge">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="currentColor" />
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" />
              </svg>
            </div>
            <span class="logo-name">S.U.M</span>
          </div>
          <p class="footer-desc">
            Sistema Unificado de Gestão Escolar.<br/>
            Transformando a educação através da tecnologia.
          </p>
        </div>

        <div class="footer-links">
          <div class="footer-column">
            <h4>Produto</h4>
            <a href="#">Funcionalidades</a>
            <a href="#">Preços</a>
            <a href="#">Integrações</a>
            <a href="#">Atualizações</a>
          </div>
          <div class="footer-column">
            <h4>Empresa</h4>
            <a href="#">Sobre</a>
            <a href="#">Carreiras</a>
            <a href="#">Blog</a>
            <a href="#">Contato</a>
          </div>
          <div class="footer-column">
            <h4>Suporte</h4>
            <a href="#">Central de Ajuda</a>
            <a href="#">Documentação</a>
            <a href="#">Status</a>
            <a href="#">API</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 S.U.M. Todos os direitos reservados.</p>
        <div class="footer-social">
          <a href="#" class="social-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </a>
          <a href="#" class="social-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
          </a>
          <a href="#" class="social-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, defineComponent, h, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import ClassroomMap2D from '@/components/classroom/ClassroomMap2D.vue'
import MapToolbar from '@/components/classroom/MapToolbar.vue'
import MapMini from '@/components/classroom/MapMini.vue'
import MapConfig from '@/components/classroom/MapConfig.vue'
// Lazy-load shared, heavier visual components
const InteractiveChart = defineAsyncComponent(() => import('@/shared/InteractiveChart.vue'))
const SkillRadar = defineAsyncComponent(() => import('@/shared/SkillRadar.vue'))
const DynamicTable = defineAsyncComponent(() => import('@/shared/DynamicTable.vue'))

// Icons
const TrendingUpIcon = defineComponent({
  render: () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polyline', { points: '23 6 13.5 15.5 8.5 10.5 1 18' }),
    h('polyline', { points: '17 6 23 6 23 12' })
  ])
})

const CheckIcon = defineComponent({
  render: () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polyline', { points: '20 6 9 17 4 12' })
  ])
})

const ClockIcon = defineComponent({
  render: () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('circle', { cx: 12, cy: 12, r: 10 }),
    h('polyline', { points: '12 6 12 12 16 14' })
  ])
})

const UsersIcon = defineComponent({
  render: () => h('svg', { width: 20, height: 20, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: 9, cy: 7, r: 4 }),
    h('path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87' })
  ])
})

const BarChartIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('line', { x1: 12, y1: 20, x2: 12, y2: 10 }),
    h('line', { x1: 18, y1: 20, x2: 18, y2: 4 }),
    h('line', { x1: 6, y1: 20, x2: 6, y2: 16 })
  ])
})

const BookOpenIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z' }),
    h('path', { d: 'M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z' })
  ])
})

const GraduationCapIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M22 10v6M2 10l10-5 10 5-10 5z' }),
    h('path', { d: 'M6 12v5c3 3 9 3 12 0v-5' })
  ])
})

const SettingsIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('circle', { cx: 12, cy: 12, r: 3 }),
    h('path', { d: 'M12 1v6m0 6v6' })
  ])
})

const FileIcon = defineComponent({
  render: () => h('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
    h('polyline', { points: '14 2 14 8 20 8' })
  ])
})

const SmallUsersIcon = defineComponent({
  render: () => h('svg', { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
    h('circle', { cx: 9, cy: 7, r: 4 })
  ])
})

const MapIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('polygon', { points: '1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6' }),
    h('line', { x1: 8, y1: 2, x2: 8, y2: 18 }),
    h('line', { x1: 16, y1: 6, x2: 16, y2: 22 })
  ])
})

const CalendarIcon = defineComponent({
  render: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
    h('rect', { x: 3, y: 4, width: 18, height: 18, rx: 2, ry: 2 }),
    h('line', { x1: 16, y1: 2, x2: 16, y2: 6 }),
    h('line', { x1: 8, y1: 2, x2: 8, y2: 6 }),
    h('line', { x1: 3, y1: 10, x2: 21, y2: 10 })
  ])
})

// State
const scrolled = ref(false)
const menuOpen = ref(false)
const activeProfile = ref<string | null>(null)
const router = useRouter()

const goToEntrar = () => router.push('/entrar')

// Data
const metrics = [
  { value: '+45%', label: 'Produtividade', icon: TrendingUpIcon, color: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' },
  { value: '98%', label: 'Satisfação', icon: CheckIcon, color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' },
  { value: '24/7', label: 'Disponível', icon: ClockIcon, color: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)' },
  { value: '500+', label: 'Instituições', icon: UsersIcon, color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }
]

const features = [
  {
    title: 'Dashboard Inteligente',
    description: 'Análise completa em tempo real com métricas de produtividade, frequência e desempenho acadêmico',
    icon: BarChartIcon,
    color: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
  },
  {
    title: 'Mapeamento 2D/3D',
    description: 'Visualize e organize salas de aula com tecnologia interativa e drag-and-drop intuitivo',
    icon: MapIcon,
    color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
  },
  {
    title: 'Gestão de Turmas',
    description: 'Controle completo de alunos, professores, horários e recursos escolares',
    icon: BookOpenIcon,
    color: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'
  },
  {
    title: 'Relatórios Avançados',
    description: 'Gere relatórios detalhados e análises preditivas para tomada de decisões',
    icon: CalendarIcon,
    color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
  }
]

const profiles = [
  {
    id: 'aluno',
    name: 'Aluno',
    icon: BookOpenIcon,
    description: 'Acompanhe suas notas, frequência, atividades e cronograma de estudos em tempo real',
    badge: 'Estudante',
    color: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    stats: [
      { label: 'Desempenho', value: 'A+', icon: FileIcon },
      { label: 'Frequência', value: '95%', icon: CheckIcon }
    ]
  },
  {
    id: 'professor',
    name: 'Professor',
    icon: UsersIcon,
    description: 'Gerencie turmas, lance notas, crie atividades e acompanhe o desenvolvimento dos alunos',
    badge: 'Educador',
    color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    stats: [
      { label: 'Turmas', value: '6', icon: BookOpenIcon },
      { label: 'Alunos', value: '180', icon: SmallUsersIcon }
    ]
  },
  {
    id: 'coordenador',
    name: 'Coordenador',
    icon: GraduationCapIcon,
    description: 'Supervisione professores e alunos com dashboards analíticos e relatórios detalhados',
    badge: 'Coordenação',
    color: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
    stats: [
      { label: 'Professores', value: '32', icon: UsersIcon },
      { label: 'Turmas', value: '24', icon: BookOpenIcon }
    ]
  },
  {
    id: 'diretor',
    name: 'Diretor',
    icon: SettingsIcon,
    description: 'Visão completa da instituição com métricas estratégicas e controle total de gestão',
    badge: 'Administração',
    color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    stats: [
      { label: 'Unidades', value: '3', icon: GraduationCapIcon },
      { label: 'Total Alunos', value: '850+', icon: SmallUsersIcon }
    ]
  }
]

// Map state
const rows2D = ref(5)
const cols2D = ref(8)
const groupMode2D = ref<'single'|'duo'|'trio'>('single')
const snap2D = ref(true)
const mapRef = ref<InstanceType<typeof ClassroomMap2D> | null>(null)
const tool = ref<'select'|'move'>('select')
const miniSeats = ref<Array<{ x:number;y:number;w:number;h:number }>>([])
const miniTeacher = ref<{ x:number;y:number;w:number;h:number }>({ x:0,y:0,w:0,h:0 })
const rowsArray = ref<number[]>([8,8,8,8,8])
const teacherPos = ref<'left'|'center'|'right'|'hidden'>('center')
const teacherLabel = ref('Professor')
const mapBg = ref('#ffffff')
const altColors = ref(true)
const showNumbers = ref(true)
const showBorders = ref(true)
const rules = ref({})
const studentsRaw = ref('')
const students = ref<Array<{ name:string; list?:string }>>([])

// Chart data
const miniChartBars = ref<number[]>(Array.from({ length: 12 }, (_, i) => 35 + Math.round(45 * Math.abs(Math.sin(i)))))
const productivityChart = {
  labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],
  datasets: [
    { 
      label: 'Produtividade', 
      data: [65, 72, 78, 85, 90], 
      borderColor: '#10b981', 
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
}

const radarSkills = [
  { name: 'Matemática', value: 85, color: '#3b82f6' },
  { name: 'Português', value: 78, color: '#10b981' },
  { name: 'Ciências', value: 82, color: '#8b5cf6' },
  { name: 'História', value: 90, color: '#f59e0b' },
  { name: 'Geografia', value: 75, color: '#ef4444' },
  { name: 'Inglês', value: 88, color: '#06b6d4' }
]

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
  { turma: '7º C', professor: 'Prof. Santos', sala: 'Sala 05', horario: '10:00', students: 32, status: 'Ativa' },
  { turma: '6º A', professor: 'Profª. Lima', sala: 'Sala 02', horario: '11:00', students: 25, status: 'Ativa' }
]

// Methods
const actionRotate = () => mapRef.value?.rotateSelection()
const actionDelete = () => mapRef.value?.deleteSelection()
const actionSave = () => mapRef.value?.saveLayout()
const actionLoad = () => mapRef.value?.loadLayout()
const actionExport = () => mapRef.value?.exportPng()

const handleTeacherUpdate = (p: { x: number; y: number }) => {
  miniTeacher.value = { x: p.x, y: p.y, w: 42, h: 42 }
}

const handleSeatsUpdate = (seats: any[]) => {
  miniSeats.value = seats.map(s => ({ x: s.x, y: s.y, w: s.w, h: s.h }))
}

const syncRowsConfig = () => {
  rows2D.value = rowsArray.value.length
}

const parseStudents = (raw: string) => {
  const lines = (raw || '').split(/\r?\n/)
  const res: Array<{ name: string; list?: string }> = []
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

const applyDistribution = (method: 'random'|'alpha'|'input'|'mix') => {
  students.value = parseStudents(studentsRaw.value)
  mapRef.value?.distribute(method, rules.value)
}

const saveDefaults = () => {
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

const loadDefaults = () => {
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

const resetLayout = () => {
  rowsArray.value = [8,8,8,8,8]
  teacherPos.value = 'center'
  teacherLabel.value = 'Professor'
  mapBg.value = '#ffffff'
  altColors.value = true
  showNumbers.value = true
  showBorders.value = true
  syncRowsConfig()
}

const handleChartClick = (data: any) => console.log('Chart clicked:', data)
const handleSkillClick = (skill: any) => console.log('Skill clicked:', skill)
const handleTableRowClick = (row: any) => console.log('Row clicked:', row)
const handleTableSelection = (rows: any[]) => console.log('Selection:', rows)
const handleTableExport = (format: string) => console.log('Export:', format)

const handleScroll = () => {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  // Animate mini chart deterministically for better SSR/hydration
  let t = 0
  const id = window.setInterval(() => {
    t += 0.15
    miniChartBars.value = miniChartBars.value.map((_, i) => {
      const v = 50 + 35 * Math.sin(t + i * 0.35)
      return Math.max(5, Math.min(95, Math.round(v)))
    })
  }, 800)
  ;(onUnmounted as any)(() => window.clearInterval(id))
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
  
// Strongly-typed template handlers to avoid implicit any
const setTool = (t: 'select' | 'move') => {
  tool.value = t
}

const updateRows = (v: number[]) => {
  rowsArray.value = v
  syncRowsConfig()
}

const updateTeacherPos = (v: 'left'|'center'|'right'|'hidden') => {
  teacherPos.value = v
}

const updateTeacherLabel = (v: string) => {
  teacherLabel.value = v
}

const updateBackground = (v: string) => {
  mapBg.value = v
}

const updateAltColors = (v: boolean) => {
  altColors.value = v
}

const updateShowNumbers = (v: boolean) => {
  showNumbers.value = v
}

const updateShowBorders = (v: boolean) => {
  showBorders.value = v
}

const distributeFromConfig = (m: 'random'|'alpha'|'input'|'mix') => {
  mapRef.value?.distribute(m, rules.value)
}

const applyRules = (r: Record<string, unknown>) => {
  rules.value = r
}

</script>