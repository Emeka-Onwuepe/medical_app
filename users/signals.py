from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
User=get_user_model()
from django.dispatch import receiver
from .models import Medical_practitional_Meta_Data

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'medical_practitioner':
        Medical_practitional_Meta_Data.objects.create(medical_practitioner=instance)
    elif instance.user_type == 'medical_practitioner':
        Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=instance) 
        
