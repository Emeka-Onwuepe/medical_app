from django.contrib import admin
from django.urls import path,include

from platforms.views import Whatsapp_Hooks,send_whatsapp_message

app_name="platform"
urlpatterns = [
    path('hooks123',Whatsapp_Hooks,name='template'),
    path('send/<str:message>',send_whatsapp_message,name='template')
    
    ] 