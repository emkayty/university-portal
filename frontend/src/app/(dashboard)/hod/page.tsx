/**
 * HOD Dashboard Page
 * ==================
 * Head of Department - department overview, approvals
 */
'use client';

import { useState } from 'react';
import { Building, Users, CheckCircle, Clock, AlertTriangle, FileText, BookOpen, Calendar, TrendingUp, UserCheck } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_STAFF = [
  { id: '1', name: 'Dr. Ahmed Musa', title: 'Senior Lecturer', courses: 2, status: 'active' },
  { id: '2', name: 'Mrs. Fatima Bello', title: 'Lecturer I', courses: 3, status: 'active' },
  { id: '3', name: 'Mr. Chukwudi Okafor', title: 'Assistant Lecturer', courses: 1, status: 'on_leave' },
];

const DEMO_APPROVALS = [
  { id: '1', course: 'CS301', lecturer: 'Dr. Ahmed Musa', submitted: '2024-11-10', status: 'pending', count: 45 },
  { id: '2', course: 'CS201', lecturer: 'Mrs. Fatima Bello', submitted: '2024-11-09', status: 'pending', count: 62 },
];

export default function HODDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [staff] = useState(DEMO_STAFF);
  const [approvals] = useState(DEMO_APPROVALS);

  const pendingCount = approvals.filter(a => a.status === 'pending').length;

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      
      <div className="lg:pl-64">
        <DashboardHeader />
        
        <main className="p-4 lg:p-6">
          {/* Welcome */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">
              Department Dashboard
            </h1>
            <p className="text-gray-500">
              Department of Computer Science
            </p>
          </div>
          
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Total Staff</p>
                  <h3 className="font-bold text-2xl">{staff.length}</h3>
                </div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Pending Approvals</p>
                  <h3 className="font-bold text-2xl text-amber-600">{pendingCount}</h3>
                </div>
                <Clock className="w-8 h-8 text-amber-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Active Courses</p>
                  <h3 className="font-bold text-2xl">8</h3>
                </div>
                <BookOpen className="w-8 h-8 text-green-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Avg Attendance</p>
                  <h3 className="font-bold text-2xl">87%</h3>
                </div>
                <TrendingUp className="w-8 h-8 text-purple-600" />
              </div>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/approvals" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <CheckCircle className="w-8 h-8 text-amber-600" />
              <div>
                <p className="font-medium">Result Approvals</p>
                <p className="text-xs text-gray-500">{pendingCount} pending</p>
              </div>
            </a>
            
            <a href="/dashboard/staff" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <Users className="w-8 h-8 text-blue-600" />
              <div>
                <p className="font-medium">Staff</p>
                <p className="text-xs text-gray-500">Manage team</p>
              </div>
            </a>
            
            <a href="/dashboard/courses" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <BookOpen className="w-8 h-8 text-green-600" />
              <div>
                <p className="font-medium">Allocation</p>
                <p className="text-xs text-gray-500">Course分配</p>
              </div>
            </a>
            
            <a href="/dashboard/reports" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <FileText className="w-8 h-8 text-purple-600" />
              <div>
                <p className="font-medium">Reports</p>
                <p className="text-xs text-gray-500">Analytics</p>
              </div>
            </a>
          </div>
          
          {/* Pending Approvals */}
          <div className="card">
            <div className="p-4 border-b border-gray-100 flex items-center justify-between">
              <h2 className="font-semibold">Pending Result Approvals</h2>
              <a href="/dashboard/approvals" className="text-sm text-blue-600 hover:underline">View All</a>
            </div>
            <div className="divide-y divide-gray-100">
              {approvals.map(approval => (
                <div key={approval.id} className="p-4 flex items-center justify-between">
                  <div>
                    <p className="font-medium">{approval.course}</p>
                    <p className="text-sm text-gray-500">
                      {approval.lecturer} • {approval.count} students • {approval.submitted}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`
                      px-3 py-1 rounded-full text-xs
                      ${approval.status === 'pending' ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'}
                    `}>
                      {approval.status}
                    </span>
                    <button className="btn btn-primary text-sm">
                      Review
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}