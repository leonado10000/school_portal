from django.urls import path, include
from .views import nb_checking, list_checks, student_checks_detail, all_students

urlpatterns = [
    path('nb_checking/<str:check_id>', nb_checking, name='nb_checking'),
    path('list_checks', list_checks, name='list_checks'),
    path('student_checks_detail/<str:student_id>', student_checks_detail, name='student_checks_detail'),
    path('all_students', all_students, name='all_students')
]
