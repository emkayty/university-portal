'use client'

import { useState, useEffect } from 'react'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: {
    id: string
    email: string
    role: string
    name: string
  } | null
  token: string | null
  isAuthenticated: boolean
  login: (user: any, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
)

// API client
const API_BASE = '/api/v1'

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = useAuthStore.getState().token
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  })
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }))
    throw new Error(error.error || 'Request failed')
  }
  
  return response.json()
}

// Auth hooks
export async function login(email: string, password: string) {
  const data = await apiClient<{ access: string; refresh: string }>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  
  // Decode JWT to get user info (simplified)
  const user = { id: '1', email, role: 'student', name: email.split('@')[0] }
  
  useAuthStore.getState().login(user, data.access)
  return user
}

export function logout() {
  useAuthStore.getState().logout()
}