import axios from 'axios';

const catalogoApi = axios.create({
  baseURL: import.meta.env.VITE_CATALOGO_API_URL || 'http://localhost:5001',
  timeout: 10000,
});

export interface CatalogoModulo {
  fabricante: string;
  nome_modelo: string;
  potencia_w: number;
}

export interface CatalogoInversor {
  fabricante: string;
  nome_modelo: string;
  potencia_w: number;
}

export const catalogoService = {
  // Buscar módulos
  async getModulos(params?: {
    fabricante?: string;
    potencia_min?: number;
    potencia_max?: number;
    limit?: number;
    search?: string;
  }) {
    const response = await catalogoApi.get<{ total: number; data: CatalogoModulo[] }>('/modulos', { params });
    return response.data;
  },

  // Buscar inversores
  async getInversores(params?: {
    fabricante?: string;
    potencia_min?: number;
    potencia_max?: number;
    limit?: number;
    search?: string;
  }) {
    const response = await catalogoApi.get<{ total: number; data: CatalogoInversor[] }>('/inversores', { params });
    return response.data;
  },

  // Buscar fabricantes
  async getFabricantes(tipo: 'modulos' | 'inversores') {
    const response = await catalogoApi.get<{ total: number; data: string[] }>('/fabricantes', { params: { tipo } });
    return response.data;
  },

  // Busca global
  async search(query: string, limit?: number) {
    const response = await catalogoApi.get('/search', { params: { q: query, limit } });
    return response.data;
  },
};

export default catalogoService;