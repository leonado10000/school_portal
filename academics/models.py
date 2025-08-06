from django.db import models
from core.models import School, Batch
from people.models import Student, Teacher

class ResultReport(models.Model):
    report_id = models.CharField(max_length=20, unique=True)
    session = models.CharField(max_length=7)
    report_class = models.IntegerField()
    teacher_incharge = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='report_teacher', null=True, blank=True)

class ReportCard(models.Model):
    report_id = models.ForeignKey(ResultReport, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    