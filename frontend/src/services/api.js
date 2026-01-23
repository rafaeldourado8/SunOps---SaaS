// SunOPS/frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (credentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  getMe: () => api.get('/auth/me'),
};

export const clientesApi = {
  getAll: (params) => api.get('/clientes/', { params }),
  getById: (id) => api.get(`/clientes/${id}`),
  create: (data) => api.post('/clientes/', data),
  update: (id, data) => api.put(`/clientes/${id}`, data),
  delete: (id) => api.delete(`/clientes/${id}`),
  promover: (id) => api.post(`/clientes/${id}/promover`),
};

export const propostasApi = {
  getAll: () => api.get('/propostas/'),
  getById: (id) => api.get(`/propostas/${id}`),
  create: (data) => api.post('/propostas/', data),
  update: (id, data) => api.put(`/propostas/${id}`, data),
  delete: (id) => api.delete(`/propostas/${id}`),
  addItem: (id, item) => api.post(`/propostas/${id}/itens`, item),
  solicitarDesconto: (id, percentual) => 
    api.post(`/propostas/${id}/desconto`, { percentual }),
  generatePDF: (id) => api.get(`/propostas/${id}/pdf`, { responseType: 'blob' }),
};

export const premissasApi = {
  getAll: () => api.get('/premissas/'),
  getById: (id) => api.get(`/premissas/${id}`),
  create: (data) => api.post('/premissas/', data),
  update: (id, data) => api.put(`/premissas/${id}`, data),
  delete: (id) => api.delete(`/premissas/${id}`),
  // CORREÇÃO: Adicionado método GET para configurações
  getConfig: () => api.get('/premissas/configuracao'),
  updateConfig: (config) => api.put('/premissas/configuracao', config),
};

export const templatesApi = {
  getAll: () => api.get('/templates/'),
  upload: (file, tipo, nome, vendedorId) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tipo', tipo);
    formData.append('nome', nome);
    formData.append('vendedor_id', vendedorId);
    return api.post('/templates/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  delete: (id) => api.delete(`/templates/${id}`),
};

export default api;