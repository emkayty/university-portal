/**
 * Dashboard Layout Components
 * =====================
 * Sidebar, Header, Navigation for all dashboards
 */
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  GraduationCap, 
  Users, 
  BookOpen, 
  DollarSign, 
  Settings, 
  Bell, 
  Menu, 
  X,
  LogOut,
  Home,
  Calendar,
  ClipboardList,
  Award,
  Building,
  HomeIcon,
  CreditCard,
  BarChart3
} from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';

interface SidebarLink {
  href: string;
  label: string;
  icon: React.ElementType;
  roles?: string[];
}

const SIDEBAR_LINKS: SidebarLink[] = [
  // Student links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['student'] },
  { href: '/dashboard/courses', label: 'My Courses', icon: BookOpen, roles: ['student'] },
  { href: '/dashboard/assignments', label: 'Assignments', icon: ClipboardList, roles: ['student'] },
  { href: '/dashboard/results', label: 'Results', icon: Award, roles: ['student'] },
  { href: '/dashboard/attendance', label: 'Attendance', icon: Calendar, roles: ['student'] },
  { href: '/dashboard/timetable', label: 'Timetable', icon: Calendar, roles: ['student'] },
  { href: '/dashboard/fees', label: 'Fees', icon: DollarSign, roles: ['student'] },
  { href: '/dashboard/hostel', label: 'Hostel', icon: HomeIcon, roles: ['student'] },
  { href: '/dashboard/transcript', label: 'Transcript', icon: GraduationCap, roles: ['student'] },
  
  // Lecturer links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['lecturer'] },
  { href: '/dashboard/my-courses', label: 'My Courses', icon: BookOpen, roles: ['lecturer'] },
  { href: '/dashboard/attendance', label: 'Attendance', icon: Calendar, roles: ['lecturer'] },
  { href: '/dashboard/grades', label: 'Grade Book', icon: Award, roles: ['lecturer'] },
  
  // HOD links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['hod'] },
  { href: '/dashboard/department', label: 'Department', icon: Building, roles: ['hod'] },
  { href: '/dashboard/approvals', label: 'Approvals', icon: ClipboardList, roles: ['hod'] },
  { href: '/dashboard/staff', label: 'Staff', icon: Users, roles: ['hod'] },
  
  // Dean links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['dean'] },
  { href: '/dashboard/faculty', label: 'Faculty', icon: Building, roles: ['dean'] },
  { href: '/dashboard/approvals', label: 'Approvals', icon: ClipboardList, roles: ['dean'] },
  { href: '/dashboard/reports', label: 'Reports', icon: BarChart3, roles: ['dean'] },
  
  // Registrar links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['registrar'] },
  { href: '/dashboard/admissions', label: 'Admissions', icon: Users, roles: ['registrar'] },
  { href: '/dashboard/students', label: 'Students', icon: GraduationCap, roles: ['registrar'] },
  { href: '/dashboard/calendar', label: 'Calendar', icon: Calendar, roles: ['registrar'] },
  { href: '/dashboard/graduation', label: 'Graduation', icon: Award, roles: ['registrar'] },
  
  // Bursar links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['bursar'] },
  { href: '/dashboard/fees', label: 'Fees', icon: DollarSign, roles: ['bursar'] },
  { href: '/dashboard/payments', label: 'Payments', icon: CreditCard, roles: ['bursar'] },
  { href: '/dashboard/scholarships', label: 'Scholarships', icon: Award, roles: ['bursar'] },
  
  // Admin links
  { href: '/dashboard', label: 'Dashboard', icon: Home, roles: ['institution_admin'] },
  { href: '/dashboard/settings', label: 'Settings', icon: Settings, roles: ['institution_admin'] },
  { href: '/dashboard/users', label: 'Users', icon: Users, roles: ['institution_admin'] },
  { href: '/dashboard/academic', label: 'Academic', icon: Building, roles: ['institution_admin'] },
];

export function DashboardSidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();
  const { sidebarOpen, toggleSidebar, settings } = useInstitutionStore();
  
  const userRole = user?.role || 'student';
  
  const filteredLinks = SIDEBAR_LINKS.filter(
    link => !link.roles || link.roles.includes(userRole)
  );

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={toggleSidebar}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 z-50 h-full w-64 bg-slate-900 text-white
        transform transition-transform duration-200 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
      `}>
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-bold text-lg">{settings?.institution_name || 'UniCore'}</h1>
              <p className="text-xs text-slate-400">Portal</p>
            </div>
          </div>
          <button onClick={toggleSidebar} className="lg:hidden">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        {/* Navigation */}
        <nav className="p-4 space-y-1">
          {filteredLinks.map(link => {
            const isActive = pathname === link.href || pathname.startsWith(link.href + '/');
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`
                  flex items-center gap-3 px-4 py-3 rounded-lg text-sm
                  transition-colors duration-150
                  ${isActive 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }
                `}
              >
                <link.icon className="w-5 h-5" />
                {link.label}
              </Link>
            );
          })}
        </nav>
        
        {/* User section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-700">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center">
              <span className="text-sm font-medium">
                {user?.first_name?.[0] || 'U'}{user?.last_name?.[0] || ''}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-xs text-slate-400 capitalize">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 w-full px-4 py-2 text-sm text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </aside>
    </>
  );
}

export function DashboardHeader() {
  const { user } = useAuthStore();
  const { theme, toggleTheme, setSidebarOpen } = useInstitutionStore();

  return (
    <header className="sticky top-0 z-30 h-16 bg-white border-b border-gray-200 flex items-center px-4 lg:px-6">
      <button 
        onClick={setSidebarOpen} 
        className="mr-4 p-2 rounded-lg hover:bg-gray-100 lg:hidden"
      >
        <Menu className="w-5 h-5" />
      </button>
      
      <div className="flex-1" />
      
      <div className="flex items-center gap-2">
        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-gray-100"
        >
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
        
        {/* Notifications */}
        <button className="p-2 rounded-lg hover:bg-gray-100 relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>
        
        {/* Profile */}
        <div className="flex items-center gap-2 ml-2 pl-4 border-l">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm">
            {user?.first_name?.[0] || 'U'}
          </div>
        </div>
      </div>
    </header>
  );
}