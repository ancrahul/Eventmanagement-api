from copy import error
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.response import Response
from .models import Events, EventsJoined
from django.contrib.auth.models import User

# to get only the username from the User model 
class CreatorDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# show all event field and sets creator as current user if condition is true
class EventSerializer(serializers.ModelSerializer):

    creator = CreatorDetails(read_only=True)

    # create the event and adding the creator detail in event model
    def create(self, validated_data):
        user = self.context['request'].user #current user 
        if 'superuser' in user.groups.values_list('name',flat=True) or user.is_superuser: # if current user group list contain superuser or current user is super user then it will add creator as the current user and then create an event 
            validated_data['creator'] = user # appending current user detail in model Events.creator
            return super().create(validated_data) 
        else:
            error = {'detail':'current user does not have permission to create event'}
            raise serializers.ValidationError(error)   
 
    class Meta:
        model = Events
        fields ='__all__'    



#show all Eventsjoined field and add username as current username d
class JoinEventSerializer(serializers.ModelSerializer):
    
    username = CreatorDetails(read_only=True)

    # joining an event in Eventssjoined model and adding username detail in eventsjoined model
    def create(self, validated_data):
        user = self.context['request'].user # get current user detail
        validated_data['username'] = user # appending current user in mode Eventsjoined.username 
        return super().create(validated_data) 
        
    class Meta: 
        model = EventsJoined
        fields = '__all__'