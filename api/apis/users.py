from django.utils import timezone
from api.helpers import generate_otp
from users.forms import UserModelForm
from users.models import Medical_practitional_Meta_Data
from users.serializers import (Get_User_Serializer,User_Serializer, 
                               Login_Serializer,Edit_User_Serializer)
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import permissions,generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
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

class ManageMPUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = User_Serializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data['data']
        action = request.data['action']
        
        if action == 'update':
            serializer = self.get_serializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            returnedUser = Get_User_Serializer(user)
            return Response(returnedUser.data)
        elif action == 'delete':
            user.delete()
            return Response({"message": "User deleted"})


# @csrf_exempt 
# def EditUser(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = UserModelForm(data=request.POST, files=request.FILES)
#         print(form.is_valid())
#     return HttpResponse("EVENT_RECEIVED", status=200)
        
class EditUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Edit_User_Serializer
    # serializer_class = User_Serializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user 
        
        serializer = self.get_serializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # form = UserModelForm(data=request.data, files=request.FILES, instance=user)
        # if form.is_valid():
        #     form.save()
        _, token = AuthToken.objects.create(user)
        returnedUser = Get_User_Serializer(user)
        return Response({"user": returnedUser.data, "token": token})
        return Response({'message':'An error occurred'},status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePassword(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Edit_User_Serializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if  data['action'] == 'old_password':
            if not user.check_password(data['old_password']):
                return Response({"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'correct password'})
            
        if data['action'] == 'change_password':
            if not user.check_password(data['old_password']):
                return Response({"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(data['new_password'])
            user.save()
            AuthToken.objects.filter(user=user).delete()
            return Response({"message": "Password changed successfully"})
        
        if data['action'] == 'check_email':
            if User.objects.filter(email=data['email']).exists():
                return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # send email verification
                # Generate a password reset link
                reset_link = f"{settings.FRONTEND_URL}/reset-password?email={data['email']}"
                # Generate a deep link for the mobile app
                app_link = f"myapp://reset-password?email={data['email']}"
                # Send email
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link below to reset your password:\n{reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[data['email']],
                    fail_silently=False,
                )
            return Response({"message": "Email is available"})

class OTPApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
        
    def post(self, request, *args, **kwargs):
        user = request.user
        action= request.data['action']
        
        if action == 'get':
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
        
class Test_Email(generics.GenericAPIView):
        
    def get(self, request, *args, **kwargs):
        print("Sending test email...")
        # send email
        send_mail(
            subject="Test Email",
            message="This is a test email from the Django application.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["pascalemy2010@gmail.com"],
            fail_silently=False,
        )
        return Response({"message": "Test email sent successfully"})