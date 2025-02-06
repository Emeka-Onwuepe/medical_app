from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from api.apis.users import LoginUser, OTPApi, RegisterMPUser
from api.apis.patient import PatientApi

# from api.apis.whatsapp import Whatsapp_Hooks

router = routers.DefaultRouter()

app_name="apis"


urlpatterns = [
    path('registermp', RegisterMPUser.as_view(), name="register"),
    path('login', LoginUser.as_view(), name="login"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('patient',PatientApi.as_view(),name='patient_view'),
    path('logoutall', KnoxView.LogoutAllView.as_view(), name="knox_logoutall"),
    path('otp', OTPApi.as_view(), name="otp"),       
]

urlpatterns += router.urls
# 3b4617c16e32e03dd533a92ceb0602630d78b20023959960980daaf9e2aa20a2
# {"data":{"full_name": "Odogwu Okeke",
#           "identifier":"12",
#           "whatsapp_number":"08037746313"},
# "action": "create"}