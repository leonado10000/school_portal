from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField(default="model.school@gmail.com")

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Batch(models.Model):
    associate_school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    batch_id = models.CharField(max_length=20)  # e.g., 2024-25
    start_date = models.DateField(auto_now_add=True)
    current_class = models.IntegerField(default=1)
    status = models.CharField(max_length=10,choices=[('Active','Active'),('Inactive','Inactive')],default='None')

    def __str__(self):
        return self.batch_id
