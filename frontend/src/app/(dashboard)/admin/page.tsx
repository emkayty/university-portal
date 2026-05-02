/**
 * Institution Admin Dashboard
 * ===================
 * System settings, users, backup
 */
'use client';

import { useState } from 'react';
import { Settings, Users, Database, Server, Shield, Bell, FileText, Palette, Building, Activity, HardDrive, RefreshCw } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_STATS = {
  users: 1250,
  students: 850,
  staff: 42,
  active_sessions: 1,
};

export default function AdminDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [stats] = useState(DEMO_STATS);

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">System Administration</h1>
            <p className="text-gray-500">{settings?.institution_name || 'University Portal'}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Total Users</p><h3 className="font-bold text-2xl">{stats.users}</h3></div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Students</p><h3 className="font-bold text-2xl">{stats.students}</h3></div>
                <Activity className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Staff</p><h3 className="font-bold text-2xl">{stats.staff}</h3></div>
                <Server className="w-8 h-8 text-purple-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">System Status</p><h3 className="font-bold text-2xl text-green-600">Healthy</h3></div>
                <Shield className="w-8 h-8 text-green-600" />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/settings" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Palette className="w-8 h-8 text-blue-600" /><div><p className="font-medium">Branding</p><p className="text-xs text-gray-500">Logo, colors</p></div>
            </a>
            <a href="/dashboard/users" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Users className="w-8 h-8 text-green-600" /><div><p className="font-medium">Users</p><p className="text-xs text-gray-500">Manage accounts</p></div>
            </a>
            <a href="/dashboard/academic" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Building className="w-8 h-8 text-purple-600" /><div><p className="font-medium">Academic</p><p className="text-xs text-gray-500">Structure</p></div>
            </a>
            <a href="/dashboard/backup" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <HardDrive className="w-8 h-8 text-amber-600" /><div><p className="font-medium">Backup</p><p className="text-xs text-gray-500">Data backup</p></div>
            </a>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/audit" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <FileText className="w-8 h-8 text-blue-600" /><div><p className="font-medium">Audit Logs</p><p className="text-xs text-gray-500">Activity log</p></div>
            </a>
            <a href="/dashboard/notifications" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Bell className="w-8 h-8 text-green-600" /><div><p className="font-medium">Notifications</p><p className="text-xs text-gray-500">Alerts</p></div>
            </a>
            <a href="/dashboard/database" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Database className="w-8 h-8 text-purple-600" /><div><p className="font-medium">Database</p><p className="text-xs text-gray-500">Migrations</p></div>
            </a>
            <a href="/dashboard/security" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Shield className="w-8 h-8 text-amber-600" /><div><p className="font-medium">Security</p><p className="text-xs text-gray-500">Settings</p></div>
            </a>
          </div>
          
          <div className="card">
            <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Quick System Actions</h2></div>
            <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              <button className="btn btn-secondary w-full">Run Migrations</button>
              <button className="btn btn-secondary w-full">Collect Static</button>
              <button className="btn btn-secondary w-full">Clear Cache</button>
              <button className="btn btn-primary w-full">Create Backup</button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}