/**
 * Dean Dashboard Page
 * ==================
 * Faculty overview, accreditation, reports
 */
'use client';

import { useState } from 'react';
import { Building, Users, BookOpen, TrendingUp, FileText, CheckCircle, Award, BarChart3 } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_DEPARTMENTS = [
  { id: '1', name: 'Computer Science', students: 450, staff: 12, courses: 15 },
  { id: '2', name: 'Information Systems', students: 320, staff: 8, courses: 12 },
  { id: '3', name: 'Software Engineering', students: 280, staff: 6, courses: 10 },
];

const DEMO_APPROVALS = [
  { id: '1', faculty: 'Computer Science', level: 'Faculty Board', status: 'pending', count: 3 },
  { id: '2', faculty: 'Information Systems', level: 'Faculty Board', status: 'pending', count: 2 },
];

export default function DeanDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [departments] = useState(DEMO_DEPARTMENTS);
  const [approvals] = useState(DEMO_APPROVALS);

  const totalStudents = departments.reduce((s, d) => s + d.students, 0);
  const totalStaff = departments.reduce((s, d) => s + d.staff, 0);

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Faculty Dashboard</h1>
            <p className="text-gray-500">Faculty of Technology</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Total Students</p><h3 className="font-bold text-2xl">{totalStudents}</h3></div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Total Staff</p><h3 className="font-bold text-2xl">{totalStaff}</h3></div>
                <Building className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Departments</p><h3 className="font-bold text-2xl">{departments.length}</h3></div>
                <BookOpen className="w-8 h-8 text-purple-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Accreditation</p><h3 className="font-bold text-2xl text-green-600">82%</h3></div>
                <Award className="w-8 h-8 text-green-600" />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/approvals" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <CheckCircle className="w-8 h-8 text-amber-600" /><div><p className="font-medium">Result Approvals</p><p className="text-xs text-gray-500">Faculty Board</p></div>
            </a>
            <a href="/dashboard/faculty" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Building className="w-8 h-8 text-blue-600" /><div><p className="font-medium">Departments</p><p className="text-xs text-gray-500">Manage depts</p></div>
            </a>
            <a href="/dashboard/reports" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <BarChart3 className="w-8 h-8 text-purple-600" /><div><p className="font-medium">Analytics</p><p className="text-xs text-gray-500">Reports</p></div>
            </a>
            <a href="/dashboard/accreditation" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Award className="w-8 h-8 text-green-600" /><div><p className="font-medium">Accreditation</p><p className="text-xs text-gray-500">NUC compliance</p></div>
            </a>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Departments</h2></div>
              <div className="divide-y divide-gray-100">
                {departments.map(dept => (
                  <div key={dept.id} className="p-4 flex items-center justify-between">
                    <div><p className="font-medium">{dept.name}</p><p className="text-sm text-gray-500">{dept.students} students • {dept.staff} staff</p></div>
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">{dept.courses} courses</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Pending Approvals</h2></div>
              <div className="divide-y divide-gray-100">
                {approvals.map(app => (
                  <div key={app.id} className="p-4 flex items-center justify-between">
                    <div><p className="font-medium">{app.faculty}</p><p className="text-sm text-gray-500">{app.level} • {app.count} items</p></div>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs">{app.status}</span>
                      <button className="btn btn-primary text-sm">Review</button>
                    </div>
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