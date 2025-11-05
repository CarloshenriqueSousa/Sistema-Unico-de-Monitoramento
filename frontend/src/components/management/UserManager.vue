<template>
  <div class="user-manager">
    <div class="manager-background"></div>
    
    <div class="manager-header">
      <div class="header-content">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M4.5 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM14.25 8.625a3.375 3.375 0 116.75 0 3.375 3.375 0 01-6.75 0zM1.5 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM17.25 19.128l-.001.144a2.25 2.25 0 01-.233.96 10.088 10.088 0 005.06-1.01.75.75 0 00.42-.643 4.875 4.875 0 00-6.957-4.611 8.586 8.586 0 011.71 5.157v.003z" />
          </svg>
        </div>
        <div>
          <h3 class="manager-title">Gerenciador de Usuários</h3>
          <p class="manager-subtitle">Gerencie perfis e permissões</p>
        </div>
      </div>
      
      <div class="header-actions">
        <div class="search-box">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="search-icon">
            <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar usuário..."
            class="search-input"
          />
        </div>
        
        <button @click="addUser" class="action-btn primary">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
          </svg>
          Adicionar Usuário
        </button>
      </div>
    </div>
    
    <div class="manager-content">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Carregando usuários...</p>
      </div>
      
      <div v-else class="users-grid">
        <div 
          v-for="user in filteredUsers" 
          :key="user.id"
          class="user-card"
        >
          <div class="card-header">
            <div class="user-avatar" :style="{ background: getAvatarGradient(user.role) }">
              {{ getInitials(user.nome) }}
            </div>
            <div class="user-badge" :class="getRoleBadgeClass(user.role)">
              {{ user.role }}
            </div>
          </div>
          
          <div class="card-content">
            <h4 class="user-name">{{ user.nome }}</h4>
            <p class="user-email">{{ user.email }}</p>
            
            <div v-if="user.role === 'Aluno' && user.skills" class="user-skills">
              <div class="skill-item">
                <span class="skill-label">Humanas</span>
                <div class="skill-bar">
                  <div class="skill-fill" :style="{ width: `${user.skills.humanas}%` }"></div>
                </div>
              </div>
              <div class="skill-item">
                <span class="skill-label">Exatas</span>
                <div class="skill-bar">
                  <div class="skill-fill" :style="{ width: `${user.skills.exatas}%` }"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="card-actions">
            <button @click="editUser(user)" class="action-icon edit">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path d="M5.433 13.917l1.262-3.155A4 4 0 017.58 9.42l6.92-6.918a2.121 2.121 0 013 3l-6.92 6.918c-.383.383-.84.685-1.343.886l-3.154 1.262a.5.5 0 01-.65-.65z" />
                <path d="M3.5 5.75c0-.69.56-1.25 1.25-1.25H10A.75.75 0 0010 3H4.75A2.75 2.75 0 002 5.75v9.5A2.75 2.75 0 004.75 18h9.5A2.75 2.75 0 0017 15.25V10a.75.75 0 00-1.5 0v5.25c0 .69-.56 1.25-1.25 1.25h-9.5c-.69 0-1.25-.56-1.25-1.25v-9.5z" />
              </svg>
            </button>
            
            <button @click="viewProfile(user)" class="action-icon view">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z" />
                <path fill-rule="evenodd" d="M.664 10.59a1.651 1.651 0 010-1.186A10.004 10.004 0 0110 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0110 17c-4.257 0-7.893-2.66-9.336-6.41zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
              </svg>
            </button>
            
            <button @click="deleteUser(user)" class="action-icon delete">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.52.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const loading = ref(false)
const searchQuery = ref('')

const users = ref([
  { id: 1, nome: 'João Silva', email: 'joao@escola.com', role: 'Aluno', skills: { humanas: 85, exatas: 78 } },
  { id: 2, nome: 'Maria Santos', email: 'maria@escola.com', role: 'Professor', skills: null },
  { id: 3, nome: 'Pedro Costa', email: 'pedro@escola.com', role: 'Aluno', skills: { humanas: 76, exatas: 92 } },
  { id: 4, nome: 'Ana Oliveira', email: 'ana@escola.com', role: 'Admin', skills: null },
  { id: 5, nome: 'Carlos Souza', email: 'carlos@escola.com', role: 'PDT', skills: null }
])

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.nome.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.role.toLowerCase().includes(query)
  )
})

const getInitials = (name) => {
  const parts = name.split(' ')
  return parts.length >= 2 
    ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    : name.substring(0, 2).toUpperCase()
}

const getAvatarGradient = (role) => {
  const gradients = {
    'Aluno': 'linear-gradient(135deg, #2d531a, #0f1e3f)',
    'Professor': 'linear-gradient(135deg, #7c3aed, #2563eb)',
    'Admin': 'linear-gradient(135deg, #f59e0b, #ea580c)',
    'PDT': 'linear-gradient(135deg, #10b981, #059669)'
  }
  return gradients[role] || 'linear-gradient(135deg, #6b7280, #4b5563)'
}

const getRoleBadgeClass = (role) => {
  const classes = {
    'Aluno': 'badge-student',
    'Professor': 'badge-teacher',
    'Admin': 'badge-admin',
    'PDT': 'badge-pdt'
  }
  return classes[role] || 'badge-default'
}

const addUser = () => {
  console.log('Adicionar usuário')
}

const editUser = (user) => {
  console.log('Editar usuário:', user.id)
}

const viewProfile = (user) => {
  console.log('Ver perfil:', user.id)
}

const deleteUser = (user) => {
  if (confirm(`Tem certeza que deseja excluir ${user.nome}?`)) {
    console.log('Deletar usuário:', user.id)
  }
}
</script>

<style scoped>
.user-manager {
  position: relative;
  background: #ffffff;
  border-radius: 1.5rem;
  overflow: hidden;
}

.manager-background {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(225, 212, 194, 0.3), transparent 60%);
  pointer-events: none;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 2px solid rgba(45, 83, 26, 0.1);
  position: relative;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 3.5rem;
  height: 3.5rem;
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(45, 83, 26, 0.3);
}

.header-icon svg {
  width: 2rem;
  height: 2rem;
  color: #e1d4c2;
}

.manager-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f1d20;
  margin: 0;
}

.manager-subtitle {
  font-size: 0.875rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0.25rem 0 0 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.125rem;
  height: 1.125rem;
  color: #0f1e3f;
  opacity: 0.5;
}

.search-input {
  width: 280px;
  padding: 0.75rem 1rem 0.75rem 3rem;
  background: rgba(225, 212, 194, 0.3);
  border: 2px solid rgba(45, 83, 26, 0.2);
  border-radius: 0.75rem;
  font-size: 0.9375rem;
  color: #1f1d20;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2d531a;
  background: rgba(225, 212, 194, 0.4);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #2d531a, #0f1e3f);
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 83, 26, 0.4);
}

.btn-icon {
  width: 1.125rem;
  height: 1.125rem;
}

.manager-content {
  padding: 2rem;
  position: relative;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1rem;
  color: #6b7280;
}

.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(45, 83, 26, 0.2);
  border-top-color: #2d531a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: #ffffff;
  border: 2px solid rgba(45, 83, 26, 0.1);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s ease;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(31, 29, 32, 0.1);
  border-color: rgba(45, 83, 26, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(225, 212, 194, 0.3), rgba(225, 212, 194, 0.1));
}

.user-avatar {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  color: #e1d4c2;
  box-shadow: 0 4px 12px rgba(45, 83, 26, 0.3);
}

.user-badge {
  padding: 0.375rem 0.875rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-student {
  background: rgba(45, 83, 26, 0.15);
  color: #2d531a;
}

.badge-teacher {
  background: rgba(124, 58, 237, 0.15);
  color: #7c3aed;
}

.badge-admin {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.badge-pdt {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.card-content {
  padding: 1.5rem;
}

.user-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1f1d20;
  margin: 0 0 0.5rem 0;
}

.user-email {
  font-size: 0.875rem;
  color: #0f1e3f;
  opacity: 0.7;
  margin: 0 0 1rem 0;
}

.user-skills {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(45, 83, 26, 0.1);
}

.skill-item {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.skill-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f1d20;
  opacity: 0.6;
  text-transform: uppercase;
}

.skill-bar {
  height: 0.5rem;
  background: rgba(225, 212, 194, 0.3);
  border-radius: 0.25rem;
  overflow: hidden;
}

.skill-fill {
  height: 100%;
  background: linear-gradient(90deg, #2d531a, #0f1e3f);
  border-radius: 0.25rem;
  transition: width 0.8s ease;
}

.card-actions {
  display: flex;
  justify-content: space-around;
  padding: 1rem 1.5rem;
  border-top: 2px solid rgba(45, 83, 26, 0.1);
}

.action-icon {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-icon svg {
  width: 1.125rem;
  height: 1.125rem;
}

.action-icon.edit {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.action-icon.edit:hover {
  background: rgba(245, 158, 11, 0.2);
  transform: scale(1.1);
}

.action-icon.view {
  background: rgba(45, 83, 26, 0.1);
  color: #2d531a;
}

.action-icon.view:hover {
  background: rgba(45, 83, 26, 0.2);
  transform: scale(1.1);
}

.action-icon.delete {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.action-icon.delete:hover {
  background: rgba(220, 38, 38, 0.2);
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .search-input {
    width: 200px;
  }
}
</style>