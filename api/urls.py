from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from api.apis.events import EventApi
from api.apis.users import ChangePassword, LoginUser, ManageMPUser, OTPApi, RegisterMPUser,EditUser, Test_Email, forgotPassword, resetPasswordAppLink, serve_assetlinks
from api.apis.patient import PatientApi
from api.apis.whatsapp import Whatsapp_Record_Api

# from api.apis.whatsapp import Whatsapp_Hooks

router = routers.DefaultRouter()

app_name="apis"
 

urlpatterns = [
    # users apis
    path('registermp', RegisterMPUser.as_view(), name="register"),
    path('managemp',ManageMPUser.as_view(),name='managemp_view'),
    path('edituser',EditUser.as_view(),name='editUser'),
    path('changepassword',ChangePassword.as_view(),name='change_password'),
    path('forgotpassword',forgotPassword.as_view(),name='forgot_password'),
    path('resetPassword',resetPasswordAppLink,name='reset_password'),
    path('.well-known/assetlinks.json', serve_assetlinks, name='serve_assetlinks'),

    # path('edituser',EditUser,name='editUser'),
    path('login', LoginUser.as_view(), name="login"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('logoutall', KnoxView.LogoutAllView.as_view(), name="knox_logoutall"),
    path('otp', OTPApi.as_view(), name="otp"), 
    # patients api
    path('patient',PatientApi.as_view(),name='patient_view'),
    # Events api
    path('event',EventApi.as_view(),name='event_view'),
    # whatsapp_record api
    path('whatsapp_records',Whatsapp_Record_Api.as_view(),name='whatsapp_records_view'),
    path('textemail',Test_Email.as_view(),name='test_email_view'),
    
]

urlpatterns += router.urls
# 3b4617c16e32e03dd533a92ceb0602630d78b20023959960980daaf9e2aa20a2
# {"data":{"full_name": "Odogwu Okeke",
#           "identifier":"12",
#           "whatsapp_number":"08037746313"},
# "action": "create"}