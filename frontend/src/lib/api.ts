/**
 * UniCore API Client
 * ==============
 * TypeScript client for Django Ninja API
 */
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  count?: number;
  results?: T[];
}

interface ApiError {
  detail?: string;
  [key: string]: unknown;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
    // Try to load token from localStorage on client
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle 401 - token expired
    if (response.status === 401 && this.token) {
      const refreshed = await this.refreshToken();
      if (refreshed) {
        return this.request<T>(endpoint, options);
      } else {
        this.clearToken();
        throw new Error('Session expired');
      }
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    return data as T;
  }

  // Auth
  async login(email: string, password: string) {
    const data = await this.request<{ access: string; refresh: string }>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(data.access);
    return data;
  }

  async logout() {
    this.clearToken();
  }

  async refreshToken() {
    if (!this.token) return false;
    
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) return false;

      const data = await this.request<{ access: string }>('/auth/refresh/', {
        method: 'POST',
        body: JSON.stringify({ refresh }),
      });
      
      this.setToken(data.access);
      return true;
    } catch {
      return false;
    }
  }

  async getMe() {
    return this.request<any>('/auth/me/');
  }

  // Academic
  async getFaculties() {
    return this.request<any[]>('/academic/faculties/');
  }

  async getDepartments(facultyId?: string) {
    const params = facultyId ? `?faculty=${facultyId}` : '';
    return this.request<any[]>(`/academic/departments/${params}`);
  }

  async getProgrammes(departmentId?: string) {
    const params = departmentId ? `?department=${departmentId}` : '';
    return this.request<any[]>(`/academic/programmes/${params}`);
  }

  async getCourses(programmeId?: string) {
    const params = programmeId ? `?programme=${programmeId}` : '';
    return this.request<any[]>(`/academic/courses/${params}`);
  }

  // Student
  async getMyProfile() {
    return this.request<any>('/students/me/');
  }

  async getMyResults() {
    return this.request<any>('/students/me/results/');
  }

  async getMyCourses() {
    return this.request<any>('/students/me/courses/');
  }

  async registerCourses(courseIds: string[]) {
    return this.request<any>('/students/me/register-courses/', {
      method: 'POST',
      body: JSON.stringify({ course_ids: courseIds }),
    });
  }

  async getMyTimetable(semesterId?: string) {
    const params = semesterId ? `?semester=${semesterId}` : '';
    return this.request<any>(`/students/me/timetable/${params}`);
  }

  async getMyFees() {
    return this.request<any>('/students/me/fees/');
  }

  async makePayment(amount: number, feeItemIds: string[]) {
    return this.request<any>('/payments/initialize/', {
      method: 'POST',
      body: JSON.stringify({ amount, fee_item_ids: feeItemIds }),
    });
  }

  // Lecturer
  async getMyCoursesAllocated() {
    return this.request<any[]>('/lecturer/courses/');
  }

  async getCourseMaterials(courseId: string) {
    return this.request<any[]>(`/courses/${courseId}/materials/`);
  }

  async uploadMaterial(courseId: string, file: File, title: string, type: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('type', type);

    return fetch(`${this.baseUrl}/courses/${courseId}/materials/`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
    });
  }

  async createAssignment(courseId: string, data: any) {
    return this.request<any>(`/courses/${courseId}/assignments/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getAssignments(courseId: string) {
    return this.request<any[]>(`/courses/${courseId}/assignments/`);
  }

  async createAttendanceSession(courseId: string, date: string) {
    return this.request<any>(`/courses/${courseId}/attendance-sessions/`, {
      method: 'POST',
      body: JSON.stringify({ date }),
    });
  }

  async submitGrades(courseId: string, results: any[]) {
    return this.request<any>('/lecturer/grade-sheet/', {
      method: 'POST',
      body: JSON.stringify({ course_id: courseId, results }),
    });
  }

  // Hostel
  async getHostels() {
    return this.request<any[]>('/hostels/');
  }

  async getHostelAllocations(sessionId?: string) {
    const params = sessionId ? `?session=${sessionId}` : '';
    return this.request<any[]>(`/hostel-allocations/${params}`);
  }

  // NYSC
  async getNYSCData() {
    return this.request<any[]>('/nysc/');
  }

  async exportNYSC(year?: string) {
    const params = year ? `?year=${year}` : '';
    return this.request<any[]>(`/nysc/export/${params}`);
  }

  // ML Services
  async predictCGPA(features: any) {
    return this.request<any>('/ml/predict-cgpa/', {
      method: 'POST',
      body: JSON.stringify(features),
    });
  }

  async getDropoutRisk(studentId: string) {
    return this.request<any>(`/ml/dropout-risk/${studentId}/`);
  }

  async getChatbotResponse(message: string) {
    return this.request<any>('/ml/chatbot/', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async analyzeSentiment(feedback: string) {
    return this.request<any>('/ml/sentiment/', {
      method: 'POST',
      body: JSON.stringify({ feedback }),
    });
  }

  // Settings
  async getSettings() {
    return this.request<any>('/settings/');
  }

  async updateSettings(data: any) {
    return this.request<any>('/settings/', {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }
}

// Export singleton
export const api = new ApiClient();
export { ApiClient };
export type { ApiResponse, ApiError };