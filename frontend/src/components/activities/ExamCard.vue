<!-- filepath: src/components/activities/ExamCard.vue -->
<template>
  <div class="exam-card">
    <h3>{{ exam?.title }}</h3>
    <p>Disciplina: {{ exam?.subject }}</p>
    <p>Dificuldade: {{ exam?.difficulty }}</p>
    <router-link :to="`/exams/${exam?.id}`">Ver detalhes</router-link>
  </div>
</template>
<script setup lang="ts">
defineProps<{ exam?: { id: number, title: string, subject: string, difficulty: string } }>()
</script>