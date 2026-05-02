/**
 * Bursar Dashboard Page
 * ==================
 * Fees, payments, scholarships
 */
'use client';

import { useState } from 'react';
import { DollarSign, CreditCard, FileText, Award, TrendingUp, Clock, CheckCircle, AlertTriangle } from 'lucide-react';
import { useAuthStore, useInstitutionStore } from '@/store';
import { DashboardSidebar, DashboardHeader } from '@/components/layout/Dashboard';

const DEMO_FINANCE = {
  revenue: 45000000,
  outstanding: 8500000,
  collected: 36500000,
  expenses: 28000000,
};

const DEMO_RECENT = [
  { id: '1', student: 'John Doe', amount: 75000, type: 'School Fees', date: '2024-11-10', status: 'completed' },
  { id: '2', student: 'Mary Ahmed', amount: 150000, type: 'Hostel', date: '2024-11-09', status: 'completed' },
  { id: '3', student: 'Peter Obi', amount: 75000, type: 'School Fees', date: '2024-11-09', status: 'pending' },
];

export default function BursarDashboard() {
  const { user } = useAuthStore();
  const { settings } = useInstitutionStore();
  const [finance] = useState(DEMO_FINANCE);
  const [recent] = useState(DEMO_RECENT);

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardSidebar />
      <div className="lg:pl-64">
        <DashboardHeader />
        <main className="p-4 lg:p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Finance Dashboard</h1>
            <p className="text-gray-500">Bursary & Accounts</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Total Revenue</p><h3 className="font-bold text-2xl">₦{((finance.revenue)/1000000).toFixed(1)}M</h3></div>
                <DollarSign className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Collected</p><h3 className="font-bold text-2xl text-green-600">₦{((finance.collected)/1000000).toFixed(1)}M</h3></div>
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Outstanding</p><h3 className="font-bold text-2xl text-red-600">₦{((finance.outstanding)/1000000).toFixed(1)}M</h3></div>
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
            </div>
            <div className="card p-4">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-500 text-sm">Expenses</p><h3 className="font-bold text-2xl">₦{((finance.expenses)/1000000).toFixed(1)}M</h3></div>
                <TrendingUp className="w-8 h-8 text-purple-600" />
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <a href="/dashboard/fees" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <DollarSign className="w-8 h-8 text-blue-600" /><div><p className="font-medium">Fee Structure</p><p className="text-xs text-gray-500">Manage fees</p></div>
            </a>
            <a href="/dashboard/payments" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <CreditCard className="w-8 h-8 text-green-600" /><div><p className="font-medium">Payments</p><p className="text-xs text-gray-500">Transactions</p></div>
            </a>
            <a href="/dashboard/invoices" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <FileText className="w-8 h-8 text-purple-600" /><div><p className="font-medium">Invoices</p><p className="text-xs text-gray-500">Generate</p></div>
            </a>
            <a href="/dashboard/scholarships" className="card p-4 flex items-center gap-3 hover:shadow-md">
              <Award className="w-8 h-8 text-amber-600" /><div><p className="font-medium">Scholarships</p><p className="text-xs text-gray-500">Awards</p></div>
            </a>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Recent Transactions</h2></div>
              <div className="divide-y divide-gray-100">
                {recent.map(tx => (
                  <div key={tx.id} className="p-4 flex items-center justify-between">
                    <div><p className="font-medium">{tx.student}</p><p className="text-sm text-gray-500">₦{tx.amount.toLocaleString()} • {tx.type} • {tx.date}</p></div>
                    <span className={`px-3 py-1 rounded-full text-xs ${tx.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>{tx.status}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="card">
              <div className="p-4 border-b border-gray-100"><h2 className="font-semibold">Quick Actions</h2></div>
              <div className="p-4 space-y-3">
                <button className="btn btn-secondary w-full justify-start">Generate Bulk Invoices</button>
                <button className="btn btn-secondary w-full justify-start">Export Payment Report</button>
                <button className="btn btn-secondary w-full justify-start">Reconcile Transactions</button>
                <button className="btn btn-secondary w-full justify-start">Generate Payroll CSV</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}