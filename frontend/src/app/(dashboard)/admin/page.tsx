/**
 * Admin Dashboard - REAL DATA
 */
'use client';
import { Users, Activity, Server, Shield, Settings, Database, FileText, Building, HardDrive, RefreshCw } from 'lucide-react';
import { useAdminDashboard } from '@/hooks/useData';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';
import { PageLoader, ErrorState, QuickAction } from '@/components/ui/DashboardUI';

function StatsSection() {
  const { analytics, loading } = useAdminDashboard();
  if (loading || !analytics) return <div className="grid grid-cols-4 gap-4 mb-6"><div className="card p-4 animate-pulse h-24"></div></div>;
  const stats = [
    { label: 'Total Students', value: analytics.total_students, icon: '👨‍🎓', color: 'blue' },
    { label: 'Total Staff', value: analytics.total_staff, icon: '👨‍🏫', color: 'green' },
    { label: 'Active Courses', value: analytics.active_courses, icon: '📚', color: 'purple' },
    { label: 'Avg GPA', value: analytics.average_gpa.toFixed(2), icon: '📊', color: 'amber' },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      {stats.map((s, i) => (
        <div key={i} className="card p-4"><p className="text-gray-500 text-sm">{s.label}</p><h3 className="font-bold text-2xl">{s.value}</h3></div>
      ))}
    </div>
  );
}

function QuickActionsSection() {
  const actions = [
    { icon: '⚙️', label: 'Settings', sub: 'Branding', href: '/dashboard/settings' },
    { icon: '👥', label: 'Users', sub: 'Manage', href: '/dashboard/users' },
    { icon: '🏛️', label: 'Academic', sub: 'Structure', href: '/dashboard/academic' },
    { icon: '💾', label: 'Backup', sub: 'Data', href: '/dashboard/backup' },
  ];
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {actions.map((a, i) => (
        <a key={i} href={a.href} className="card p-4 flex items-center gap-3 hover:shadow-md">
          <span className="text-2xl">{a.icon}</span><div><p className="font-medium">{a.label}</p><p className="text-xs text-gray-500">{a.sub}</p></div>
        </a>
      ))}
    </div>
  );
}

function UsersSection() {
  const { students, staff, loading } = useAdminDashboard();
  return (
    <div className="card">
      <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Users</h2></div>
      <div className="divide-y divide-gray-100">
        <div className="p-4"><p className="font-medium">Students</p><p className="text-gray-500">{students.length || 0} total</p></div>
        <div className="p-4"><p className="font-medium">Staff</p><p className="text-gray-500">{staff.length || 0} total</p></div>
      </div>
    </div>
  );
}

export default function AdminDashboard() {
  const { loading, error, refetch } = useAdminDashboard();
  if (error) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><ErrorState title="Load Failed" message={error.message} onRetry={refetch} /></main></div></div>;
  if (loading) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><PageLoader /></main></div></div>;
  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="flex justify-between mb-6">
            <div><h1 className="text-2xl font-bold">System Administration</h1><p className="text-gray-500">Manage the portal</p></div>
            <button onClick={refetch} className="p-2 hover:bg-gray-100 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
          </div>
          <StatsSection />
          <h2 className="font-semibold mb-3">Quick Actions</h2>
          <QuickActionsSection />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6"><UsersSection /></div>
        </main>
      </div>
    </div>
  );
}
