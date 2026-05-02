"""
UniCore ML/AI Services - Critical University Features
===============================================

Features:
1. CGPA Prediction - Predict student final grade
2. Dropout Risk Detection - Early warning system
3. Course Recommendation - Suggest courses
4. Student Similarity - Peer matching
5. Anomaly Detection - Unusual patterns
"""
import numpy as np
from django.db.models import Avg, Count, Q
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class StudentFeatures:
    """Feature vector for student ML models"""
    attendance_rate: float       # 0-100
    assignment_score: float      # 0-100
    quiz_score: float           # 0-100
    avg_midterm: float         # 0-100
    study_hours_per_week: float
    previous_gpa: float        # 0-5.0
    credits_registered: int
    level: int                 # 100-500
    
    def to_vector(self) -> List[float]:
        return [
            self.attendance_rate / 100,
            self.assignment_score / 100,
            self.quiz_score / 100,
            self.avg_midterm / 100,
            min(self.study_hours_per_week / 40, 1),
            self.previous_gpa / 5,
            min(self.credits_registered / 30, 1),
            self.level / 500
        ]


class CGPAPredictor:
    """
    CGPA/Final Grade Prediction
    =====================
    Uses weighted features to predict expected final grade.
    In production, this would use a trained sklearn/TensorFlow model.
    """
    
    # Feature weights (simple linear model - would be learned)
    WEIGHTS = {
        'attendance': 0.15,
        'assignment': 0.20,
        'quiz': 0.15,
        'midterm': 0.30,
        'study_hours': 0.10,
        'previous': 0.10
    }
    
    @classmethod
    def predict_final_grade(cls, features: StudentFeatures) -> Dict:
        """
        Predict final grade for a course
        
        Args:
            features: Student feature vector
            
        Returns:
            Dict with predicted_score, confidence, recommendation
        """
        # Simple weighted average (placeholder for ML model)
        score = (
            features.attendance_rate * cls.WEIGHTS['attendance'] +
            features.assignment_score * cls.WEIGHTS['assignment'] +
            features.quiz_score * cls.WEIGHTS['quiz'] +
            features.avg_midterm * cls.WEIGHTS['midterm'] +
            min(features.study_hours_per_week * 2.5, 100) * cls.WEIGHTS['study_hours'] +
            features.previous_gpa * 20 * cls.WEIGHTS['previous']
        )
        
        # Map to grade
        grade, grade_point = cls._score_to_grade(score)
        
        return {
            'predicted_score': round(score, 1),
            'grade': grade,
            'grade_point': grade_point,
            'confidence': 'high' if features.avg_midterm > 0 else 'medium',
            'recommendation': cls._get_recommendation(score)
        }
    
    @classmethod
    def _score_to_grade(cls, score: float) -> Tuple[str, float]:
        """Convert numeric score to grade"""
        if score >= 70:
            return 'A', 5.0
        elif score >= 60:
            return 'B', 4.0
        elif score >= 50:
            return 'C', 3.0
        elif score >= 45:
            return 'D', 2.0
        elif score >= 40:
            return 'E', 1.0
        return 'F', 0.0
    
    @classmethod
    def _get_recommendation(cls, score: float) -> str:
        """Get study recommendation"""
        if score >= 70:
            return "Excellent! Maintain current effort."
        elif score >= 60:
            return "Good. Slight increase in study hours recommended."
        elif score >= 50:
            return "Average. Increase assignment submissions and attend all classes."
        elif score >= 40:
            return "At risk. Consider tutorial sessions and office hours."
        return "Critical. Seek immediate academic counseling."


class DropoutRiskDetector:
    """
    Dropout Risk Detection
    ====================
    Identifies at-risk students based on:
    - Academic performance decline
    - Low attendance
    - Non-payment of fees
    - Failed courses
    """
    
    RISK_WEIGHTS = {
        'gpa_decline': 0.25,
        'attendance': 0.20,
        'failed_courses': 0.25,
        'fee_balance': 0.15,
        'engagement': 0.15
    }
    
    @classmethod
    def calculate_risk_score(cls, student_id: str) -> Dict:
        """
        Calculate dropout risk score for a student
        
        Returns:
            Dict with risk_level (low/medium/high/critical), 
            risk_score (0-100), factors, interventions
        """
        # In production, fetch real data from DB
        # Placeholder implementation
        risk_factors = []
        risk_score = 0
        
        # This would be replaced with actual DB queries
        # Example factors:
        # - gpa_decline: > 0.5 drop = 25 points
        # - attendance < 75%: 20 points
        # - failed_courses > 2: 25 points
        # - fee_balance > threshold: 15 points
        # - low_engagement: 15 points
        
        return {
            'student_id': student_id,
            'risk_score': risk_score,
            'risk_level': cls._score_to_level(risk_score),
            'factors': risk_factors,
            'interventions': cls._get_interventions(risk_score)
        }
    
    @classmethod
    def _score_to_level(cls, score: float) -> str:
        """Map risk score to level"""
        if score >= 75:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 25:
            return 'medium'
        return 'low'
    
    @classmethod
    def _get_interventions(cls, score: float) -> List[str]:
        """Get recommended interventions"""
        if score >= 75:
            return [
                "Immediate academic counseling",
                "Mandatory study group assignment",
                "Contact parent/guardian",
                "Review scholarship eligibility"
            ]
        elif score >= 50:
            return [
                "Weekly check-in with advisor",
                "Peer tutoring referral",
                "Payment plan for fees"
            ]
        elif score >= 25:
            return [
                " attendance monitoring",
                "Mid-semester feedback"
            ]
        return ["Continue current support"]


class CourseRecommender:
    """
    Course Recommendation System
    =========================
    Recommends courses based on:
    - Student career goals
    - Previous performance
    - Prerequisite completion
    - Programme requirements
    """
    
    @classmethod
    def recommend_courses(cls, student_id: str, limit: int = 5) -> List[Dict]:
        """
        Recommend courses for a student
        
        Returns:
            List of recommended courses with match_score
        """
        # Placeholder - in production, this would:
        # 1. Fetch student profile and career goal
        # 2. Check programme requirements
        # 3. Consider prerequisite completion
        # 4. Use collaborative filtering
        
        recommendations = []
        
        return recommendations
    
    @classmethod
    def calculate_match_score(cls, student, course) -> float:
        """
        Calculate how well a course matches a student
        
        Uses:
        - Career alignment (40%)
        - Prerequisite completion (30%)
        - Difficulty vs ability (20%)
        - Programme requirement (10%)
        """
        # Placeholder
        return 75.0


class StudentSimilarity:
    """
    Student Similarity / Peer Matching
    ===================================
    Find similar students for:
    - Study groups
    - Peer mentoring
    - Research collaboration
    """
    
    FEATURES = ['gpa', 'programme', 'courses', 'interests', 'level']
    
    @classmethod
    def find_similar_students(
        cls, 
        student_id: str, 
        n: int = 5,
        exclude_ids: List[str] = None
    ) -> List[Dict]:
        """
        Find n most similar students
        
        Uses cosine similarity on feature vectors
        """
        # Placeholder - would use actual DB data
        return []


class AnomalyDetector:
    """
    Anomaly Detection
    ===============
    Detects unusual patterns:
    - Grade spikes/drops
    - Attendance anomalies
    - Fee payment patterns
    """
    
    @classmethod
    def detect_grade_anomaly(cls, student_id: str) -> Dict:
        """Detect unusual grade patterns"""
        # Placeholder for grade anomaly detection
        return {
            'has_anomaly': False,
            'pattern': 'normal',
            'details': None
        }
    
    @classmethod
    def detect_attendance_anomaly(cls, student_id: str) -> Dict:
        """Detect unusual attendance patterns"""
        return {
            'has_anomaly': False,
            'details': None
        }


class ChatbotService:
    """
    University FAQ Chatbot
    ==================
    Handles common questions:
    - Admission requirements
    - Fees and payment
    - Hostel allocation
    - Exam schedules
    - Transcript requests
    """
    
    # FAQ knowledge base
    KNOWLEDGE_BASE = {
        ' admission': {
            'keywords': ['admission', 'apply', 'entry', 'jamb', 'post-utme'],
            'answer': ''' For undergraduate admission:
            1. Have at least 5 O'Level credits including English and Mathematics
            2. Meet JAMB cutoff mark
            3. Pass institution's Post-UTME screening
            4. Choose institution as first choice
            Contact admissions@uni.edu.ng for details.'''
        },
        'fees': {
            'keywords': ['fees', 'school fees', 'payment', 'tution', 'balance'],
            'answer': '''School fees varies by programme:
            - Science: ₦150,000 per session
            - Arts: ₦120,000 per session
            - Payment plans available (2 installments)
            Log in to student portal for your specific fee structure.'''
        },
        'hostel': {
            'keywords': ['hostel', 'accommodation', 'room', 'bed', ' lodging'],
            'answer': '''Hostel allocation:
            1. Apply online after registration
            2. Pay accommodation fee
            3. Beds allocated by faculty and level
            4. Hostel registration opens Week 2 of semester'''
        },
        'result': {
            'keywords': ['result', 'grade', 'score', 'cgpa'],
            'answer': '''View results:
            1. Log student portal
            2. Go to Academic > Results
            3. Select semester
            4. Results available after Senate approval'''
        },
        'transcript': {
            'keywords': ['transcript', 'certificate', 'document'],
            'answer': '''Request transcript:
            1. Clear all fees with Bursary
            2. Apply via student portal (₦5,000)
            3. Process in 5-7 working days
            4. Collect from Academic Office'''
        }
    }
    
    @classmethod
    def get_response(cls, query: str) -> Dict:
        """
        Get chatbot response to query
        
        Args:
            query: User's question
            
        Returns:
            Dict with answer, confidence, related_topics
        """
        query = query.lower()
        
        # Find matching topic
        for topic, data in cls.KNOWLEDGE_BASE.items():
            if any(kw in query for kw in data['keywords']):
                return {
                    'topic': topic,
                    'answer': data['answer'],
                    'confidence': 0.9,
                    'related_topics': list(cls.KNOWLEDGE_BASE.keys())[:3]
                }
        
        # No match
        return {
            'topic': None,
            'answer': '''I'm not sure about that. Please contact:
            - Admissions: admissions@uni.edu.ng
            - Bursary: bursary@uni.edu.ng
            - Student Affairs: studentaffairs@uni.edu.ng''',
            'confidence': 0.3,
            'related_topics': list(cls.KNOWLEDGE_BASE.keys())
        }


class SentimentAnalyzer:
    """
    Course Feedback Sentiment Analysis
    ====================
    Analyzes course/instructor feedback
    """
    
    @classmethod
    def analyze_feedback(cls, text: str) -> Dict:
        """
        Analyze feedback sentiment
        
        Returns:
            Dict with sentiment (positive/neutral/negative), 
            score (-1 to 1), keywords
        """
        text = text.lower()
        
        # Simple keyword-based sentiment
        positive_words = ['good', 'excellent', 'great', 'helpful', 'clear', 'engaging']
        negative_words = ['bad', 'poor', 'confusing', 'boring', 'late', 'unfair']
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            score = 0.7
        elif neg_count > pos_count:
            sentiment = 'negative'
            score = -0.7
        else:
            sentiment = 'neutral'
            score = 0.0
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_indicators': pos_count,
            'negative_indicators': neg_count
        }


class CapacityForecaster:
    """
    Course Capacity Forecasting
    ====================
    Predicts course demand for planning
    """
    
    @classmethod
    def predict_demand(cls, course_id: str, session_id: str) -> Dict:
        """
        Predict registration demand
        
        Returns:
            Dict with predicted_count, confidence, recommendation
        """
        # Placeholder - would use historical data
        return {
            'course_id': course_id,
            'predicted_registrations': 150,
            'capacity_threshold': 200,
            'confidence': 'medium',
            'recommendation': 'no_action'
        }


# Export all services
__all__ = [
    'StudentFeatures',
    'CGPAPredictor', 
    'DropoutRiskDetector',
    'CourseRecommender',
    'StudentSimilarity',
    'AnomalyDetector',
    'ChatbotService',
    'SentimentAnalyzer',
    'CapacityForecaster'
]