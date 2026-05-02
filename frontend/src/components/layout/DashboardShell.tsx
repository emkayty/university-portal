'use client'

import { useState } from 'react'
import Link from 'next/link'
import { 
  Home, BookOpen, Users, GraduationCap, 
  DollarSign, Settings, Bell, Menu, X,
  LogOut, Calendar, FileText
} from 'lucide-react'

// Navigation items based on role
const navigation = {
  student: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'My Courses', href: '/dashboard/courses', icon: BookOpen },
    { name: 'Assignments', href: '/dashboard/assignments', icon: FileText },
    { name: 'Results', href: '/dashboard/results', icon: GraduationCap },
    { name: 'Finance', href: '/dashboard/finance', icon: DollarSign },
  ],
  lecturer: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'My Courses', href: '/dashboard/courses', icon: BookOpen },
    { name: 'Grade Book', href: '/dashboard/grades', icon: FileText },
    { name: 'Attendance', href: '/dashboard/attendance', icon: Users },
  ],
  hod: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Departments', href: '/dashboard/departments', icon: Users },
    { name: 'Results', href: '/dashboard/results', icon: FileText },
    { name: 'Reports', href: '/dashboard/reports', icon: GraduationCap },
  ],
  dean: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Faculties', href: '/dashboard/faculties', icon: Home },
    { name: 'Results', href: '/dashboard/results', icon: FileText },
  ],
  registrar: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Admissions', href: '/dashboard/admissions', icon: Users },
    { name: 'Students', href: '/dashboard/students', icon: GraduationCap },
    { name: 'Academic Calendar', href: '/dashboard/calendar', icon: Calendar },
  ],
  bursar: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Fees', href: '/dashboard/fees', icon: DollarSign },
    { name: 'Payments', href: '/dashboard/payments', icon: DollarSign },
    { name: 'Reports', href: '/dashboard/reports', icon: FileText },
  ],
  institution_admin: [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Settings', href: '/dashboard/settings', icon: Settings },
    { name: 'Users', href: '/dashboard/users', icon: Users },
    { name: 'Audit Logs', href: '/dashboard/audit', icon: FileText },
  ]
}

interface DashboardShellProps {
  children: React.ReactNode
  role: string
  userName?: string
}

export function DashboardShell({ children, role, userName }: DashboardShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const navItems = navigation[role as keyof typeof navigation] || navigation.student
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white border-r transform
        transition-transform duration-200 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="h-full flex flex-col">
          {/* Logo */}
          <div className="h-16 flex items-center justify-between px-4 border-b">
            <span className="text-xl font-bold text-[var(--primary)]">UniCore</span>
            <button 
              className="lg:hidden"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-3 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100"
              >
                <item.icon className="h-5 w-5" />
                {item.name}
              </Link>
            ))}
          </nav>
          
          {/* User section */}
          <div className="p-4 border-t">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                <span className="text-sm font-medium">
                  {userName?.charAt(0).toUpperCase() || 'U'}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{userName || 'User'}</p>
                <p className="text-xs text-gray-500 capitalize">{role}</p>
              </div>
              <button className="text-gray-400">
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </aside>
      
      {/* Main content */}
      <div className="lg:pl-64">
        {/* Topbar */}
        <header className="h-16 bg-white border-b flex items-center justify-between px-4 sticky top-0 z-30">
          <button 
            className="lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <div className="flex-1 lg:flex-none" />
          
          <div className="flex items-center gap-4">
            <button className="relative text-gray-500 hover:text-gray-700">
              <Bell className="h-5 w-5" />
              <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full" />
            </button>
          </div>
        </header>
        
        {/* Page content */}
        <main className="p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}