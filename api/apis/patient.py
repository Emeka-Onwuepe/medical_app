
from users.models import Patient
from users.serializers import Patient_Serializer
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import permissions,generics
from rest_framework.response import Response


class PatientApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Patient_Serializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        action = request.data['action']
        data['data']['medical_practitioner'] = user.id
        
        if action =='get_all':
            patients = Patient.objects.filter(medical_practitioner=user)
            patients = self.get_serializer(patients,many=True)
            return Response(patients.data)
        
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