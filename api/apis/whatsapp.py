from rest_framework import permissions,generics,status
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# class Whatsapp_Hooks(generics.GenericAPIView):
#     permission_classes = []

#     def get(self, request, *args, **kwargs):
#         VERIFY_TOKEN = '01948ea0-dc55-7b76-ae95-6bc44cc9f7e9'
#         mode = request.query_params['hub.mode']
#         challenge = request.query_params['hub.challenge']
#         verify_token = request.query_params['hub.verify_token']
       
#         if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
#             return Response(challenge)
              
#         return Response('hello world')
    
# @csrf_exempt 
# def Whatsapp_Hooks(request, *args, **kwargs):
#     if request.method == 'GET':
#         VERIFY_TOKEN = '01948ea0-dc55-7b76-ae95-6bc44cc9f7e9'
#         mode = request.GET['hub.mode']
#         challenge = request.GET['hub.challenge']
#         verify_token = request.GET['hub.verify_token']
       
#         if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
#             return Response(challenge,status=status.HTTP_200_OK)
              
        
        
        # Respond with a 200 OK status
    