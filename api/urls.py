from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

# from api.apis.whatsapp import Whatsapp_Hooks

router = routers.DefaultRouter()

app_name="apis"


urlpatterns = [
    # path('hooks123', Whatsapp_Hooks.as_view(), name="hooks"),
    # path('hooks123', Whatsapp_Hooks, name="hooks"),
           
]

urlpatterns += router.urls