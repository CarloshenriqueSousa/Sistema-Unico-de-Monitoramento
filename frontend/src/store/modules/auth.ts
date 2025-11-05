import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api';

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('token'));
  const role = ref<string>(user.value?.role ?? '');
  const isAuthenticated = ref(!!token.value);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const login = async ({ email, password }: { email: string; password: string }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.post('/api/token/', { email, password });
      token.value = response.data.access;
      localStorage.setItem('token', token.value!);
      isAuthenticated.value = true;

      const userResponse = await api.get<User>('/api/user/me/');
      user.value = userResponse.data;
      role.value = user.value ? user.value.role : '';
      localStorage.setItem('user', JSON.stringify(user.value));
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Credenciais inválidas';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    role.value = '';
    isAuthenticated.value = false;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const checkAuth = () => {
    const tokenVal = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (tokenVal && userData) {
      try {
        user.value = JSON.parse(userData);
        token.value = tokenVal;
        role.value = user.value ? user.value.role : '';
        isAuthenticated.value = true;
      } catch {
        logout();
      }
    }
  };

  checkAuth();

  return {
    user,
    token,
    role,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    checkAuth
  };
});