from django.db import models

from users.models import Patient, User

# Create your models here.
status = (
                ("completed","completed"),
                ("pending","pending"),
                ("missed","missed"),
                ("cancelled","cancelled"),
                )

class Event(models.Model):
    """Model definition for Event."""

    # TODO: Define fields here
    title = models.CharField(verbose_name="title", max_length=150)
    description = models.CharField(verbose_name="description", max_length=255)
    time = models.DateTimeField(verbose_name="time", auto_now=False, auto_now_add=False)
    patient = models.ForeignKey(Patient, verbose_name="patient", 
                                on_delete=models.CASCADE,related_name='event_patient')
    medical_practitioner = models.ForeignKey(User, verbose_name="patient", 
                                on_delete=models.CASCADE,related_name='event_medical_practitioner')
    status = models.CharField(max_length=10, choices = status)
    

    class Meta:
        """Meta definition for Event."""

        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        """Unicode representation of Event."""
        return f"{self.time}--{self.medical_practitioner} -- {self.patient}"

