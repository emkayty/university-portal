/**
 * UniCore TypeScript Types
 * ===================
 * Types mirroring Django models and schemas for frontend-backend alignment
 */

// ============================================================================
// USER & AUTH
// ============================================================================

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  last_login?: string;
}

export type UserRole = 
  | 'student' 
  | 'lecturer' 
  | 'hod' 
  | 'dean' 
  | 'registrar' 
  | 'bursar' 
  | 'institution_admin';

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse extends AuthTokens {
  user: User;
}

// ============================================================================
// ACADEMIC STRUCTURE
// ============================================================================

export interface Faculty {
  id: string;
  name: string;
  code: string;
  dean?: User;
  created_at: string;
}

export interface Department {
  id: string;
  name: string;
  code: string;
  faculty: Faculty;
  hod?: User;
  created_at: string;
}

export interface Programme {
  id: string;
  name: string;
  code: string;
  duration_years: number;
  department: Department;
  grading_policy?: GradingPolicy;
  created_at: string;
}

export interface Course {
  id: string;
  code: string;
  title: string;
  credit_units: number;
  level: number;
  semester_offered: number;
  programme: Programme;
  department: Department;
  has_prerequisites: boolean;
}

export interface CoursePrerequisite {
  id: string;
  course: Course;
  prerequisite_course: Course;
  minimum_grade?: string;
}

export interface GradingPolicy {
  id: string;
  name: string;
  scale_type: 'british' | 'american' | 'custom';
  grade_boundaries: GradeBoundary[];
  pass_mark: number;
  max_score: number;
  cgpa_formula: string;
}

export interface GradeBoundary {
  grade: string;
  min_score: number;
  grade_point: number;
}

export interface AcademicSession {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
}

export interface Semester {
  id: string;
  name: string;
  session: AcademicSession;
  start_date: string;
  end_date: string;
  registration_start: string;
  registration_end: string;
}

// ============================================================================
// STUDENT
// ============================================================================

export interface StudentProfile {
  id: string;
  user: User;
  matric_number?: string;
  first_name: string;
  last_name: string;
  gender: 'M' | 'F';
  phone: string;
  date_of_birth?: string;
  nationality: string;
  state_of_origin?: string;
  lga?: string;
  programme: Programme;
  current_level: number;
  admission_status: AdmissionStatus;
  clearance_status: ClearanceStatus;
}

export type AdmissionStatus = 
  | 'applicant'
  | 'admitted'
  | 'deferred'
  | 'suspended'
  | 'withdrawn'
  | 'graduated';

export type ClearanceStatus = 
  | 'pending'
  | 'in_progress'
  | 'completed';

export interface AdmissionApplication {
  id: string;
  student_profile: StudentProfile;
  jamb_reg_no: string;
  jamb_score?: number;
  o_level_result: Record<string, any>;
  application_session: AcademicSession;
  status: string;
  reviewer?: User;
}

export interface CourseRegistration {
  id: string;
  student: StudentProfile;
  course: Course;
  session: AcademicSession;
  semester: Semester;
  status: 'active' | 'dropped';
  registered_at: string;
}

export interface TimetableEntry {
  id: string;
  course: Course;
  day_of_week: number;
  start_time: string;
  end_time: string;
  venue: string;
}

export interface Result {
  id: string;
  registration: CourseRegistration;
  session: AcademicSession;
  semester: Semester;
  course_code: string;
  course_title: string;
  score: number;
  grade: string;
  grade_point: number;
  status: ResultStatus;
}

export type ResultStatus = 
  | 'pending'
  | 'approved'
  | 'rejected';

export interface CGPAHistory {
  id: string;
  student: StudentProfile;
  session: AcademicSession;
  semester: Semester;
  gpa: number;
  cumulative_gpa: number;
}

// ============================================================================
// STAFF
// ============================================================================

export interface StaffProfile {
  id: string;
  user: User;
  staff_id: string;
  first_name: string;
  last_name: string;
  department: Department;
  employment_date: string;
  rank: string;
  contract_type: string;
}

export interface LeaveRequest {
  id: string;
  staff: StaffProfile;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  approved_by?: User;
  approval_comment?: string;
}

export interface LeaveBalance {
  id: string;
  staff: StaffProfile;
  leave_type: string;
  total_days: number;
  used_days: number;
  session: AcademicSession;
}

// ============================================================================
// LEARNING
// ============================================================================

export interface Material {
  id: string;
  course: Course;
  lecturer: StaffProfile;
  title: string;
  file_url: string;
  type: MaterialType;
  uploaded_at: string;
  is_offline_available: boolean;
}

export type MaterialType = 
  | 'pdf'
  | 'video'
  | 'link'
  | 'document';

export interface Assignment {
  id: string;
  course: Course;
  lecturer: StaffProfile;
  title: string;
  description: string;
  due_date: string;
  max_score: number;
  grading_rubric?: Record<string, any>;
}

export interface AssignmentSubmission {
  id: string;
  assignment: Assignment;
  student: StudentProfile;
  file_url?: string;
  text_answer?: string;
  submitted_at: string;
  score?: number;
  feedback?: string;
  status: 'pending' | 'submitted' | 'graded';
}

export interface Quiz {
  id: string;
  course: Course;
  lecturer: StaffProfile;
  title: string;
  duration_minutes: number;
  start_time: string;
  end_time: string;
  questions: QuizQuestion[];
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_option: number;
}

export interface QuizAttempt {
  id: string;
  quiz: Quiz;
  student: StudentProfile;
  started_at: string;
  submitted_at?: string;
  answers: Record<string, any>;
  score_total?: number;
}

export interface AttendanceSession {
  id: string;
  course: Course;
  lecturer: StaffProfile;
  date: string;
  qr_code_token: string;
  is_active: boolean;
}

export interface AttendanceRecord {
  id: string;
  session: AttendanceSession;
  student: StudentProfile;
  timestamp: string;
  method: 'qr' | 'manual';
}

// ============================================================================
// FINANCE
// ============================================================================

export interface FeeItem {
  id: string;
  name: string;
  amount: number;
  is_compulsory: boolean;
  programme?: Programme;
  session: AcademicSession;
  level: number;
}

export interface StudentFee {
  id: string;
  student: StudentProfile;
  fee_item: FeeItem;
  amount_due: number;
  amount_paid: number;
  status: FeeStatus;
}

export type FeeStatus = 
  | 'pending'
  | 'partial'
  | 'paid';

export interface Payment {
  id: string;
  student: StudentProfile;
  amount: number;
  payment_ref: string;
  gateway: 'paystack' | 'flutterwave';
  status: PaymentStatus;
  paid_at?: string;
}

export type PaymentStatus = 
  | 'pending'
  | 'completed'
  | 'failed';

export interface Scholarship {
  id: string;
  student: StudentProfile;
  name: string;
  amount: number;
  awarded_by: string;
  session: AcademicSession;
}

// ============================================================================
// HOSTEL & ACCOMMODATION
// ============================================================================

export interface Hostel {
  id: string;
  name: string;
  code: string;
  gender: 'male' | 'female' | 'mixed';
  total_beds: number;
  available_beds: number;
  warden?: StaffProfile;
  address: string;
}

export interface Room {
  id: string;
  hostel: Hostel;
  room_number: string;
  floor: number;
  capacity: number;
  current_occupants: number;
  room_type: RoomType;
  gender: string;
  fee: number;
  is_available: boolean;
}

export type RoomType = 
  | 'single'
  | 'double'
  | 'triple'
  | '4-in-1';

export interface HostelAllocation {
  id: string;
  student: StudentProfile;
  room: Room;
  session: AcademicSession;
  bed_number: string;
  check_in_date?: string;
  check_out_date?: string;
  is_active: boolean;
}

// ============================================================================
// COURSE ALLOCATION
// ============================================================================

export interface CourseAllocation {
  id: string;
  course: Course;
  lecturer: StaffProfile;
  session: AcademicSession;
  semester: Semester;
  is_primary: boolean;
  workload_hours: number;
  is_active: boolean;
}

// ============================================================================
// NYSC
// ============================================================================

export interface NYSCData {
  id: string;
  student: StudentProfile;
  state_code: string;
  callup_number: string;
  nysc_year: number;
  ppa_state: string;
  ppa_lga: string;
  ppa_organisation: string;
  service_status: NYSCStatus;
  start_date?: string;
  end_date?: string;
}

export type NYSCStatus = 
  | 'pending'
  | 'posted'
  | 'service_ongoing'
  | 'completed'
  | 'exempted';

// ============================================================================
// ID CARDS
// ============================================================================

export interface StudentIDCard {
  id: string;
  student: StudentProfile;
  card_number: string;
  card_type: IDCardType;
  photo_url?: string;
  is_approved: boolean;
  approved_by?: StaffProfile;
  issue_date?: string;
  expiry_date?: string;
  is_active: boolean;
}

export type IDCardType = 
  | 'temporary'
  | 'permanent'
  | 'visitor';

// ============================================================================
// ALUMNI
// ============================================================================

export interface Alumni {
  id: string;
  student: StudentProfile;
  graduation_year: number;
  class_of_degree: DegreeClass;
  current_employer?: string;
  job_title?: string;
  employment_sector: EmploymentSector;
}

export type DegreeClass = 
  | 'first_class'
  | 'second_class_upper'
  | 'second_class_lower'
  | 'third_class'
  | 'pass';

export type EmploymentSector = 
  | 'public'
  | 'private'
  | 'self_employed'
  | 'ngos'
  | 'entrepreneur'
  | 'further_study'
  | 'unemployed';

// ============================================================================
// MEDICAL RECORDS
// ============================================================================

export interface MedicalRecord {
  id: string;
  student: StudentProfile;
  blood_group: BloodGroup;
  genotype: Genotype;
  has_allergies: boolean;
  allergies_detail?: string;
  has_chronic_conditions: boolean;
  conditions_detail?: string;
  on_medication: boolean;
  medication_detail?: string;
  has_disability: boolean;
  disability_type?: string;
  disability_detail?: string;
  requires_special_accommodation: boolean;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  emergency_contact_relationship: string;
}

export type BloodGroup = 'A+' | 'A-' | 'B+' | 'B-' | 'AB+' | 'AB-' | 'O+' | 'O-';
export type Genotype = 'AA' | 'AS' | 'SS' | 'AC' | 'SC';

// ============================================================================
// ML SERVICES
// ============================================================================

export interface CGPAPrediction {
  predicted_score: number;
  grade: string;
  grade_point: number;
  confidence: 'low' | 'medium' | 'high';
  recommendation: string;
}

export interface StudentFeatures {
  attendance_rate: number;
  assignment_score: number;
  quiz_score: number;
  avg_midterm: number;
  study_hours_per_week: number;
  previous_gpa: number;
  credits_registered: number;
  level: number;
}

export interface DropoutRisk {
  student_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  factors: string[];
  interventions: string[];
}

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export interface CourseRecommendation {
  course: Course;
  match_score: number;
  reason: string;
}

export interface ChatbotResponse {
  topic: string;
  answer: string;
  confidence: number;
  related_topics: string[];
}

export interface SentimentAnalysis {
  sentiment: 'positive' | 'neutral' | 'negative';
  score: number;
  positive_indicators: number;
  negative_indicators: number;
}

// ============================================================================
// SETTINGS
// ============================================================================

export interface InstitutionSettings {
  institution_name: string;
  motto: string;
  logo_url: string;
  primary_color: string;
  secondary_color: string;
  grading_scale_type: 'british' | 'american' | 'custom';
  grading_boundaries: GradeBoundary[];
  academic_year_start: string;
  semester_structure: SemesterStructure[];
  payment_gateway: 'paystack' | 'flutterwave' | null;
  setup_complete: boolean;
}

export interface SemesterStructure {
  name: string;
  weeks: number;
}

// ============================================================================
// API RESPONSE WRAPPERS
// ============================================================================

export interface PaginatedResponse<T> {
  count: number;
  results: T[];
  next?: string;
  previous?: string;
}

export interface ApiError {
  detail: string;
}