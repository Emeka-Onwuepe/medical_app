from django.db.models.signals import pre_delete,pre_save,post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from platforms.models import Api_Number
User=get_user_model()

@receiver(pre_save, sender=Api_Number)
def api_number_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_number = Api_Number.objects.get(pk=instance.pk).number
        if old_number != instance.number:
            users = User.objects.filter(api_number=old_number)
            for user in users:
                user.api_number = instance.number
                user.save()
                
@receiver(post_delete, sender=Api_Number)
def api_number_post_delete(sender, instance, **kwargs):
    print(instance.number)
    users = User.objects.filter(api_number=instance.number)
    # print(users)
    for user in users:
        print(user.api_number)
        user.api_number = ''
        user.save()

    
    
    