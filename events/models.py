from django.db import models

from users.models import Patient, User

# Create your models here.
status = (
                ("completed","completed"),
                ("pending","pending"),
                ("missed","missed"),
                ("cancelled","cancelled"),
                )
mode = (('online','online'),
        ('offline','offline'))


class Event(models.Model):
    """Model definition for Event."""

    # TODO: Define fields here
    condition = models.CharField(verbose_name="condition", max_length=250,null=True,blank=True)
    symptoms = models.CharField(verbose_name="symptoms", max_length=250,null=True,blank=True)
    notes = models.CharField(verbose_name="notes", max_length=255,null=True,blank=True)
    date  = models.DateField(verbose_name="date",auto_now=False, auto_now_add=False)
    time = models.TimeField(verbose_name='time', auto_now=False, auto_now_add=False)
    patient = models.ForeignKey(Patient, verbose_name="patient", 
                                on_delete=models.CASCADE,related_name='event_patient')
    medical_practitioner = models.ForeignKey(User, verbose_name="patient", 
                                on_delete=models.CASCADE,related_name='event_medical_practitioner')
    status = models.CharField(max_length=10, choices = status,default='pending')
    mode = models.CharField(max_length=10, choices = mode,default='offline')
    document = models.FileField(verbose_name='document', upload_to='patient_documents/',
                                null=True,blank=True)
    

    class Meta:
        """Meta definition for Event."""

        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']

    def __str__(self):
        """Unicode representation of Event."""
        return f"{self.time}--{self.medical_practitioner} -- {self.patient}"
    
    def patient_name(self):
        return self.patient.full_name

