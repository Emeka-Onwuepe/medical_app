from django.db import models
from users.models import Patient, User
from django.core.validators import FileExtensionValidator

# Create your models here.

context_options = (
                ("medical_practitioner","medical_practitioner"),
                ("patient","patient"),
                )

record_types = (
                ("video","video"),
                ("audio","audio"),
                ("image","image"),
                ("text","text"),
                )
class Whatsapp_Record(models.Model):
    """Model definition for Whatsapp_Record."""

    # TODO: Define fields here
    medical_practitioner = models.ForeignKey(User, verbose_name="medical_practitioner",
                                             on_delete=models.CASCADE, related_name='whatsapp_medical_practitioner')
    patient = models.ForeignKey(Patient, verbose_name="patient",
                                             on_delete=models.CASCADE, related_name='whatsapp_patient')
    context = models.CharField(max_length=20, choices = context_options)
    record_type = models.CharField(max_length=8, choices = record_types)
    video = models.FileField(verbose_name="video",upload_to = 'videos/',validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    audio = models.FileField(verbose_name="audio",upload_to = 'audios/',validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    image = models.ImageField(verbose_name='image', upload_to='audios/', null=True,blank=True
                            #   height_field=None, width_field=None, max_length=None
                            )
    text = models.TextField(verbose_name='text',null=True,blank=True)
    timestamp = models.DateTimeField(verbose_name="timestamp", auto_now=False, auto_now_add=False)
    date_recorded = models.DateTimeField(verbose_name="recorded", auto_now=False, auto_now_add=True)
    

    class Meta:
        """Meta definition for Whatsapp_Record."""

        verbose_name = 'Whatsapp_Record'
        verbose_name_plural = 'Whatsapp_Records'
        ordering = ['timestamp']

    def __str__(self):
        """Unicode representation of Whatsapp_Record."""
        return f"{self.timestamp}--{self.medical_practitioner} -- {self.patient}"

