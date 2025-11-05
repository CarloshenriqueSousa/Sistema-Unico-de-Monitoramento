// types/user.ts
export interface User {
  id: number
  email: string
  name: string
  role: 'admin' | 'teacher' | 'student'
  avatar?: string
  phone?: string
  createdAt?: Date
  updatedAt?: Date
  isActive?: boolean
  preferences?: UserPreferences
}

export interface UserPreferences {
  theme?: 'light' | 'dark' | 'auto'
  language?: string
  notifications?: boolean
  emailNotifications?: boolean
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  name: string
  role?: 'teacher' | 'student'
}

export interface TokenResponse {
  access: string
  refresh: string
}