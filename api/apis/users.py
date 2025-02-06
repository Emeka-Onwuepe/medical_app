from django.utils import timezone
from api.helpers import generate_otp
from users.models import Medical_practitional_Meta_Data
from users.serializers import Get_User_Serializer, Patient_Serializer, User_Serializer, Login_Serializer
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import permissions,generics,status
from rest_framework.response import Response
from knox.models import AuthToken
# from twilio.rest import Client


class LoginUser(generics.GenericAPIView):
    serializer_class = Login_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        returnedUser = Get_User_Serializer(user)
        return Response({"user": returnedUser.data, "token": token})

class RegisterMPUser(generics.GenericAPIView):
    serializer_class = User_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _,token=AuthToken.objects.create(user)
        returnedUser=Get_User_Serializer(user)
        return Response({"user":returnedUser.data,
                         "token":token
                         })
        
        
# class PatientApi(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = Patient_Serializer
    
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         data = request.data['data']
#         action = request.data['action']
#         # del data['action']
#         data['medical_practitioner'] = user.id
        
#         if action == "create":
#             serializer = self.get_serializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             patient = serializer.save()
#             patient = self.get_serializer(patient)
#             return Response({'created':True,'id':patient})    


class OTPApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        otp = generate_otp()
        user = request.user
        if user.verified_number:
            return Response({"message": "Number already verified"}, status=status.HTTP_400_BAD_REQUEST)
       
        md_meta,created = Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=user)
        md_meta.otp = otp
        md_meta.otp_created = timezone.now()
        md_meta.save() 
        
        
        # Your Account SID from twilio.com/console
        # account_sid = 'your_account_sid'
        # # Your Auth Token from twilio.com/console
        # auth_token = 'your_auth_token'
        # client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     to=user.phone_number,  # Assuming user has a phone_number attribute
        #     from_="your_twilio_phone_number",
        #     body=f"Your OTP is {otp}"
        # )

        return Response({"message": "OTP sent successfully"})
        
    def post(self, request, *args, **kwargs):
        user = request.user
        otp = request.data['otp']
        md_meta = Medical_practitional_Meta_Data.objects.get(medical_practitioner=user)
        
        diff = timezone.now() - md_meta.otp_created
        if diff.seconds > 600:
            return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if md_meta.otp != int(otp):
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                md_meta.otp = 0
                md_meta.save()
                user.verified_number = True
                user.save()
                
        
        return Response({"message": "OTP authenticated"})
        
        