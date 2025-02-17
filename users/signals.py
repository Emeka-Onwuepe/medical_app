from django.db.models.signals import post_save,post_delete,pre_delete
from django.contrib.auth import get_user_model
User=get_user_model()
from django.dispatch import receiver
from .models import Medical_practitional_Meta_Data, Patient

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'medical_practitioner':
        Medical_practitional_Meta_Data.objects.create(medical_practitioner=instance)
    elif instance.user_type == 'medical_practitioner':
        Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=instance) 
        

@receiver(post_save, sender=Patient)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.medical_practitioner_id)
        user.patient_count += 1
        user.save()


@receiver(pre_delete, sender=Patient)
def create_patient_profile(sender, instance, **kwargs):
    user = User.objects.get(pk=instance.medical_practitioner_id)
    user.patient_count -= 1
    user.save()
