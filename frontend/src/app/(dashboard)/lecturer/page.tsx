/**
 * Lecturer Dashboard Page
 * ===================
 * Main lecturer landing with classes, materials, and grading
 */
'use client';

import { useState } from 'react';
import { BookOpen, Users, Calendar, Award, Upload, Clock, CheckCircle, AlertCircle, FileText, QrCode } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_COURSES = [
  { id: '1', code: 'CS301', title: 'Data Structures', students: 45, level: 300, sessions: 15 },
  { id: '2', code: 'CS201', title: 'Introduction to Programming', students: 62, level: 200, sessions: 14 },
  { id: '3', code: 'CS401', title: 'Algorithms', students: 28, level: 400, sessions: 15 },
];

const DEMO_PENDING = [
  { id: '1', course: 'CS301', task: 'Grade submissions', count: 15, due: '2024-11-15' },
  { id: '2', course: 'CS201', task: 'Create quiz', count: 0, due: '2024-11-20' },
  { id: '3', course: 'CS401', task: 'Upload materials', count: 3, due: '2024-11-12' },
];

export default function LecturerDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [courses] = useState(DEMO_COURSES);
  const [pending] = useState(DEMO_PENDING);

  const primaryColor = settings?.primary_color || '#1e40af';

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      
      <div className="lg:pl-64">
        <DashboardHeader />
        
        <main className="p-4 lg:p-6">
          {/* Welcome */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome, {user?.first_name || 'Lecturer'}!
            </h1>
            <p className="text-gray-500">
              Manage your courses and students
            </p>
          </div>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">My Courses</p>
                  <h3 className="font-bold text-2xl">{courses.length}</h3>
                </div>
                <BookOpen className="w-8 h-8 text-blue-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Total Students</p>
                  <h3 className="font-bold text-2xl">{courses.reduce((s, c) => s + c.students, 0)}</h3>
                </div>
                <Users className="w-8 h-8 text-green-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Pending Tasks</p>
                  <h3 className="font-bold text-2xl">{pending.length}</h3>
                </div>
                <AlertCircle className="w-8 h-8 text-amber-600" />
              </div>
            </div>
            
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-500 text-sm">This Week</p>
                  <h3 className="font-bold text-2xl">12h</h3>
                </div>
                <Clock className="w-8 h-8 text-purple-600" />
              </div>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/materials" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <Upload className="w-8 h-8 text-blue-600" />
              <div>
                <p className="font-medium">Upload Material</p>
                <p className="text-xs text-gray-500">Course notes</p>
              </div>
            </a>
            
            <a href="/dashboard/attendance" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <QrCode className="w-8 h-8 text-green-600" />
              <div>
                <p className="font-medium">Take Attendance</p>
                <p className="text-xs text-gray-500">QR scan</p>
              </div>
            </a>
            
            <a href="/dashboard/grades" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <Award className="w-8 h-8 text-amber-600" />
              <div>
                <p className="font-medium">Grade Book</p>
                <p className="text-xs text-gray-500">Submit scores</p>
              </div>
            </a>
            
            <a href="/dashboard/assignments" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <FileText className="w-8 h-8 text-purple-600" />
              <div>
                <p className="font-medium">Assignments</p>
                <p className="text-xs text-gray-500">Create & manage</p>
              </div>
            </a>
          </div>
          
          {/* My Courses */}
          <div className="card">
            <div className="p-4 border-b border-gray-100 flex items-center justify-between">
              <h2 className="font-semibold">My Courses</h2>
              <a href="/dashboard/my-courses" className="text-sm text-blue-600 hover:underline">View All</a>
            </div>
            <div className="divide-y divide-gray-100">
              {courses.map(course => (
                <div key={course.id} className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
                      <BookOpen className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium">{course.code} - {course.title}</p>
                      <p className="text-sm text-gray-500">Level {course.level} • {course.students} students</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs">
                      {course.sessions} sessions
                    </span>
                    <button className="btn btn-secondary text-sm">
                      Manage
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