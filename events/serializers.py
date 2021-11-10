from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

# to get only the username from the User model 
class CreatorDetails(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# show all event field and sets creator as current user if condition is true
class EventSerializer(serializers.ModelSerializer):

    creator = CreatorDetails(read_only=True)
    queue_no = serializers.IntegerField(read_only = True)

    # create the event and adding the creator detail in event model
    def create(self, validated_data):
        user = self.context['request'].user #current user 
        if 'superuser' in user.groups.values_list('name',flat=True) or user.is_superuser: # if current user group list contain superuser or current user is super user then it will add creator as the current user and then create an event 
            validated_data['creator'] = user # appending current user detail in model Events.creator
            return super().create(validated_data) 
        else:
            error = {'detail':'current user does not have permission to create event'}
            raise serializers.ValidationError(error)# raising custom error if user doesnt have permission
 
    class Meta:
        model = Events
        fields ='__all__'    




#show all BookEvent field and add username as current username d
class BookEventSerializer(serializers.ModelSerializer):
    
    username = CreatorDetails(read_only=True)
    queue_no = serializers.IntegerField(read_only = True)
    is_queued = serializers.BooleanField(read_only=True)


    # Book an event in Eventssjoined model and adding username detail in BookEvent model
    def create(self, validated_data):
        data = self.data
        id = data['events_joined']
        event_obj = Events.objects.get(id = id)
        user = self.context['request'].user # get current user detail
        validated_data['username'] = user # appending current user in mode BookEvent.username

        # sets BookEvent.queue_no to event.queue_no and BookEvent.is_queued to True if events.seat_Avail<1 and event.queue_no>=1
        if event_obj.seat_avail < 1 and event_obj.queue_no >= 1:
            validated_data['queue_no'] = event_obj.queue_no
            validated_data['is_queued'] = True
        return super().create(validated_data)   
        
    class Meta: 
        model = BookEvent
        fields = '__all__'



class UserTransactionSerailizer(serializers.ModelSerializer):
    class Meta: 
        model = UserTransaction
        fields = '__all__'



class UserWalltetSerializer(serializers.ModelSerializer):
    wallet_username = serializers.CharField(read_only = True)
    wallet_amount = serializers.DecimalField(max_digits=10,decimal_places=2,read_only = True)
    class Meta:     
        model = UserWallet
        fields = '__all__'


