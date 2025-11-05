// services/api.ts (Melhorado: Adicionado error handling global, refresh token logic, typed responses)
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Configuração da API
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000'),
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
};

// Instância principal da API
const api: AxiosInstance = axios.create(API_CONFIG);

// Interceptor de requisição - adiciona token de autenticação
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de resposta - tratamento de erros e refresh token
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const originalRequest = error.config;

    // Se o erro for 401 (não autorizado) e não foi uma tentativa de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_CONFIG.baseURL}/api/auth/token/refresh/`, {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          // Reexecuta a requisição original com o novo token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Se o refresh falhar, limpa os tokens e redireciona para login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        
        // Redireciona para login apenas se não estiver já na página de login
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }

    // Tratamento de outros erros
    if (error.response?.status >= 500) {
      console.error('Erro do servidor:', error.response.data);
    } else if (error.response?.status >= 400) {
      console.error('Erro do cliente:', error.response.data);
    }

    return Promise.reject(error);
  }
);

// Funções auxiliares para facilitar o uso da API
export const apiService = {
  // GET request
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return api.get(url, config);
  },

  // POST request
  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return api.post(url, data, config);
  },

  // PUT request
  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return api.put(url, data, config);
  },

  // PATCH request
  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return api.patch(url, data, config);
  },

  // DELETE request
  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return api.delete(url, config);
  },

  // Upload de arquivo
  upload: <T = any>(url: string, file: File, onProgress?: (progress: number) => void): Promise<AxiosResponse<T>> => {
    const formData = new FormData();
    formData.append('file', file);

    return api.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });
  },
};

// Função para testar a conexão com o backend
export const testConnection = async (): Promise<boolean> => {
  try {
    const response = await api.get('/api/health/');
    return response.status === 200;
  } catch (error) {
    console.error('Erro ao testar conexão com o backend:', error);
    return false;
  }
};

export default api;