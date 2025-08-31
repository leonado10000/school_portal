# urls.py (add)
from django.urls import path
from . import views

urlpatterns = [
    # ... your existing urls ...
    path("reports/notebook/", views.notebook_report, name="notebook_report"),
]
