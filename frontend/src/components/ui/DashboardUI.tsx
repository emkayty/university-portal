/**
 * Dashboard UI Components
 * ====================
 * Skeleton loaders, spinners, empty states, toasts, search
 */
'use client';

import React from 'react';

// SKELETON LOADER
export function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`animate-pulse bg-gray-200 rounded ${className}`} />;
}

export function CardSkeleton() {
  return (
    <div className="card p-4">
      <Skeleton className="h-4 w-24 mb-2" />
      <Skeleton className="h-8 w-16" />
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {[...Array(4)].map((_, i) => <CardSkeleton key={i} />)}
    </div>
  );
}

// LOADING SPINNER
export function Loader({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' };
  return <div className={`${sizes[size]} border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin`} />;
}

export function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-center">
        <Loader size="lg" />
        <p className="mt-4 text-gray-500">Loading...</p>
      </div>
    </div>
  );
}

// EMPTY STATE
interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
}

export function EmptyState({ title, description, icon }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      {icon && <div className="text-gray-300 mb-4">{icon}</div>}
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      {description && <p className="mt-1 text-gray-500 max-w-sm">{description}</p>}
    </div>
  );
}

// ERROR STATE
interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({ title = 'Something went wrong', message = 'Please try again.', onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mb-4">
        <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-gray-500">{message}</p>
      {onRetry && <button onClick={onRetry} className="mt-4 btn btn-secondary">Try Again</button>}
    </div>
  );
}

// TOAST NOTIFICATIONS
type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

let toasts: Toast[] = [];
let listeners: ((t: Toast[]) => void)[] = [];

export function toast(type: ToastType, message: string) {
  const id = Math.random().toString(36).substr(2, 9);
  toasts = [...toasts, { id, type, message }];
  listeners.forEach(fn => fn(toasts));
  setTimeout(() => {
    toasts = toasts.filter(t => t.id !== id);
    listeners.forEach(fn => fn(toasts));
  }, 5000);
}

export function Toaster() {
  const [current, setCurrent] = React.useState<Toast[]>([]);
  
  React.useEffect(() => {
    listeners.push(setCurrent);
    return () => { listeners = listeners.filter(fn => fn !== setCurrent); };
  }, []);
  
  if (current.length === 0) return null;
  
  const colors = { success: 'bg-green-500', error: 'bg-red-500', warning: 'bg-amber-500', info: 'bg-blue-500' };
  
  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {current.map(t => (
        <div key={t.id} className={`${colors[t.type]} text-white px-4 py-3 rounded-lg shadow-lg animate-slide-in`}>
          {t.message}
        </div>
      ))}
    </div>
  );
}

// SEARCH INPUT
interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function SearchInput({ value, onChange, placeholder = 'Search...' }: SearchInputProps) {
  return (
    <div className="relative">
      <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-10 pr-10 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      {value && (
        <button onClick={() => onChange('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
}

// THEME TOGGLE
export function useTheme() {
  const [dark, setDark] = React.useState(false);
  
  React.useEffect(() => {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      setDark(true);
      document.documentElement.classList.add('dark');
    }
  }, []);
  
  const toggle = () => {
    const newDark = !dark;
    setDark(newDark);
    document.documentElement.classList.toggle('dark', newDark);
    localStorage.setItem('theme', newDark ? 'dark' : 'light');
  };
  
  return { dark, toggle };
}

// STATS CARD
interface StatsCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  color?: string;
}

export function StatsCard({ label, value, icon, color = 'blue' }: StatsCardProps) {
  const colors: Record<string, string> = {
    blue: 'text-blue-600 bg-blue-50',
    green: 'text-green-600 bg-green-50',
    red: 'text-red-600 bg-red-50',
  };
  
  return (
    <div className="card p-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-gray-500 text-sm">{label}</p>
          <h3 className="font-bold text-2xl mt-1">{value}</h3>
        </div>
        {icon && <div className={`p-2 rounded-lg ${colors[color]}`}>{icon}</div>}
      </div>
    </div>
  );
}

// QUICK ACTION
interface QuickActionProps {
  icon: React.ReactNode;
  label: string;
  sublabel?: string;
  href?: string;
}

export function QuickAction({ icon, label, sublabel, href }: QuickActionProps) {
  const content = (
    <div className="card p-4 flex items-center gap-3 hover:shadow-md transition-all cursor-pointer group">
      <div className="group-hover:scale-110 transition-transform">{icon}</div>
      <div>
        <p className="font-medium group-hover:text-blue-600">{label}</p>
        {sublabel && <p className="text-xs text-gray-500">{sublabel}</p>}
      </div>
    </div>
  );
  
  return href ? <a href={href}>{content}</a> : content;
}