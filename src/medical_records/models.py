from django.db import models


class MedicalRecord(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='medical_documents/', blank=True, null=True)
