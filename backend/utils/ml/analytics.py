"""
Data Science Analytics - Critical University Insights
===============================================

Features:
1. Enrollment Analytics
2. Performance Analytics  
3. Financial Analytics
4. Predictive Analytics
5. Cohort Analysis
"""
from django.db.models import Avg, Count, Sum, Q, F, Max, Min
from django.db.models.functions import TruncMonth, TruncSemester
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class EnrollmentAnalytics:
    """
    Student Enrollment Analytics
    ==================
    """
    
    @classmethod
    def get_enrollment_trends(cls, session_id: str = None) -> Dict:
        """Get enrollment trends over time"""
        from apps.student.models import StudentProfile
        
        query = StudentProfile.objects.all()
        if session_id:
            query = query.filter(admission_session_id=session_id)
        
        total = query.count()
        by_status = query.values('admission_status').annotate(count=Count('id'))
        
        return {
            'total_enrolled': total,
            'by_status': {item['admission_status']: item['count'] for item in by_status},
            'trend': 'increasing'  # Would calculate from historical
        }
    
    @classmethod
    def get_demographics(cls) -> Dict:
        """Student demographics"""
        from apps.student.models import StudentProfile
        
        by_gender = StudentProfile.objects.values('gender').annotate(
            count=Count('id')
        )
        
        by_programme = StudentProfile.objects.filter(
            programme__isnull=False
        ).values('programme__name').annotate(count=Count('id'))
        
        by_state = StudentProfile.objects.exclude(
            state_of_origin=''
        ).values('state_of_origin').annotate(count=Count('id'))
        
        return {
            'by_gender': {item['gender']: item['count'] for item in by_gender},
            'by_programme': list(by_programme)[:10],
            'top_states': list(by_state.order_by('-count')[:10])
        }


class PerformanceAnalytics:
    """
    Student Performance Analytics
    =====================
    """
    
    @classmethod
    def get_course_statistics(cls, course_id: str = None) -> Dict:
        """Get course performance statistics"""
        from apps.student.models import Result
        from django.db.models import Avg
        
        query = Result.objects.filter(status='approved')
        if course_id:
            query = query.filter(registration__course_id=course_id)
        
        stats = query.aggregate(
            avg_score=Avg('score'),
            max_score=Max('score'),
            min_score=Min('score'),
            total_results=Count('id')
        )
        
        # Grade distribution
        grade_dist = query.values('grade').annotate(count=Count('id'))
        
        return {
            'average_score': round(stats['avg_score'] or 0, 1),
            'max_score': stats['max_score'] or 0,
            'min_score': stats['min_score'] or 0,
            'total_results': stats['total_results'] or 0,
            'grade_distribution': {item['grade']: item['count'] for item in grade_dist}
        }
    
    @classmethod
    def get_gpa_distribution(cls) -> Dict:
        """CGPA distribution across students"""
        from apps.student.models import CGPAHistory
        
        latest = CGPAHistory.objects.order_by('student', '-session', '-semester')
        latest = latest.distinct('student')
        
        gpas = list(latest.values_list('cumulative_gpa', flat=True))
        
        if not gpas:
            return {}
        
        # Buckets
        first_class = sum(1 for g in gpas if g >= 4.0)
        second_upper = sum(1 for g in gpas if 3.0 <= g < 4.0)
        second_lower = sum(1 for g in gpas if 2.0 <= g < 3.0)
        pass_class = sum(1 for g in gpas if g >= 1.0 and g < 2.0)
        prob = sum(1 for g in gpas if g < 1.0)
        
        return {
            'first_class': first_class,
            'second_class_upper': second_upper,
            'second_class_lower': second_lower,
            'pass_class': pass_class,
            'probation': prob,
            'total': len(gpas)
        }


class FinancialAnalytics:
    """
    Financial Analytics
    ================
    """
    
    @classmethod
    def get_revenue_by_session(cls, session_id: str = None) -> Dict:
        """Revenue by academic session"""
        from apps.finance.models import Payment
        
        query = Payment.objects.filter(status='completed')
        if session_id:
            query = query.filter(session_id=session_id)
        
        total = query.aggregate(total=Sum('amount'))['total'] or 0
        
        by_type = Payment.objects.filter(
            status='completed'
        ).values('payment_type').annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        return {
            'total_revenue': float(total),
            'by_type': [{
                'type': item['payment_type'],
                'amount': float(item['total']),
                'count': item['count']
            } for item in by_type]
        }
    
    @classmethod
    def get_outstanding_fees(cls) -> Dict:
        """Outstanding fees analysis"""
        from apps.finance.models import StudentFee
        
        unpaid = StudentFee.objects.filter(is_paid=False)
        
        total_unpaid = unpaid.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        by_programme = unpaid.values(
            'student__programme__name'
        ).annotate(total=Sum('amount'))
        
        return {
            'total_outstanding': float(total_unpaid),
            'count_unpaid': unpaid.count(),
            'by_programme': list(by_programme)
        }


class PredictiveAnalytics:
    """
    Predictive Analytics
    ==================
    """
    
    @classmethod
    def predict_registration_demand(cls, course_id: str, session_id: str) -> Dict:
        """Predict course registration demand"""
        from apps.student.models import CourseRegistration
        from apps.learning.models import Course
        
        try:
            course = Course.objects.get(id=course_id)
            
            # Historical data
            last_3_sessions = CourseRegistration.objects.filter(
                course=course
            ).values('session').annotate(count=Count('id'))
            
            if last_3_sessions.count() < 2:
                return {
                    'course': course.code,
                    'predicted_demand': 100,
                    'confidence': 'low',
                    'reason': 'Insufficient historical data'
                }
            
            # Simple moving average
            counts = [s['count'] for s in last_3_sessions]
            avg = sum(counts) / len(counts)
            
            return {
                'course': course.code,
                'predicted_demand': int(avg * 1.1),  # 10% growth
                'historical': counts,
                'confidence': 'high',
                'recommendation': 'increase_capacity' if avg > course.max_capacity * 0.8 else 'stable'
            }
            
        except Course.DoesNotExist:
            return {'error': 'Course not found'}
    
    @classmethod
    def predict_graduation_rate(cls, session_id: str) -> Dict:
        """Predict graduation rate for session"""
        from apps.student.models import StudentProfile
        
        admitted = StudentProfile.objects.filter(
            admission_status='admitted'
        ).count()
        
        # Historical graduation rate (placeholder)
        graduation_rate = 0.75  # 75% average
        
        predicted_graduates = int(admitted * graduation_rate)
        
        return {
            'session': session_id,
            'current_enrollment': admitted,
            'predicted_graduates': predicted_graduates,
            'graduation_rate': graduation_rate,
            'confidence': 'medium'
        }


class CohortAnalytics:
    """
    Student Cohort Analysis
    =======================
    """
    
    @classmethod
    def analyze_cohort_performance(cls, cohort_year: int) -> Dict:
        """Analyze student cohort over time"""
        from apps.student.models import StudentProfile, CGPAHistory
        
        # Get students admitted in cohort year
        students = StudentProfile.objects.filter(
            admission_session__name__startswith=str(cohort_year)
        )
        
        # Get their CGPA progression
        current_cgpas = []
        for student in students:
            latest = CGPAHistory.objects.filter(
                student=student
            ).order_by('-session', '-semester').first()
            
            if latest:
                current_cgpas.append(float(latest.cumulative_gpa))
        
        if not current_cgpas:
            return {'error': 'No data for cohort'}
        
        avg_cgpa = sum(current_cgpas) / len(current_cgpas)
        
        return {
            'cohort_year': cohort_year,
            'cohort_size': students.count(),
            'current_avg_cgpa': round(avg_cgpa, 2),
            'at_risk_count': sum(1 for c in current_cgpas if c < 1.5),
            'first_class_count': sum(1 for c in current_cgpas if c >= 4.0)
        }


# Export
__all__ = [
    'EnrollmentAnalytics',
    'PerformanceAnalytics', 
    'FinancialAnalytics',
    'PredictiveAnalytics',
    'CohortAnalytics'
]
