from django.urls import path, include
from .views import checks_index, nb_checking, list_checks, student_checks_detail, all_students

urlpatterns = [
    path('nb_checking/<str:check_id>', nb_checking, name='nb_checking'),
    path('list_checks/<str:batch_id>', list_checks, name='list_checks'),
    path('checks_index', checks_index, name='checks_index'),
    path('student_checks_detail/<str:student_id>', student_checks_detail, name='student_checks_detail'),
    path('all_students', all_students, name='all_students')
]
