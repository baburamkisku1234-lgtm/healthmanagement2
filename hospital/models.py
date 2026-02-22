# hospital/models.py
from django.db import models

class Patient(models.Model):
    health_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20)
    language = models.CharField(max_length=50, blank=True)
    # add other fields as needed

    def __str__(self):
        return self.health_id
    

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    doctor = models.CharField(max_length=100)

    def __str__(self):
        return f"Record for {self.patient} on {self.date}"
