from rest_framework import serializers
from .models import Whatsapp_Record

class Whatsapp_Record_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Whatsapp_Record
        fields = '__all__'