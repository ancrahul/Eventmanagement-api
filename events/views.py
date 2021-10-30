import json
from django.http import request
# Create your views here.
from rest_framework import viewsets
from rest_framework import response
from rest_framework.response import Response
from .serializers import EventSerializer, JoinEventSerializer
from .models import Events, EventsJoined
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import F

now = timezone.now()


class EventViewset(viewsets.ModelViewSet):
    queryset  = Events.objects.all()
    serializer_class = EventSerializer 
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data
        event_joining_start_date = data['joining_start_date']
        event_joining_end_date = data['joining_end_date']
        event_start_date =  data['start_date']
        event_end_date = data['end_date']
        no_seats = int(data['seat_avail'])

        # date validation and available seat should be more than 0
            
        if event_joining_start_date > event_joining_end_date:
            return Response({'detail':'Event joining start date must be greater than event joining end date'})
        if event_joining_end_date > event_start_date:
            return Response({'detail':'event joining end date should be greater than event start date'})
        if event_start_date > event_end_date:
            return Response({'detail':'event start date should be greater than event end date'})
        if no_seats < 1:
            return Response({'detail':'number of seats cannot be zero'})
        else:
            return super().create(request, *args, **kwargs)

    
    # user can delete only those event created by current user or supperuser(i.e:admin)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # instance = current event all object
        if request.user.id == instance.creator.id or request.user.is_superuser: # current user == current events creator id or current user must be supperuser
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'details': 'Cant delete event created by different user'})
    
    # user can update only those event created by current user
    def update(self, request, *args, **kwargs):
        instance = self.get_object() # instance = current event all object
        if request.user.id == instance.creator.id : #  current user == current events creator id
            return super().update(request, *args, **kwargs)
        else:
            raise ValueError



class JoinEventView(viewsets.ModelViewSet):
    queryset  = EventsJoined.objects.all()
    serializer_class = JoinEventSerializer 
    permission_classes = [IsAuthenticated]
    
    # user can join only those event which is currently between the joining start and joining end date.
    # if user has already joined the event then it will show already joined.
    def create(self, request, *args, **kwargs):
        data = request.data
        id = data['events_joined']
        obj = Events.objects.get(id = id)
        filtered = EventsJoined.objects.filter(username=request.user,events_joined=obj).exists()
        event_joining_start_date = getattr(obj, 'joining_start_date') 
        event_joining_end_date = getattr(obj, 'joining_end_date')
        
         
        if now > event_joining_start_date and now < event_joining_end_date and obj.seat_avail > 0:# can join event if current date is between join start and join end date and seat should be more than zero
            if not filtered:
                obj.seat_avail = F("seat_avail") - 1 # decreament in availabel seats in event models
                obj.save()
                return super().create(request, *args, **kwargs)
            else:
                return Response({'details': 'Event already exists'})
        else:
            return Response({'details':'cant join event now date already passed or not yet there or no seats avialable'})
        
        
    # user can only see those event which is joined by him/her but superuser(i.e: admin) can see all joined events
    def get_queryset(self):
        if self.request.user.is_superuser:# if currentuser is supper user(i.e: admin) than can see all events joined 
            return super().get_queryset()
        else:
            return EventsJoined.objects.filter(username_id = self.request.user.id)
    
    
    def destroy(self, request, *args, **kwargs):
        join_event = self.get_object()# retriving current joined_events data
        obj = Events.objects.get(id=join_event.events_joined.id) # obj = data of events having id of current eventjoined
        obj.seat_avail = F("seat_avail") + 1 # increment in availabel seats in event models in 
        obj.save()
        return super().destroy(request, *args, **kwargs)
