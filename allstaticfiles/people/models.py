from django.db import models

# Create your models here.
from django.db import models
from core.models import School, Batch
from academics.models import Classroom

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    roll_number = models.IntegerField()
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, default=1)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
