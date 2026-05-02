/**
 * Student Dashboard Page
 * ==================
 * Main student landing with widgets
 */
'use client';

import { useEffect, useState } from 'react';
import { BookOpen, Calendar, Award, DollarSign, HomeIcon, Bell, Clock, MapPin } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';
import { api } from '@/lib/api';

// Demo data
const DEMO_CLASSES = [
  { id: '1', course: 'CS101', title: 'Introduction to Programming', time: '09:00', venue: 'Lab 1', status: 'upcoming' },
  { id: '2', course: 'MTH101', title: 'Calculus I', time: '11:00', venue: 'Room 201', status: 'upcoming' },
  { id: '3', course: 'PHY101', title: 'General Physics', time: '14:00', venue: 'Hall A', status: 'upcoming' },
];

const DEMO_ASSIGNMENTS = [
  { id: '1', course: 'CS101', title: 'Python Loops', due: '2024-11-15', status: 'pending' },
  { id: '2', course: 'MTH101', title: 'Integration Problems', due: '2024-11-18', status: 'pending' },
];

const DEMO_FEES = {
  total: 150000,
  paid: 100000,
  balance: 50000,
  status: 'partial',
};

export default function StudentDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [nextClass, setNextClass] = useState(DEMO_CLASSES[0]);
  const [cgpa, setCgpa] = useState(3.75);
  const [fees, setFees] = useState(DEMO_FEES);

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      
      <div className="lg:pl-64">
        <DashboardHeader />
        
        <main className="p-4 lg:p-6">
          {/* Welcome */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome back, {user?.first_name || 'Student'}!
            </h1>
            <p className="text-gray-500">
              Here's what's happening today
            </p>
          </div>
          
          {/* Widgets Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {/* Next Class Card */}
            <div className="card p-4 bg-gradient-to-br from-blue-600 to-blue-700 text-white">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-blue-100 text-sm">Next Class</p>
                  <h3 className="font-bold text-lg mt-1">{nextClass.course}</h3>
                  <p className="text-blue-100 text-sm">{nextClass.title}</p>
                </div>
                <BookOpen className="w-6 h-6 opacity-50" />
              </div>
              <div className="mt-4 flex items-center gap-2 text-sm">
                <Clock className="w-4 h-4" />
                {nextClass.time}
                <MapPin className="w-4 h-4 ml-2" />
                {nextClass.venue}
              </div>
            </div>
            
            {/* CGPA Card */}
            <div className="card p-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Current CGPA</p>
                  <h3 className="font-bold text-3xl mt-1" style={{ color: settings?.primary_color }}>
                    {cgpa.toFixed(2)}
                  </h3>
                </div>
                <Award className="w-6 h-6 text-amber-500" />
              </div>
              <p className="text-sm text-green-600 mt-2">Above average</p>
            </div>
            
            {/* Fee Balance Card */}
            <div className="card p-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Fee Balance</p>
                  <h3 className="font-bold text-2xl mt-1">₦{fees.balance.toLocaleString()}</h3>
                </div>
                <DollarSign className="w-6 h-6 text-red-500" />
              </div>
              {fees.balance > 0 && (
                <button className="btn btn-primary w-full mt-3 text-sm">
                  Pay Now
                </button>
              )}
            </div>
            
            {/* Attendance Card */}
            <div className="card p-4">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-gray-500 text-sm">Attendance</p>
                  <h3 className="font-bold text-2xl mt-1">85%</h3>
                </div>
                <Calendar className="w-6 h-6 text-green-500" />
              </div>
              <div className="mt-2 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ width: '85%' }} />
              </div>
            </div>
          </div>
          
          {/* Quick Links */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/courses" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <BookOpen className="w-8 h-8 text-blue-600" />
              <div>
                <p className="font-medium">My Courses</p>
                <p className="text-xs text-gray-500">5 registered</p>
              </div>
            </a>
            
            <a href="/dashboard/assignments" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <Calendar className="w-8 h-8 text-amber-600" />
              <div>
                <p className="font-medium">Assignments</p>
                <p className="text-xs text-gray-500">{DEMO_ASSIGNMENTS.length} pending</p>
              </div>
            </a>
            
            <a href="/dashboard/results" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <Award className="w-8 h-8 text-green-600" />
              <div>
                <p className="font-medium">Results</p>
                <p className="text-xs text-gray-500">View grades</p>
              </div>
            </a>
            
            <a href="/dashboard/fees" className="card p-4 flex items-center gap-3 hover:shadow-md transition-shadow">
              <DollarSign className="w-8 h-8 text-red-600" />
              <div>
                <p className="font-medium">Fees</p>
                <p className="text-xs text-gray-500">Make payment</p>
              </div>
            </a>
          </div>
          
          {/* Today's Schedule */}
          <div className="card">
            <div className="p-4 border-b border-gray-100">
              <h2 className="font-semibold">Today's Schedule</h2>
            </div>
            <div className="divide-y divide-gray-100">
              {DEMO_CLASSES.map(cls => (
                <div key={cls.id} className="p-4 flex items-center gap-4">
                  <div className="w-16 text-center">
                    <p className="text-lg font-bold">{cls.time}</p>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium">{cls.course} - {cls.title}</p>
                    <p className="text-sm text-gray-500">{cls.venue}</p>
                  </div>
                  <span className={`
                    px-3 py-1 rounded-full text-xs
                    ${cls.status === 'upcoming' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}
                  `}>
                    {cls.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}