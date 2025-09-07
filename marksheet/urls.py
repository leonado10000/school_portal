from django.urls import path
from .views import marksheet_view, all_current_terms, scorecard_pdf_download, student_scorecard

urlpatterns = [
    path('terms', all_current_terms, name='all_current_terms'),
    path('marksheet_view/<str:sheet_id>', marksheet_view, name='marksheet_view'),
    path('student/<str:student_id>', student_scorecard, name="student_scorecard"),
    path('download/<str:student_id>', scorecard_pdf_download, name="scorecard_download"),
]