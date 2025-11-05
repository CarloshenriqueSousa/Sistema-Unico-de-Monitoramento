import type { UserRole } from '@/types/user';

export interface User {
  id: string;
  identificador: string;
  nome: string;
  email: string;
  tipo: UserRole;
  metadata?: Record<string, any>;
}

export interface AuthState {
  token: string | null;
  refreshToken: string | null;
  user: User | null;
  role: UserRole;
}

export interface RootState {
  auth: AuthState;
}