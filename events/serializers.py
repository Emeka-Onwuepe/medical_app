from rest_framework import serializers
from .models import Event

class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # fields = '__all__'
        fields = ['id','condition','symptoms','notes','date','time',
                  'patient','medical_practitioner','status','mode',
                  'document','patient_name']
    
