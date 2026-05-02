"""
UniCore ML Services API
====================
ML-powered services for university operations
"""
from django.views.decorators.api_view
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import json


def api_response(data, status=200):
    return Response(data, status=status)


def api_error(message, status_code=400):
    return Response({'success': False, 'error': message}, status=status_code)


# =============================================================================
# CGPA Prediction API
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_cgpa(request):
    """
    Predict student CGPA/Grade
    
    POST /api/v1/ml/predict-cgpa/
    Body: {
        "attendance_rate": 85,
        "assignment_score": 78,
        "quiz_score": 82,
        "avg_midterm": 75,
        "study_hours_per_week": 15,
        "previous_gpa": 3.5,
        "credits_registered": 18,
        "level": 200
    }
    """
    from utils.ml.ml_services import StudentFeatures, CGPAPredictor
    
    data = request.data
    features = StudentFeatures(
        attendance_rate=data.get('attendance_rate', 0),
        assignment_score=data.get('assignment_score', 0),
        quiz_score=data.get('quiz_score', 0),
        avg_midterm=data.get('avg_midterm', 0),
        study_hours_per_week=data.get('study_hours_per_week', 0),
        previous_gpa=data.get('previous_gpa', 0),
        credits_registered=data.get('credits_registered', 15),
        level=data.get('level', 100)
    )
    
    prediction = CGPAPredictor.predict_final_grade(features)
    
    return api_response({
        'success': True,
        'prediction': prediction
    })


# =============================================================================
# Dropout Risk API
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dropout_risk(request, student_id=None):
    """
    Calculate dropout risk score
    
    GET /api/v1/ml/dropout-risk/{student_id}/
    
    Returns: risk_level (low/medium/high/critical), risk_score (0-100)
    """
    from utils.ml.ml_services import DropoutRiskDetector
    
    if student_id is None and request.method == 'POST':
        student_id = request.data.get('student_id')
    
    if not student_id:
        return api_error('student_id required', status_code=400)
    
    # In production, fetch actual student data
    risk_analysis = DropoutRiskDetector.calculate_risk_score(student_id)
    
    return api_response({
        'success': True,
        'risk_analysis': risk_analysis
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def at_risk_students(request):
    """
    List all at-risk students
    
    GET /api/v1/ml/at-risk-students/?level=high
    
    Returns list of students with their risk scores
    """
    from utils.ml.ml_services import DropoutRiskDetector
    
    # In production, fetch from DB
    # Placeholder response
    level = request.query_params.get('level', 'high')
    
    return api_response({
        'success': True,
        'count': 0,
        'students': [],
        'level_filter': level
    })


# =============================================================================
# Course Recommendation API
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recommend_courses(request, student_id=None):
    """
    Recommend courses for a student
    
    GET /api/v1/ml/recommend-courses/{student_id}/
    POST /api/v1/ml/recommend-courses/
         Body: {"student_id": "xxx", "limit": 5}
    """
    from utils.ml.ml_services import CourseRecommender
    
    if student_id is None and request.method == 'POST':
        student_id = request.data.get('student_id')
    
    if not student_id:
        return api_error('student_id required', status_code=400)
    
    limit = request.query_params.get('limit', 5)
    try:
        limit = int(limit)
    except ValueError:
        limit = 5
    
    recommendations = CourseRecommender.recommend_courses(student_id, limit=limit)
    
    return api_response({
        'success': True,
        'student_id': student_id,
        'recommendations': recommendations
    })


# =============================================================================
# Chatbot API
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_message(request):
    """
    University FAQ Chatbot
    
    POST /api/v1/ml/chatbot/
    Body: {"message": "How do I apply for hostel?"}
    """
    from utils.ml.ml_services import ChatbotService
    
    message = request.data.get('message', '')
    
    if not message:
        return api_error('message required', status_code=400)
    
    response = ChatbotService.get_response(message)
    
    return api_response({
        'success': True,
        'response': response
    })


# =============================================================================
# Sentiment Analysis API
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_feedback(request):
    """
    Analyze course feedback sentiment
    
    POST /api/v1/ml/sentiment/
    Body: {"feedback": "The course was excellent and very helpful"}
    """
    from utils.ml.ml_services import SentimentAnalyzer
    
    feedback = request.data.get('feedback', '')
    
    if not feedback:
        return api_error('feedback required', status_code=400)
    
    analysis = SentimentAnalyzer.analyze_feedback(feedback)
    
    return api_response({
        'success': True,
        'analysis': analysis
    })


# =============================================================================
# Similarity API
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_similar_students(request, student_id):
    """
    Find similar students for study groups
    
    GET /api/v1/ml/similar-students/{student_id}/?n=5
    """
    from utils.ml.ml_services import StudentSimilarity
    
    n = request.query_params.get('n', 5)
    try:
        n = int(n)
    except ValueError:
        n = 5
    
    similar = StudentSimilarity.find_similar_students(student_id, n=n)
    
    return api_response({
        'success': True,
        'student_id': student_id,
        'similar_students': similar
    })


# =============================================================================
# Anomaly Detection API
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detect_anomaly(request, student_id):
    """
    Detect anomalous patterns
    
    GET /api/v1/ml/anomaly/{student_id}/?type=grade
    """
    from utils.ml.ml_services import AnomalyDetector
    
    anomaly_type = request.query_params.get('type', 'grade')
    
    if anomaly_type == 'grade':
        result = AnomalyDetector.detect_grade_anomaly(student_id)
    else:
        result = AnomalyDetector.detect_attendance_anomaly(student_id)
    
    return api_response({
        'success': True,
        'student_id': student_id,
        'type': anomaly_type,
        'result': result
    })


# =============================================================================
# Capacity Forecasting API
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def forecast_capacity(request, course_id):
    """
    Forecast course registration demand
    
    GET /api/v1/ml/forecast/{course_id}/?session=2024/2025
    """
    from utils.ml.ml_services import CapacityForecaster
    
    session_id = request.query_params.get('session')
    
    forecast = CapacityForecaster.predict_demand(course_id, session_id or '')
    
    return api_response({
        'success': True,
        'forecast': forecast
    })
EOF