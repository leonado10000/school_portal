from django.db import models

# Create your models here.
from django.db import models
from core.models import School, Batch

class Classroom(models.Model):
    name = models.CharField(max_length=20)  # 10A, 12C
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.batch}"
