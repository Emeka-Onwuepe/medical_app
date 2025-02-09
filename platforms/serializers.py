from rest_framework import serializers
from .models import Whatsapp_Record

class Whatsapp_Record_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Whatsapp_Record
        fields = ('id','patient','context','record_id','record_type',
                  'record_format','content','timestamp',
                  'date_recorded','get_absolute_url')