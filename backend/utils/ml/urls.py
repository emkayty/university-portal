"""ML Service URLs"""
from django.urls import path
from utils.ml.api import (
    predict_cgpa,
    dropout_risk,
    at_risk_students,
    recommend_courses,
    chatbot_message,
    analyze_feedback,
    find_similar_students,
    detect_anomaly,
    forecast_capacity
)

app_name = 'ml'

urlpatterns = [
    # CGPA Prediction
    path('predict-cgpa/', predict_cgpa, name='predict_cgpa'),
    
    # Dropout Risk
    path('dropout-risk/<uuid:student_id>/', dropout_risk, name='dropout_risk'),
    path('dropout-risk/', dropout_risk, name='dropout_risk_post'),
    path('at-risk-students/', at_risk_students, name='at_risk_students'),
    
    # Course Recommendation  
    path('recommend-courses/<uuid:student_id>/', recommend_courses, name='recommend_courses'),
    path('recommend-courses/', recommend_courses, name='recommend_courses_post'),
    
    # Chatbot
    path('chatbot/', chatbot_message, name='chatbot'),
    
    # Sentiment Analysis
    path('sentiment/', analyze_feedback, name='sentiment'),
    
    # Similarity
    path('similar-students/<uuid:student_id>/', find_similar_students, name='similar_students'),
    
    # Anomaly Detection
    path('anomaly/<uuid:student_id>/', detect_anomaly, name='anomaly'),
    
    # Capacity Forecasting
    path('forecast/<uuid:course_id>/', forecast_capacity, name='forecast'),
]