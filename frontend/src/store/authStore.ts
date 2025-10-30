import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number; // ID é número no backend
  name: string;
  email: string;
  role: 'gestor' | 'vendedor' | 'suporte';
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  setToken: (token: string | null) => void; // <-- AÇÃO ADICIONADA
  login: (token: string, user: User) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      
      // AÇÃO ADICIONADA: Permite salvar apenas o token
      setToken: (token: string | null) => {
        set({ token, isAuthenticated: !!token });
      },

      login: (token: string, user: User) => {
        set({ token, user, isAuthenticated: true });
      },
      logout: () => {
        set({ token: null, user: null, isAuthenticated: false });
      },
      setUser: (user: User) => {
        // Garante que 'isAuthenticated' permaneça true se o token já estiver lá
        set((state) => ({ user, isAuthenticated: !!state.token }));
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);