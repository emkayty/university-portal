/**
 * Registrar Dashboard Page
 * ====================
 * Admissions, records, graduation
 */
'use client';

import { useState } from 'react';
import { Users, UserCheck, Calendar, GraduationCap, FileText, Award, Clock, CheckCircle } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_ADMISSIONS = [
  { id: '1', session: '2024/2025', applied: 1250, admitted: 850, enrolled: 720, status: 'ongoing' },
  { id: '2', session: '2023/2024', applied: 1100, admitted: 780, enrolled: 695, status: 'completed' },
];

const DEMO_PENDING = [
  { id: '1', type: 'Admission', item: 'JAMB Verification', count: 15, due: '2024-11-12' },
  { id: '2', type: 'Clearance', item: 'Graduation Clearance', count: 45, due: '2024-11-15' },
  { id: '3', type: 'Transcript', item: 'Transcript Requests', count: 12, due: '2024-11-14' },
];

export default function RegistrarDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [admissions] = useState(DEMO_ADMISSIONS);
  const [pending] = useState(DEMO_PENDING);
  const currentSession = admissions[0];

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Registrar Dashboard</h1>
            <p className="text-gray-500">Academic Records & Admissions</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Applied</p><h3 className="font-bold text-2xl">{currentSession.applied}</h3></div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Admitted</p><h3 className="font-bold text-2xl text-green-600">{currentSession.admitted}</h3></div>
                <UserCheck className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Enrolled</p><h3 className="font-bold text-2xl">{currentSession.enrolled}</h3></div>
                <CheckCircle className="w-8 h-8 text-purple-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Graduands</p><h3 className="font-bold text-2xl">695</h3></div>
                <GraduationCap className="w-8 h-8 text-amber-600" />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/admissions" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Users className="w-8 h-8 text-blue-600" /><div><p className="font-medium">Admissions</p><p className="text-xs text-gray-500">Manage applicants</p></div>
            </a>
            <a href="/dashboard/students" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <UserCheck className="w-8 h-8 text-green-600" /><div><p className="font-medium">Students</p><p className="text-xs text-gray-500">Records</p></div>
            </a>
            <a href="/dashboard/graduation" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <GraduationCap className="w-8 h-8 text-amber-600" /><div><p className="font-medium">Graduation</p><p className="text-xs text-gray-500">Clearance</p></div>
            </a>
            <a href="/dashboard/calendar" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Calendar className="w-8 h-8 text-purple-600" /><div><p className="font-medium">Calendar</p><p className="text-xs text-gray-500">Sessions</p></div>
            </a>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Admission Funnel ({currentSession.session})</h2></div>
              <div className="p-4 space-y-3">
                <div className="flex items-center justify-between"><span>Applied</span><span className="font-medium">{currentSession.applied}</span></div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden"><div className="h-full bg-blue-500" style={{width: '100%'}} /></div>
                <div className="flex items-center justify-between"><span>Admitted</span><span className="font-medium">{currentSession.admitted}</span></div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden"><div className="h-full bg-green-500" style={{width: '68%'}} /></div>
                <div className="flex items-center justify-between"><span>Enrolled</span><span className="font-medium">{currentSession.enrolled}</span></div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden"><div className="h-full bg-purple-500" style={{width: '58%'}} /></div>
              </div>
            </div>
            
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Pending Tasks</h2></div>
              <div className="divide-y divide-gray-100">
                {pending.map(task => (
                  <div key={task.id} className="p-4 flex items-center justify-between">
                    <div><p className="font-medium">{task.type}: {task.item}</p><p className="text-sm text-gray-500">{task.count} items • {task.due}</p></div>
                    <button className="btn btn-primary text-sm">Process</button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}