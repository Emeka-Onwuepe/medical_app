from rest_framework import routers
from django.urls import path
from knox import views as KnoxView
router = routers.DefaultRouter()

app_name="apis"


urlpatterns = [
    # path('register', RegisterUser.as_view(), name="register"),
    
           
]

urlpatterns += router.urls