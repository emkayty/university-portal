/**
 * Institution Settings Store
 * ========================
 * Manages institution branding and settings
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface InstitutionSettings {
  institution_name: string;
  motto: string;
  logo_url: string;
  primary_color: string;
  secondary_color: string;
  grading_scale_type: 'british' | 'american' | 'custom';
  grading_boundaries: { grade: string; min_score: number; grade_point: number }[];
  academic_year_start: string;
  semester_structure: { name: string; weeks: number }[];
  payment_gateway: 'paystack' | 'flutterwave' | null;
  setup_complete: boolean;
}

interface InstitutionState {
  settings: InstitutionSettings | null;
  isLoading: boolean;
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  
  setSettings: (settings: InstitutionSettings) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
}

// Default Nigerian grading scale
const DEFAULT_GRADING_BOUNDARIES = [
  { grade: 'A', min_score: 70, grade_point: 5.0 },
  { grade: 'B', min_score: 60, grade_point: 4.0 },
  { grade: 'C', min_score: 50, grade_point: 3.0 },
  { grade: 'D', min_score: 45, grade_point: 2.0 },
  { grade: 'E', min_score: 40, grade_point: 1.0 },
  { grade: 'F', min_score: 0, grade_point: 0.0 },
];

const DEFAULT_SEMESTER_STRUCTURE = [
  { name: 'First Semester', weeks: 15 },
  { name: 'Second Semester', weeks: 15 },
  { name: 'Break', weeks: 4 },
];

export const DEFAULT_SETTINGS: InstitutionSettings = {
  institution_name: 'University Name',
  motto: 'Education for Development',
  logo_url: '',
  primary_color: '#1e40af', // Blue-800
  secondary_color: '#059669', // Emerald-600
  grading_scale_type: 'british',
  grading_boundaries: DEFAULT_GRADING_BOUNDARIES,
  academic_year_start: '2024-10-01',
  semester_structure: DEFAULT_SEMESTER_STRUCTURE,
  payment_gateway: null,
  setup_complete: false,
};

export const useInstitutionStore = create<InstitutionState>()(
  persist(
    (set, get) => ({
      settings: null,
      isLoading: false,
      theme: 'light',
      sidebarOpen: true,

      setSettings: (settings) => set({ settings }),
      
      setTheme: (theme) => set({ theme }),
      
      toggleTheme: () => set((state) => ({ 
        theme: state.theme === 'light' ? 'dark' : 'light' 
      })),
      
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      toggleSidebar: () => set((state) => ({ 
        sidebarOpen: !state.sidebarOpen 
      })),
    }),
    {
      name: 'unicore-institution',
    }
  )
);