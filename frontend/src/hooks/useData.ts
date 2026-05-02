/**
 * Real Data Hooks for University Portal
 * ================================
 * Production-ready hooks with real API calls, NO demo data
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';

// =============================================================================
// TYPES
// =============================================================================

export interface User {
  id: string;
  email: string;
  role: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

export interface StudentProfile {
  id: string;
  matric_number: string | null;
  first_name: string;
  last_name: string;
  other_names?: string;
  gender: string;
  phone?: string;
  email: string;
  admission_status: string;
  current_level: number;
  programme: { id: string; name: string; code: string } | null;
  admission_session: { id: string; name: string } | null;
  clearance_progress: number;
}

export interface Course {
  id: string;
  code: string;
  title: string;
  credits: number;
  level: number;
  semester: string;
  programme: { name: string };
  lecturer: { first_name: string; last_name: string } | null;
  is_active: boolean;
}

export interface FeeRecord {
  id: string;
  name: string;
  amount: number;
  amount_paid: number;
  is_paid: boolean;
  due_date: string;
}

export interface TimetableEntry {
  id: string;
  course: { code: string; title: string };
  day_of_week: number;
  start_time: string;
  end_time: string;
  venue: string;
}

export interface Result {
  id: string;
  course: { code: string; title: string };
  session: { name: string };
  semester: { name: string };
  score: number;
  grade: string;
  grade_point: number;
  status: string;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export interface Analytics {
  total_students: number;
  total_staff: number;
  active_courses: number;
  average_gpa: number;
  graduation_rate: number;
}

// =============================================================================
// API BASE HOOK
// =============================================================================

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  immediate?: boolean;
}

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

function useApi<T>(
  fetchFn: () => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiState<T> & { refetch: () => Promise<void> } {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(options.immediate !== false);
  const [error, setError] = useState<Error | null>(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchFn();
      setData(result);
      options.onSuccess?.(result);
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e));
      setError(err);
      options.onError?.(err);
    } finally {
      setLoading(false);
    }
  }, [fetchFn, options.onSuccess, options.onError]);

  useEffect(() => {
    if (options.immediate !== false) {
      refetch();
    }
  }, [refetch, options.immediate]);

  return { data, loading, error, refetch };
}

// =============================================================================
// STUDENT HOOKS
// =============================================================================

export function useStudentProfile() {
  return useApi<StudentProfile>(() => api.getMyProfile(), { immediate: true });
}

export function useMyCourses() {
  return useApi<Course[]>(() => api.getMyCourses(), { immediate: true });
}

export function useMyResults() {
  return useApi<Result[]>(() => api.getMyResults(), { immediate: true });
}

export function useMyFees() {
  return useApi<FeeRecord[]>(() => api.getMyFees(), { immediate: true });
}

export function useMyTimetable() {
  return useApi<TimetableEntry[]>(() => api.getMyTimetable(), { immediate: true });
}

export function useMyNotifications() {
  return useApi<Notification[]>(() => 
    api.request<Notification[]>('/communication/notifications/'), 
    { immediate: true }
  );
}

// Combined student data
export function useStudentDashboard() {
  const profile = useStudentProfile();
  const courses = useMyCourses();
  const results = useMyResults();
  const fees = useMyFees();
  const notifications = useMyNotifications();

  return {
    profile: profile.data,
    courses: courses.data || [],
    results: results.data || [],
    fees: fees.data || [],
    notifications: notifications.data || [],
    loading: profile.loading || courses.loading || results.loading || fees.loading || notifications.loading,
    error: profile.error || courses.error || results.error || fees.error || notifications.error,
    refetch: async () => {
      await Promise.all([
        profile.refetch(),
        courses.refetch(),
        results.refetch(),
        fees.refetch(),
        notifications.refetch(),
      ]);
    },
  };
}

// =============================================================================
// LECTURER HOOKS
// =============================================================================

export function useLecturerCourses() {
  return useApi<Course[]>(() => api.getMyCoursesAllocated(), { immediate: true });
}

export function useCourseMaterials(courseId: string) {
  return useApi<any[]>(() => api.getCourseMaterials(courseId), { immediate: true });
}

export function useCourseAssignments(courseId: string) {
  return useApi<any[]>(() => api.getAssignments(courseId), { immediate: true });
}

// Combined lecturer data
export function useLecturerDashboard() {
  const courses = useLecturerCourses();

  return {
    courses: courses.data || [],
    loading: courses.loading,
    error: courses.error,
    refetch: courses.refetch,
  };
}

// =============================================================================
// ADMIN HOOKS
// =============================================================================

export function useAnalytics() {
  return useApi<Analytics>(() => 
    api.request<Analytics>('/reports/analytics/'), 
    { immediate: true }
  );
}

export function useAllStudents(params?: string) {
  return useApi<any[]>(() => 
    api.request<any[]>(`/students/all/${params ? `?${params}` : ''}`), 
    { immediate: true }
  );
}

export function useAllStaff() {
  return useApi<any[]>(() => 
    api.request<any[]>('/staff/all/'), 
    { immediate: true }
  );
}

export function useFaculties() {
  return useApi<any[]>(() => api.getFaculties(), { immediate: true });
}

export function useDepartments(facultyId?: string) {
  return useApi<any[]>(() => api.getDepartments(facultyId), { immediate: true });
}

// Combined admin data
export function useAdminDashboard() {
  const analytics = useAnalytics();
  const students = useAllStudents();
  const staff = useAllStaff();

  return {
    analytics: analytics.data,
    students: students.data || [],
    staff: staff.data || [],
    loading: analytics.loading || students.loading || staff.loading,
    error: analytics.error || students.error || staff.error,
    refetch: async () => {
      await Promise.all([
        analytics.refetch(),
        students.refetch(),
        staff.refetch(),
      ]);
    },
  };
}

// =============================================================================
// BURSAR HOOKS
// =============================================================================

export function useAllFees() {
  return useApi<any[]>(() => 
    api.request<any[]>('/finance/all-fees/'), 
    { immediate: true }
  );
}

export function useAllPayments() {
  return useApi<any[]>(() => 
    api.request<any[]>('/finance/all-payments/'), 
    { immediate: true }
  );
}

export function useFinanceAnalytics() {
  return useApi<any>(() => 
    api.request<any>('/reports/finance/'), 
    { immediate: true }
  );
}

export function useBursarDashboard() {
  const fees = useAllFees();
  const payments = useAllPayments();
  const analytics = useFinanceAnalytics();

  return {
    fees: fees.data || [],
    payments: payments.data || [],
    analytics: analytics.data,
    loading: fees.loading || payments.loading || analytics.loading,
    error: fees.error || payments.error || analytics.error,
    refetch: async () => {
      await Promise.all([fees.refetch(), payments.refetch(), analytics.refetch()]);
    },
  };
}

// =============================================================================
// REGISTRAR HOOKS
// =============================================================================

export function useAdmissions() {
  return useApi<any[]>(() => 
    api.request<any[]>('/students/admissions/'), 
    { immediate: true }
  );
}

export function useGraduations() {
  return useApi<any[]>(() => 
    api.request<any[]>('/students/graduations/'), 
    { immediate: true }
  );
}

export function useRegistrarDashboard() {
  const admissions = useAdmissions();
  const graduations = useGraduations();

  return {
    admissions: admissions.data || [],
    graduations: graduations.data || [],
    loading: admissions.loading || graduations.loading,
    error: admissions.error || graduations.error,
    refetch: async () => {
      await Promise.all([admissions.refetch(), graduations.refetch()]);
    },
  };
}

// =============================================================================
// ML/AI HOOKS
// =============================================================================

export function useDropoutRisk(studentId: string) {
  return useApi<any>(() => 
    api.getDropoutRisk(studentId), 
    { immediate: true }
  );
}

export function useCGPAPrediction(features: any) {
  return useApi<any>(() => 
    api.predictCGPA(features), 
    { immediate: true }
  );
}

export function useChatbot(message: string) {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);

  const sendMessage = useCallback(async () => {
    if (!message.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const result = await api.getChatbotResponse(message);
      setResponse(result);
    } catch (e) {
      setError(e instanceof Error ? e : new Error(String(e)));
    } finally {
      setLoading(false);
    }
  }, [message]);

  return { response, loading, error, sendMessage };
}

// =============================================================================
// EXPORT
// =============================================================================

export {
  useStudentProfile,
  useMyCourses,
  useMyResults,
  useMyFees,
  useMyTimetable,
  useMyNotifications,
  useStudentDashboard,
  useLecturerCourses,
  useCourseMaterials,
  useCourseAssignments,
  useLecturerDashboard,
  useAnalytics,
  useAllStudents,
  useAllStaff,
  useFaculties,
  useUseDepartments,
  useAdminDashboard,
  useAllFees,
  useAllPayments,
  useFinanceAnalytics,
  useBursarDashboard,
  useAdmissions,
  useGraduations,
  useRegistrarDashboard,
  useDropoutRisk,
  useCGPAPrediction,
  useChatbot,
};