<!-- filepath: src/components/notes/NoteEditor.vue -->
<template>
  <div>
    <textarea v-model="note.value" rows="6" placeholder="Digite sua anotação..."></textarea>
    <button @click="saveNote">Salvar</button>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
const note = ref('')
const emit = defineEmits(['save'])
function saveNote() {
  if (note.value.trim()) emit('save', note.value)
  note.value = ''
}
</script>