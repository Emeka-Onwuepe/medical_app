
from platforms.models import Whatsapp_Record
from platforms.serializers import Whatsapp_Record_Serializer_init
from users.models import Patient
from users.serializers import Patient_Serializer,Patient_Serializer_init
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import permissions,generics
from rest_framework.response import Response


class PatientApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Patient_Serializer
    
    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     action = request.query_params['action']
        
    #     if action =='get_all_last':
    #         patients = Patient.objects.filter(medical_practitioner=user)
    #         last_messages = []
    #         for patient in patients:
    #             last_mgs = Whatsapp_Record.objects.filter(patient=patient.id).first()
    #             print(last_messages)
            
    #         patients = self.get_serializer(patients,many=True)
    #         return Response(patients.data)
    #     return Response({'error':True,'message':'Invalid action'})
    
    def post(self, request, *args, **kwargs):
        
        print(request.data)
        user = request.user
        data = request.data
        action = request.data['action']
        data['data']['medical_practitioner'] = user.id
        
        if action =='get_all':
            patients = Patient.objects.filter(medical_practitioner=user)
            patients = self.get_serializer(patients,many=True)
            return Response(patients.data)
        
        if action =='get_all_last':
            patients = Patient.objects.filter(medical_practitioner=user)
            last_messages = []
            for patient in patients:
                last_mgs = Whatsapp_Record.objects.filter(patient=patient.id).last()
                print(last_mgs)
                last_messages.append(last_mgs)
            
            patients = Patient_Serializer_init(patients,many=True)
            messages = Whatsapp_Record_Serializer_init(last_messages,many=True)
            
            data ={'patients':patients.data,'messages':messages.data}
            return Response(data)
        
        if action == 'get_by_id':
            patient = Patient.objects.get(id=data['id'])
            patient = self.get_serializer(patient)
            return Response(patient.data)
        
        if action == 'get_by_identifier':
            patient = Patient.objects.get(identifier=data['identifier'])
            patient = self.get_serializer(patient)
            return Response(patient.data)
        
        if action == "create":
            serializer = self.get_serializer(data=data['data'])
            serializer.is_valid(raise_exception=True)
            patient = serializer.save()
            patient = self.get_serializer(patient)
            return Response({'created':True,'id':patient})    
        elif action == "update":
            patient = Patient.objects.get(id=data['id'])
            serializer = self.get_serializer(patient,data=data['data'])
            serializer.is_valid(raise_exception=True)
            patient = serializer.save()
            # patient = self.get_serializer(patient)
            return Response({'updated':True,'id':patient.id})
        elif action == "delete":
            patient = Patient.objects.get(id=data['id'])
            patient.delete()
            return Response({'deleted':True})
        return Response({'error':True,'message':'Invalid action'})