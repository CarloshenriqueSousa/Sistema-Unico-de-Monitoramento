<template>
  <div class="toolbar-root">
    <div class="group">
      <button class="btn" :class="{ active: tool === 'select' }" @click="$emit('set-tool','select')">Selecionar</button>
      <button class="btn" :class="{ active: tool === 'move' }" @click="$emit('set-tool','move')">Mover</button>
    </div>
    <div class="group">
      <button class="btn" @click="$emit('rotate')">Rotacionar 90°</button>
      <button class="btn danger" @click="$emit('delete')">Apagar</button>
    </div>
    <div class="group">
      <button class="btn" @click="$emit('save')">Salvar</button>
      <button class="btn" @click="$emit('load')">Carregar</button>
      <button class="btn" @click="$emit('export')">Exportar PNG</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ tool: 'select'|'move' }>()
</script>

<style scoped>
.toolbar-root {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.group {
  display: inline-flex;
  gap: 0.5rem;
  padding: 0.35rem;
  border-radius: 12px;
  border: 1px solid rgba(23,24,30,0.08);
  background: #fcfcfc;
}
.btn {
  padding: 0.45rem 0.8rem;
  font-size: 0.85rem;
  border-radius: 10px;
  background: #fcfcfc;
  border: 1.5px solid rgba(23, 24, 30, 0.12);
  color: #17181e;
  cursor: pointer;
  transition: all 0.2s;
}
.btn:hover { border-color: rgba(23,24,30,0.25); transform: translateY(-1px); }
.btn.active { background:#17181e; color:#fcfcfc; border-color:#17181e; }
.btn.danger { border-color:#ef4444; color:#ef4444; }
.btn.danger:hover { background:#ef4444; color:#fff; }
</style>
