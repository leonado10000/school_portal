from django.urls import path
from . import views

urlpatterns = [
    path("students/new/", views.student_create, name="student_create"),
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
    path("students/<int:student_id>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:student_id>/delete/", views.student_delete, name="student_delete"),
    path("classes/", views.class_list, name="class_list"),
    path("classes/<int:batch_id>/students/", views.student_list_by_batch, name="student_list_by_batch"),
]
