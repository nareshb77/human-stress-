from django.db import models

# Create your models here.
class HumanStress(models.Model):
    snoring_rate=models.CharField(max_length=350)
    respiration_rate=models.CharField(max_length=350)
    blood_oxygen=models.CharField(max_length=350)
    body_temperature=models.CharField(max_length=350)
    limb_movement=models.CharField(max_length=350)
    eye_movement=models.CharField(max_length=350)
    sleeping_hours=models.CharField(max_length=350)
    heart_rate=models.CharField(max_length=350)
    stress_level=models.CharField(max_length=350)
