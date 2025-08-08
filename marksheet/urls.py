from django.urls import path
from .views import marksheet_view, all_current_terms, student_scorecard

urlpatterns = [
    path('terms', all_current_terms, name='all_current_terms'),
    path('marksheet_view', marksheet_view, name='marksheet_view'),
    path('student/<str:student_id>', student_scorecard, name="student_scorecard")
]