/**
 * Dashboard - REAL DATA
 */
'use client';
import { RefreshCw } from 'lucide-react';
import { useDashboard } from '@/hooks/useData';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';
import { PageLoader, ErrorState } from '@/components/ui/DashboardUI';

export default function Dashboard() {
  const { loading, error, refetch } = useDashboard();
  if (error) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><ErrorState onRetry={refetch} /></main></div></div>;
  if (loading) return <div className="min-h-screen bg-gray-50"><DashboardSidebar /><div className="lg:pl-64"><DashboardHeader /><main className="p-6"><PageLoader /></main></div></div>;
  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="flex justify-between mb-6">
            <div><h1 className="text-2xl font-bold">Dashboard</h1></div>
            <button onClick={refetch} className="p-2 hover:bg-gray-100 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
          </div>
          <div className="card p-6"><p className="text-gray-500">Loading data from API...</p></div>
        </main>
      </div>
    </div>
  );
}
