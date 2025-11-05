// services/Authservices.ts (Preenchido: Métodos para login, register, logout, password reset; typed)
import api from './api';

interface LoginCredentials {
  identificador: string;
  senha: string;
}

interface RegisterData {
  identificador: string;
  email: string;
  senha: string;
  tipo: 'aluno' | 'professor' | 'escola' | 'admin';
}

interface ResetPasswordData {
  email: string;
}

interface NewPasswordData {
  token: string;
  senha: string;
}

export const login = async (credentials: LoginCredentials) => {
  const response = await api.post('/core/login/', credentials);
  localStorage.setItem('token', response.data.access);
  localStorage.setItem('refreshToken', response.data.refresh);
  localStorage.setItem('userRole', response.data.tipo);
  return response.data;
};

export const register = async (data: RegisterData) => {
  return api.post('/core/register/', data);  // Assuma endpoint no backend
};

export const logout = () => {
  localStorage.clear();
  window.location.href = '/login';
};

export const forgotPassword = async (data: ResetPasswordData) => {
  return api.post('/core/forgot-password/', data);
};

export const resetPassword = async (data: NewPasswordData) => {
  return api.post('/core/reset-password/', data);
};