/**
 * UniCore Auth Store (Zustand)
 * ==========================
 * Manages authentication state across the app
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '../lib/api';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'student' | 'lecturer' | 'hod' | 'dean' | 'registrar' | 'bursar' | 'institution_admin';
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          await api.login(email, password);
          const user = await api.getMe();
          set({ 
            user: user as User, 
            isAuthenticated: true, 
            isLoading: false 
          });
        } catch (err) {
          set({ 
            error: err instanceof Error ? err.message : 'Login failed', 
            isLoading: false 
          });
          throw err;
        }
      },

      logout: async () => {
        try {
          await api.logout();
        } catch {
          // Ignore logout errors
        }
        set({ user: null, isAuthenticated: false, error: null });
      },

      checkAuth: async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return;
        }
        
        set({ isLoading: true });
        try {
          const user = await api.getMe();
          set({ user: user as User, isAuthenticated: true, isLoading: false });
        } catch {
          set({ user: null, isAuthenticated: false, isLoading: false });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'unicore-auth',
      partialize: (state) => ({ 
        user: state.user, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);

// Role helpers
export const hasRole = (user: User | null, roles: string[]): boolean => {
  if (!user) return false;
  return roles.includes(user.role);
};

export const isAdmin = (user: User | null): boolean => 
  hasRole(user, ['institution_admin', 'registrar']);

export const isStaff = (user: User | null): boolean =>
  hasRole(user, ['lecturer', 'hod', 'dean', 'registrar', 'bursar']);

export const isStudent = (user: User | null): boolean =>
  user?.role === 'student';