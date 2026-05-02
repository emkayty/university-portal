# 🎓 UniCore v4.0 - Project Structure
# Complete File Organization

## DIRECTORY TREE

```
unicore/
│
├── 📁 BACKEND/                          # Django Backend
│   │
│   ├── manage.py                      # Django management
│   ├── requirements.txt            # Python dependencies
│   ├── pytest.ini                 # Test configuration
│   │
│   ├── 📂 unicore/                 # Django Project
│   │   ├── __init__.py
│   │   ├── settings.py          # Main settings
│   │   ├── urls.py             # URL routing
│   │   ├── wsgi.py           # WSGI config
│   │   ├── asgi.py           # ASGI config
│   │   └── __pycache__/
│   │
│   ├── 📂 apps/                   # Django Apps
│   │   ├── __init__.py          # App registry
│   │   │
│   │   ├── 📁 accounts/        # User Authentication
│   │   │   ├── __init__.py
│   │   │   ├── apps.py        # AppConfig
│   │   │   ├── models.py     # User model
│   │   │   ├── api.py      # Auth endpoints
│   │   │   ├── urls.py     # URL routes
│   │   │   ├── auth.py    # JWT auth
│   │   │   ├── backends.py  # Auth backends
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 academic/       # Academic Structure
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py    # Faculty, Dept, Programme, Course, Grading
│   │   │   ├── api.py     # CRUD endpoints
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 student/       # Student Management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # Profile, Admission, Result, NYSC
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 staff/         # Staff Management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # Profile, Leave, Promotion
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 learning/      # Learning & Teaching
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # Material, Assignment, Quiz, Attendance
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 finance/       # Finance & Payments
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # FeeItem, Payment, Scholarship
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 communication/  # Announcements
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # Announcement, Notification
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 institution/   # Settings
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # Settings, Branding
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 reports/       # Analytics
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── 📁 offline/       # Offline Sync
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py   # SyncQueue
│   │   │   ├── api.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   └── 📁 __pycache__/
│   │
│   ├── 📂 utils/                 # Utilities
│   │   ├── __init__.py
│   │   │
│   │   ├── 📁 ml/              # ML Services
│   │   │   ├── __init__.py
│   │   │   ├── ml_services.py   # CGPA predictor, Dropout risk, Chatbot
│   │   │   ├── api.py           # ML endpoints
│   │   │   └── urls.py
│   │   │
│   │   ├── data.py              # Nigerian data (states, LGAs)
│   │   ├── grading.py          # CGPA calculator
│   │   ├── pdf.py             # PDF generator
│   │   ├── qr.py              # QR utilities
│   │   └── nigerian.py         # Nigerian helpers
│   │
│   ├── 📂 templates/            # Email templates
│   │   ├── base.html
│   │   ├── welcome.html
│   │   └── password_reset.html
│   │
│   ├── 📂 static/              # Static files
│   │   └── css/
│   │
│   └── 📂 .env.example        # Environment template
│
│
├── 📁 FRONTEND/                  # Next.js Frontend
│   │
│   ├── package.json           # NPM config
│   ├── tsconfig.json       # TypeScript config
│   ├── tailwind.config.ts # Tailwind config
│   ├── next.config.js    # Next.js config
│   ├── .env.example    # Environment template
│   │
│   ├── public/              # Static assets
│   │   ├── manifest.json   # PWA manifest
│   │   ├── favicon.ico
│   │   └── icons/
│   │
│   └── src/
│       ├── app/             # App Router
│       │   ├── __init__.py
│       │   ├── layout.tsx     # Root layout
│       │   ├── page.tsx        # Login page
│       │   ├── globals.css
│       │   ├── providers.tsx
│       │   │
│       │   ├── 📁 (dashboard)/  # Protected routes
│       │   │   ├── __init__.py
│       │   │   ├── layout.tsx
│       │   │   │
│       │   │   └── 📁 student/   # Student role
│       │   │       ├── __init__.py
│       │   │       └── page.tsx
│       │   │
│       │   └── 📁 setup/       # Setup wizard
│       │       ├── __init__.py
│       │       └── page.tsx
│       │
│       ├── components/       # Reusable components
│       │   ├── __init__.py
│       │   │
│       │   └── 📁 layout/    # Layout components
│       │       ├── __init__.py
│       │       └── Dashboard.tsx  # Sidebar + Header
│       │
│       ├── lib/             # Library
│       │   ├── __init__.py
│       │   ├── api.ts        # API client
│       │   ├── utils.ts     # Utilities
│       │   └── constants.ts
│       │
│       ├── hooks/            # Custom hooks
│       │   ├── __init__.py
│       │   ├── useAuth.ts
│       │   └── useOffline.ts
│       │
│       ├── store/           # Zustand stores
│       │   ├── __init__.py
│       │   ├── auth.ts      # Auth state
│       │   └── institution.ts  # Institution state
│       │
│       ├── types/           # TypeScript types
│       │   ├── __init__.py
│       │   └── index.ts   # All interfaces
│       │
│       ├── styles/          # Styles
│       │   └── __init__.py
│       │
│       └── __pycache__/
│
│
├── 📁 PROVISION/                # Instance Provisioning
│   ├── __init__.py
│   ├── script.sh              # Bash provisioning script
│   └── template/             # Template files
│
├── 📁 DOCKER/                  # Container Configuration
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .dockerignore
│
├── 📁 DOCS/                   # Documentation
│   ├── README.md            # Main README
│   ├── ALIGNMENT.md         # Tech alignment
│   └── AUDIT.md           # Security audit
│
└── 📁 .gitignore           # Git ignore
```

---

## FILE NAMING CONVENTIONS

| Type | Convention | Example |
|------|------------|---------|
| Python | snake_case | `student_profile`, `api.py` |
| TypeScript | PascalCase | `StudentProfile`, `Dashboard.tsx` |
| CSS | kebab-case | `globals.css` |
| Config | kebab-case | `django.ini`, `pytest.ini` |

---

## IMPORT STRUCTURE

### Backend Imports
```python
# App imports
from apps.academic.models import Faculty, Department
from apps.student.models import StudentProfile
from apps.learning.models import Material, Assignment

# Utils imports
from utils.ml.services import CGPAPredictor
from utils.data import NIGERIAN_STATES
from utils.grading import calculate_cgpa

# Settings imports
from unicore import settings
```

### Frontend Imports
```typescript
// Components
import { DashboardSidebar } from '@/components/layout'

// Store
import { useAuthStore } from '@/store/auth'

// Types
import { User, StudentProfile } from '@/types'
```

---

## APP REGISTRY

| App | Label | Models | API |
|-----|-------|--------|-----|
| accounts | accounts | 1 | ✓ |
| academic | academic | 14 | ✓ |
| student | student | 12 | ✓ |
| staff | staff | 5 | ✓ |
| learning | learning | 7 | ✓ |
| finance | finance | 5 | ✓ |
| communication | communication | 4 | ✓ |
| institution | institution | 1 | ✓ |
| reports | reports | 1 | ✓ |
| offline | offline | 2 | ✓ |

---

## MODEL REFERENCE

### Academic App
- Faculty
- Department  
- Programme
- Course
- CoursePrerequisite
- AcademicSession
- Semester
- GradingPolicy
- Hostel
- Room
- HostelAllocation
- CourseAllocation
- CarryOverCourse
- AcademicWarning

### Student App
- StudentProfile
- AdmissionApplication
- CourseRegistration
- Result
- CGPAHistory
- GraduationClearance
- Transcript
- Certificate
- NYSCData
- StudentIDCard
- Alumni
- MedicalRecord

### Staff App
- StaffProfile
- LeaveRequest
- LeaveBalance
- PromotionRecord
- StaffAppraisal

### Learning App
- Material
- Assignment
- AssignmentSubmission
- Quiz
- QuizAttempt
- AttendanceSession
- AttendanceRecord

### Finance App
- FeeItem
- StudentFee
- Payment
- Scholarship
- PayrollRecord

### Communication App
- Announcement
- Notification
- Message
- AuditLog

---

## API ENDPOINT GROUPS

| Prefix | App | Endpoints |
|--------|-----|----------|
| `/auth/` | accounts | login, refresh, me |
| `/academic/` | academic | faculties, departments, programmes, courses |
| `/students/` | student | me, results, courses, fees |
| `/staff/` | staff | profile, leaves, appraisals |
| `/courses/` | learning | materials, assignments, quizzes |
| `/fees/` | finance | items, payments |
| `/ml/` | utils/ml | predict-cgpa, dropout-risk, chatbot |
| `/settings/` | institution | get, update |

---

## ENVIRONMENT VARIABLES

### Backend (.env)
```
SECRET_KEY=django-insecure-xxx
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=unicore
DB_USER=postgres
DB_PASSWORD=xxx
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
JWT_SECRET_KEY=xxx
PAYSTACK_SECRET_KEY=sk_xxx
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## DOCKER SERVICES

| Service | Image | Ports |
|--------|-------|-------|
| postgres | postgres:16 | 5432 |
| redis | redis:7 | 6379 |
| backend | unicore-backend | 8000 |
| frontend | unicore-frontend | 3000 |
| nginx | nginx | 80, 443 |

---

## DEPENDENCY GROUPS

### Core (requirements.txt)
- Django>=5.1
- djangorestframework>=3.14
- django-ninja>=0.21
- ninja-jwt>=2.7
- psycopg2-binary>=2.9
- redis>=5.0
- python-decouple>=3.8

### Development
- pytest>=8.0
- pytest-django>=4.8
- factory-boy>=3.3
- sentry-sdk>=1.40

### ML/AI
- scikit-learn>=1.4
- joblib>=1.3

### Frontend (package.json)
- next>=15.0
- react>=18.3
- typescript>=5.4
- tailwindcss>=4.0
- zustand>=4.5
- @tanstack/react-query>=5.28