<template>
  <div class="dashboard-professor">
    <h1>Dashboard do Professor</h1>
    <p>Gerencie suas turmas e atividades</p>
    <div class="cards">
      <div class="card">Minhas Turmas</div>
      <div class="card">Atividades Pendentes</div>
      <div class="card">Analytics</div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.dashboard-professor { padding: 2rem; }
.dashboard-professor h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #1a1a1a; }
.dashboard-professor p { color: #666; margin-bottom: 2rem; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
.card { padding: 1.5rem; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
</style>
