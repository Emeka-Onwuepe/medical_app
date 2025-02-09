from rest_framework import permissions,generics,status
from rest_framework.response import Response
from platforms.models import Whatsapp_Record
from platforms.serializers import Whatsapp_Record_Serializer

class Whatsapp_Record_Api(generics.GenericAPIView):

        permission_classes = [permissions.IsAuthenticated]
        permission_classes = []
        serializer_class = Whatsapp_Record_Serializer
        
        def get(self,request,*args,**kwargs):
                records = Whatsapp_Record.objects.first()
                # records = Whatsapp_Record.objects.filter(record_type ='text')
                print(records)
                # return Response('hello word')
                records = self.get_serializer(records,many=True)
                return Response(records.data)
        
        def post(self, request, *args, **kwargs):
                user = request.user
                data = request.data['data']
                action = request.data['action']
                data['medical_practitioner'] = user.id
                
                if action == 'get_patient_records':
                    records = Whatsapp_Record.objects.filter(patient=int(data['patient_id']))
                    records = self.get_serializer(records,many=True)
                    return Response(records.data)
                
                if action == 'delete':
                    record = Whatsapp_Record.objects.get(id=int(data['id']))
                    record.delete()
                    return Response({'deleted':True})
                
                return Response({'error':True,'message':'Invalid action'})      
            
                
                
                
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
    