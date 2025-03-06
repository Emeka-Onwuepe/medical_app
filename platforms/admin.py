from django.contrib import admin

from platforms.models import Api_Number, Whatsapp_Record, Whatsapp_Temp_Record

# Register your models here.
admin.site.register(Whatsapp_Record)
admin.site.register(Whatsapp_Temp_Record)
admin.site.register(Api_Number)
