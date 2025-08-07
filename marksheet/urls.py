from django.urls import path
from .views import marksheet_view

urlpatterns = [
    path('', marksheet_view, name='marksheet'),
]