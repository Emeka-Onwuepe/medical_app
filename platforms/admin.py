from django.contrib import admin

from platforms.models import Whatsapp_Record, Whatsapp_Temp_Record

# Register your models here.
admin.site.register(Whatsapp_Record)
admin.site.register(Whatsapp_Temp_Record)
