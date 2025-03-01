from django.contrib.auth import get_user_model
from events.serializers import Event_Serializer
User=get_user_model()
from rest_framework import permissions,generics,status
from rest_framework.response import Response
from events.models import Event

class EventApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Event_Serializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.get('data')
        action = request.data.get('action')
        print(action)
       
        # data['medical_practitioner'] = user.id
        
        if action =='get_all':
            events = Event.objects.filter(medical_practitioner=user)
            events = self.get_serializer(events,many=True)
            return Response(events.data)
        
        if action == 'get_by_id':
            event = Event.objects.get(id=data['id'])
            event = self.get_serializer(event)
            return Response(event.data)
        
        if action == "get_date_range":
            start_date = data['start_date']
            end_date = data['end_date']
            events = Event.objects.filter(medical_practitioner=user,time__range=[start_date,end_date])
            events = self.get_serializer(events,many=True)
            return Response(events.data)
        
        if action == 'set_status':
            event = Event.objects.get(id=data['id'])
            event.status = data['status']
            event.save()
            events = self.get_serializer(event)
            return Response(events.data)
            
        if not action and not request.data.get('id'):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            event = serializer.save()
            event = self.get_serializer(event)
            return Response({'created':True,'event':event.data})    
        elif  request.data.get('id'):
            data = request.data
            event = Event.objects.get(id=data['id'])
            serializer = self.get_serializer(event,data=data)
            serializer.is_valid(raise_exception=True)
            event = serializer.save()
            event = self.get_serializer(event)
            return Response({'updated':True,'event':event.data})
        elif action == "delete":
            event = Event.objects.get(id=data['id'])
            event.delete()
            return Response({'deleted':True})
        return Response({'error':True,'message':'Invalid action'})