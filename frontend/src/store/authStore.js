import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi } from '../services/api';
import toast from 'react-hot-toast';

const TIMEOUT_MINUTES = 4;
const TIMEOUT_MS = TIMEOUT_MINUTES * 60 * 1000;

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      lastActivity: Date.now(),
      
      login: async (email, password) => {
        try {
          const response = await authApi.login({ username: email, password });
          const { access_token, user } = response.data;
          
          set({
            user,
            token: access_token,
            lastActivity: Date.now(),
          });
          
          localStorage.setItem('token', access_token);
          localStorage.setItem('user', JSON.stringify(user));
          localStorage.setItem('lastActivity', Date.now().toString());
          
          return { success: true };
        } catch (error) {
          return { 
            success: false, 
            error: error.response?.data?.detail || 'Erro ao fazer login' 
          };
        }
      },
      
      logout: () => {
        set({ user: null, token: null, lastActivity: null });
        localStorage.clear();
        window.location.href = '/login';
      },
      
      updateActivity: () => {
        const now = Date.now();
        set({ lastActivity: now });
        localStorage.setItem('lastActivity', now.toString());
      },
      
      checkTimeout: () => {
        const { lastActivity, token } = get();
        if (!token || !lastActivity) return false;
        
        const now = Date.now();
        const elapsed = now - lastActivity;
        
        if (elapsed > TIMEOUT_MS) {
          toast.error('Sessão expirada por inatividade');
          get().logout();
          return true;
        }
        return false;
      },
      
      initialize: () => {
        const token = localStorage.getItem('token');
        const userStr = localStorage.getItem('user');
        const lastActivity = localStorage.getItem('lastActivity');
        
        if (token && userStr && lastActivity) {
          const user = JSON.parse(userStr);
          const activity = parseInt(lastActivity);
          
          // Verificar se não expirou
          if (Date.now() - activity > TIMEOUT_MS) {
            get().logout();
          } else {
            set({ user, token, lastActivity: activity });
          }
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        lastActivity: state.lastActivity 
      }),
    }
  )
);

// Verificar timeout a cada 30 segundos
setInterval(() => {
  const state = useAuthStore.getState();
  if (state.token) {
    state.checkTimeout();
  }
}, 30000);

// Atualizar atividade em eventos do usuário
if (typeof window !== 'undefined') {
  ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
    document.addEventListener(event, () => {
      const state = useAuthStore.getState();
      if (state.token) {
        state.updateActivity();
      }
    }, { passive: true });
  });
}

export default useAuthStore;