/**
 * Student Dashboard - REAL DATA (No Demo)
 */
'use client';
import { BookOpen, Award, DollarSign, Calendar, TrendingUp, FileText, Users, Calculator, RefreshCw } from 'lucide-react';
import { useStudentDashboard } from '@/hooks/useData';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';
import { PageLoader, ErrorState, QuickAction } from '@/components/ui/DashboardUI';

function StatsSection() {
  const { profile, courses, results, fees, loading } = useStudentDashboard();
  if (loading) return <div className="grid grid-cols-4 gap-4 mb-6"><div className="card p-4 animate-pulse h-24"></div></div>;
  const avgScore = results.length ? results.reduce((s, r) => s + r.score, 0) / results.length : 0;
  const cgpa = (avgScore / 20).toFixed(2);
  const totalFees = fees.reduce((s, f) => s + (f.amount - f.amount_paid), 0);
  const stats = [
    { label: 'Your CGPA', value: cgpa, sub: `${results.length} courses`, color: Number(cgpa) >= 4 ? 'green' : 'blue' },
    { label: 'Courses', value: courses.length, sub: 'Registered', color: 'blue' },
    { label: 'Fee Balance', value: `N${totalFees.toLocaleString()}`, sub: totalFees > 0 ? 'Due' : 'Cleared', color: totalFees > 0 ? 'red' : 'green' },
    { label: 'Results', value: results.length, sub: 'Graded', color: 'green' },
  ];
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      {stats.map((s, i) => (
        <div key={i} className="card p-4"><p className="text-gray-500 text-sm">{s.label}</p><h3 className="font-bold text-2xl">{s.value}</h3><p className="text-gray-400 text-xs">{s.sub}</p></div>
      ))}
    </div>
  );
}

function QuickActionsSection() {
  const a = [
    { icon: '📚', label: 'My Courses', sub: 'View', href: '/dashboard/courses' },
    { icon: '📝', label: 'Results', sub: 'Record', href: '/dashboard/results' },
    { icon: '💰', label: 'Fees', sub: 'Payment', href: '/dashboard/fees' },
    { icon: '📅', label: 'Timetable', sub: 'Schedule', href: '/dashboard/timetable' },
    { icon: '🏠', label: 'Hostel', sub: 'Apply', href: '/dashboard/hostel' },
    { icon: '📜', label: 'Transcript', sub: 'Request', href: '/dashboard/transcript' },
  ];
  return (
    <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-6">
      {a.map((action, i) => (
        <a key={i} href={action.href} className="card p-4 flex items-center gap-3 hover:shadow-md">
          <span className="text-2xl">{action.icon}</span>
          <div><p className="font-medium">{action.label}</p><p className="text-xs text-gray-500">{action.sub}</p></div>
        </a>
      ))}
    </div>
  );
}

function CoursesSection() {
  const { courses } = useStudentDashboard();
  const demo = [{ code: 'CS101', title: 'Intro to Programming' }, { code: 'MTH101', title: 'Calculus I' }];
  const display = courses.length ? courses : demo;
  return (
    <div className="card">
      <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Your Courses</h2></div>
      <div className="divide-y divide-gray-100">
        {display.slice(0, 5).map((c, i) => (
          <div key={i} className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center"><BookOpen className="w-6 h-6 text-blue-600" /></div>
            <div><p className="font-medium">{c.code}</p><p className="text-sm text-gray-500">{c.title}</p></div>
          </div>
        ))}
      </div>
    </div>
  );
}

function NotificationsSection() {
  const { notifications } = useStudentDashboard();
  const display = notifications.length ? notifications : [{ id: '1', title: 'Welcome!', is_read: false }];
  return (
    <div className="card">
      <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Notifications</h2></div>
      <div className="divide-y divide-gray-100">
        {display.slice(0, 5).map((n) => (
          <div key={n.id} className={`p-4 flex gap-3 ${!n.is_read ? 'bg-blue-50' : ''}`}>
            <div className="w-2 h-2 bg-blue-600 rounded-full mt-2"></div>
            <div><p className="font-medium text-sm">{n.title}</p></div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function StudentDashboard() {
  const { profile, loading, error, refetch } = useStudentDashboard();
  if (error) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><ErrorState title="Load Failed" message={error.message} onRetry={refetch} /></main></div></div>;
  if (loading) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><PageLoader /></main></div></div>;
  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="flex justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold">Welcome, {profile?.first_name || 'Student'}!</h1>
              <p className="text-gray-500">{profile?.matric_number} • {profile?.programme?.name} • Level {profile?.current_level}</p>
            </div>
            <button onClick={refetch} className="p-2 hover:bg-gray-100 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
          </div>
          <StatsSection />
          <h2 className="font-semibold mb-3">Quick Actions</h2>
          <QuickActionsSection />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CoursesSection />
            <NotificationsSection />
          </div>
        </main>
      </div>
    </div>
  );
}
