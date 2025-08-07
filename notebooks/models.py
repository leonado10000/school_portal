from django.db import models

# Create your models here.
from django.db import models
from people.models import Student, Teacher
from core.models import Batch, Subject

class SubmissionRecord(models.Model):
    submission_id = models.CharField(max_length=50)
    associated_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)
    associated_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default="sub_1")
    subject_context = models.CharField(max_length=100,blank=True, null=True)
    associated_batch = models.ForeignKey(Batch, on_delete=models.CASCADE, default="batch_1")    
    add_date = models.DateField(auto_now_add=True)

class NotebookSubmission(models.Model):
    submission_id = models.ForeignKey(SubmissionRecord, on_delete=models.CASCADE, default="sub_1")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    checked_date = models.DateField(null=True, blank=True)
    incomplete_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.checked_date if self.checked_date else None}"
