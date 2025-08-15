from django.db import models
from people.models import Teacher, Student
from core.models import Batch
class Marksheet(models.Model):
    marksheet_id = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    forclass = models.IntegerField()
    term = models.CharField(max_length=10,default="2025-26_1") # term-years _ term_number 

    def __str__(self):
        return f"class:{self.forclass}; term:{self.term};"

class Scorecard(models.Model):
    marksheet_id = models.ForeignKey(Marksheet, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    hindi_theory = models.IntegerField()
    hindi_assessment = models.IntegerField()
    english_theory = models.IntegerField()
    english_assessment = models.IntegerField()
    maths_theory = models.IntegerField()
    maths_assessment = models.IntegerField()
    science_theory = models.IntegerField()
    science_assessment = models.IntegerField()
    sst_evs_theory = models.IntegerField()
    sst_evs_assessment = models.IntegerField()
    drawing_theory = models.IntegerField(default=0)
    drawing_assessment = models.IntegerField(default=0)
    computer_music_theory = models.IntegerField(default=0)
    computer_music_assessment = models.IntegerField(default=0)
    gk_theory = models.IntegerField(default=0)
    gk_assessment = models.IntegerField(default=0)
    punjabi_skt_theory = models.IntegerField()
    punjabi_skt_assessment = models.IntegerField()

    def __str__(self):
        return f"Scorecard for {self.student.student_id}.{self.student.name} in {self.marksheet_id.forclass}"