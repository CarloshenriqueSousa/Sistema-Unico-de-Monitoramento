<template>
  <div class="user-registration-view">
    <GlassCard>
      <h2 class="text-2xl font-bold mb-4">Cadastro de Usuários</h2>
      <form @submit.prevent="registerUser" class="space-y-4">
        <input v-model="user.name" class="bg-gray-800 rounded-lg px-3 py-2 w-full" placeholder="Nome" />
        <input v-model="user.email" class="bg-gray-800 rounded-lg px-3 py-2 w-full" placeholder="Email" />
        <select v-model="user.role" class="bg-gray-800 rounded-lg px-3 py-2 w-full">
          <option value="Aluno">Aluno</option>
          <option value="Professor">Professor</option>
          <option value="Gestor">Gestor</option>
        </select>
        <button class="bg-cyan-600 hover:bg-cyan-500 px-4 py-2 rounded-lg w-full">Cadastrar</button>
      </form>
    </GlassCard>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import GlassCard from '@shared/GlassCard.vue';

export default defineComponent({
  name: 'UserRegistrationView',
  components: { GlassCard },
  setup() {
    const user = ref({ name: '', email: '', role: 'Aluno' });
    function registerUser() {
      // lógica de cadastro
      user.value = { name: '', email: '', role: 'Aluno' };
    }
    return { user, registerUser };
  }
});
</script>