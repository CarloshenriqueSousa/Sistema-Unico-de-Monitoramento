<!-- filepath: src/components/notes/NoteItem.vue -->
<template>
  <div class="note-item">
    <p>{{ note }}</p>
    <button @click="$emit('remove')">Remover</button>
  </div>
</template>
<script setup lang="ts">
defineProps<{ note: string }>()
defineEmits(['remove'])
</script>