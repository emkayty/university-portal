# UniCore v4.0 - University Operating System

A production-ready, white-label university web portal built to Nigerian & global university standards.

## Features

- **7 Role-Based Dashboards**: Student, Lecturer, HOD, Dean, Registrar, Bursar, Institution Admin
- **Setup Wizard**: Brand customization, grading system (British/American/Custom), calendar, payment gateway
- **Learning Management**: Materials, assignments, quizzes, attendance with QR codes
- **Result Workflow**: Lecturer → HOD → Dean → Senate approval pipeline
- **Finance**: Fee management, Paystack/Flutterwave integration, payroll
- **Offline PWA**: Offline materials, queued attendance, sync when online
- **Nigerian Standards**: JAMB integration, NYSC export, NDPR compliance

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure your environment
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
cd provision
./provision.sh  # Creates new instance
```

## Tech Stack

- Backend: Python 3.12, Django 5.1, Django Ninja, PostgreSQL 16
- Frontend: Next.js 15, TypeScript, Tailwind CSS 4
- Auth: JWT (django-ninja-jwt)
- Payments: Paystack, Flutterwave
- Storage: S3-compatible

## Project Structure

```
backend/
├── unicore/           # Django project
├── apps/             # All applications
│   ├── accounts/     # User, roles, auth
│   ├── institution/  # Settings, wizard
│   ├── academic/    # Faculty, dept, courses
│   ├── student/    # Student lifecycle
│   ├── staff/      # Staff management
│   ├── learning/   # Materials, assignments
│   ├── finance/   # Fees, payments
│   └── offline/   # Sync
└── utils/           # Grading, PDF, QR

frontend/
├── src/
│   ├── app/        # Pages
│   ├── components/  # UI components
│   ├── hooks/      # useAuth
│   └── lib/        # API client
└── public/         # Static assets
```

## API Endpoints

All endpoints under `/api/v1/`:
- Auth: `/auth/login`, `/auth/refresh`, `/auth/me`
- Settings: `/settings`
- Academic: `/faculties`, `/departments`, `/courses`, `/grading-policies`
- Student: `/students/me`, `/registrations`, `/results`, `/cgpa`
- Learning: `/materials`, `/assignments`, `/quizzes`, `/attendance`
- Finance: `/fees`, `/payments`, `/scholarships`

## Documentation

See full specification in project specification document.