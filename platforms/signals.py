from django.db.models.signals import pre_delete,pre_save,post_delete,post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from platforms.helpers import get_whatsapp_api_files
from platforms.models import Api_Number, Whatsapp_Record
from django.core.files.base import ContentFile
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

@receiver(post_save, sender=Whatsapp_Record)
def whatsapp_record_post_save(sender, instance, created, **kwargs):
    if not created:
        # If the record is being updated, we don't need to do anything
        return
    file_id = None
    content = None
    record_format = None
    if instance.record_type != 'text':
        file_id = instance.content
        record_format = instance.record_format
        content = get_whatsapp_api_files(file_id)
        if not content:
            file_id = None
            content = None
            record_format = None
            return
        
    # Save the file based on the record type
    if instance.record_type == 'image':
        instance.image.save(f"{file_id}.{record_format}", ContentFile(content))
        instance.save()

    elif instance.record_type == 'audio':
        if record_format == 'ogg; codecs=opus':
            record_format = 'ogg'
        instance.audio.save(f"{file_id}.{record_format}", ContentFile(content))
        instance.save()
    elif instance.record_type == 'video':
        instance.video.save(f"{file_id}.{record_format}", ContentFile(content))
        instance.save()

@receiver(post_delete, sender=Whatsapp_Record)
def delete_whatsapp_record_files(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.audio:
        instance.audio.delete(save=False)
    if instance.video:
        instance.video.delete(save=False)

@receiver(pre_save, sender=Whatsapp_Record)
def delete_whatsapp_record_files_copies(sender, instance, *args, **kwargs):
    if instance.pk:
        record = Whatsapp_Record.objects.get(pk=instance.pk)
        if record.image != instance.image:
            record.image.delete(False)
        if record.audio != instance.audio:
            record.audio.delete(False)
        if record.video != instance.video:
            record.video.delete(False)
