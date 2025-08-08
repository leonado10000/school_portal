from django.db import models
from people.models import Teacher, Student
from core.models import Batch
class Marksheet(models.Model):
    marksheet_id = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    forclass = models.IntegerField()

class Scorecard(models.Model):
    marksheet_id = models.ForeignKey(Marksheet, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.IntegerField()

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
    drawing_theory = models.IntegerField()
    drawing_assessment = models.IntegerField()
    computer_music_theory = models.IntegerField()
    computer_music_assessment = models.IntegerField()
    gk_theory = models.IntegerField()
    gk_assessment = models.IntegerField()
    punjabi_skt_theory = models.IntegerField()
    punjabi_skt_assessment = models.IntegerField()
