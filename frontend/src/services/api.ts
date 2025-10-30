import axios from 'axios';
import { useAuthStore } from '../store/authStore';

// Pega a URL base da API da variável de ambiente VITE_API_BASE_URL
// Se não estiver definida, usa localhost:8000 como padrão (para dev fora do Docker)
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: baseURL, // Usa a variável
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token automaticamente (CORRIGIDO)
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;

  // 1. Verifique se a rota é de login PRIMEIRO.
  if (config.url === '/auth/login') {
    // Se for login e os dados forem FormData...
    if (config.data instanceof FormData) {
      // ...defina o Content-Type correto exigido pelo OAuth2.
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    }
    // Retorne a config de login (sem token de autorização)
    return config;
  }

  // 2. Para TODAS AS OUTRAS rotas, adicione o token se ele existir.
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Evita o loop de logout se o erro for na própria página de login
      if (window.location.pathname !== '/login') {
        useAuthStore.getState().logout();
        window.location.href = '/login'; // Redireciona para a página de login
      }
    }
    return Promise.reject(error);
  }
);

export default api;