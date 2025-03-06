from django.db.models.signals import post_save,post_delete,pre_delete
from django.contrib.auth import get_user_model
from platforms.models import Api_Number
User=get_user_model()
from django.dispatch import receiver
from .models import Medical_practitional_Meta_Data, Patient
from django.utils import timezone

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
            
    if instance.user_type == 'medical_practitioner':
        # medi = Medical_practitional_Meta_Data.objects.create(medical_practitioner=instance)
        medi,created = Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=instance)
        if created:
            medi.last_opened = timezone.now()
            medi.save()
        
    if not instance.api_number:
        api_numbers = Api_Number.objects.filter(in_use=True)
        if api_numbers:
            selected = api_numbers.last()
            instance.api_number = selected.number
            selected.count += 1
            selected.save()
            instance.save()
    # elif instance.user_type == 'medical_practitioner':
    #     medi,_ = Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=instance)
    #     medi.last_opened = timezone.now() 
    #     medi.save()
        
               
@receiver(post_save, sender=Patient)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.medical_practitioner_id)
        user.patient_count += 1
        if instance.gender == 'female':
            user.female_count += 1
        else:
            user.male_count += 1
        user.save()


@receiver(pre_delete, sender=Patient)
def create_patient_profile(sender, instance, **kwargs):
    user = User.objects.get(pk=instance.medical_practitioner_id)
    user.patient_count -= 1
    if instance.gender == 'female':
        user.female_count -= 1
    else:
        user.male_count -= 1
    user.save()
