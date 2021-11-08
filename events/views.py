# Create your views here.
from rest_framework import viewsets
from rest_framework import response
from rest_framework.response import Response
from django.http import HttpResponse, request
from .serializers import EventSerializer, JoinEventSerializer, UserTransactionSerailizer, UserWalltetSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import F
import csv


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
        instance = self.get_object() # instance = current event all event_object
        if request.user.id == instance.creator.id or request.user.is_superuser: # current user == current events creator id or current user must be supperuser
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'details': 'Cant delete event created by different user'})
    
    # user can update only those event created by current user
    def update(self, request, *args, **kwargs):
        instance = self.get_object() # instance = current event all event_object
        if request.user.id == instance.creator.id : #  current user == current events creator id
            return super().update(request, *args, **kwargs)
        else:
            raise ValueError



class JoinEventView(viewsets.ModelViewSet):
    queryset  = EventsJoined.objects.all()
    serializer_class = JoinEventSerializer 
    permission_classes = [IsAuthenticated]



    def user_transaction(self,user,event_name,transaction_event_fees,transaction_type):
        UserTransaction.objects.create(
            transaction_username=user,
            transaction_event_name=event_name,
            transaction_event_fees=transaction_event_fees,
            transaction_type=transaction_type
        )


    # user can join only those event which is currently between the joining start and joining end date.
    # if user has already joined the event then it will show already joined.
    def create(self, request, *args, **kwargs):
        data = request.data
        id = data['events_joined'] # id of current event which we are joining
        event_obj = Events.objects.filter(id = id).first()# refrencing object of Events model with id
        filtered = EventsJoined.objects.filter(username=request.user,events_joined=event_obj).exists()#user with event if exist then true
        event_joining_start_date = getattr(event_obj, 'joining_start_date') 
        event_joining_end_date = getattr(event_obj, 'joining_end_date')
        user_wallet_obj , created= UserWallet.objects.get_or_create(wallet_username = request.user)
         
        if now > event_joining_start_date and now < event_joining_end_date: #and event_obj.seat_avail > 0:# can join event if current date is between join start and join end date and seat should be more than zero
            
            if event_obj.seat_avail > 0 :
                if not filtered: # if user exist with same event then go to else part
                    if user_wallet_obj.wallet_amount >= event_obj.fees:
                        user_wallet_obj.wallet_amount = F('wallet_amount') - event_obj.fees 
                        user_wallet_obj.save()
                        self.user_transaction(request.user,event_obj,event_obj.fees, debit)
                        event_obj.seat_avail = F("seat_avail") - 1 # decreament in availabel seats in event models if seat > 1
                        event_obj.save()
                        return super().create(request, *args, **kwargs)
                    else:
                        return Response({'details':'insufficient amount in wallet'})
                else:
                    return Response({'details': 'Event already exists'})
            
            elif event_obj.seat_avail < 1:
                if not filtered:
                    if user_wallet_obj.wallet_amount >= event_obj.fees:
                        user_wallet_obj.wallet_amount = F('wallet_amount') - event_obj.fees 
                        user_wallet_obj.save()
                        self.user_transaction(request.user,event_obj,event_obj.fees,debit)
                        event_obj.queue_no = F('queue_no') + 1 # increment the queue in events model if seat == 0
                        event_obj.save()
                        return super().create(request, *args, **kwargs)
                    else:
                        return Response({'details':'insufficient amount in wallet'})
                else:
                    return Response({'details': 'Event already exists'})
        else:
            return Response({'details':'cant join event now date already passed or not yet there or no seats avialable'})
        
    

    # user can only see those event which is joined by him/her but superuser(i.e: admin) can see all joined events
    def get_queryset(self):
        if self.request.user.is_superuser:# if currentuser is supper user(i.e: admin) than can see all events joined 
            return super().get_queryset()
        else:
            return EventsJoined.objects.filter(username_id = self.request.user.id)# will only see event created by hiim/her
    
    
    def destroy(self, request, *args, **kwargs):
        user_wallet_obj , created= UserWallet.objects.get_or_create(wallet_username = request.user)
        join_event = self.get_object()# retriving current joined_events data
        event_obj = Events.objects.get(id=join_event.events_joined.id)
        
        transaction_wallet_obj = UserTransaction.objects.filter(transaction_event_name = event_obj.id,transaction_username = request.user).first()
        # print(transaction_wallet_obj.transaction_event_fees)
        
        if not Events.objects.filter(queue_no = 0, seat_avail = 0).exists():
            event_obj.queue_no = F('queue_no') - 1 # decrement in queue_no in event model
            
        else:
            event_obj.seat_avail = F("seat_avail") + 1 # increment in seat_avail in event model

        user_wallet_obj.wallet_amount = F('wallet_amount') + transaction_wallet_obj.transaction_event_fees 
        user_wallet_obj.save()
        event_obj.save()
        self.user_transaction(request.user,event_obj,transaction_wallet_obj.transaction_event_fees, credit)
        return super().destroy(request, *args, **kwargs)


    def perform_destroy(self, instance):
        events = self.get_object()
    
         # update eventsjoined.queue_no with decrement having same event.eventname when current object is deleted 
        objs = EventsJoined.objects.filter(events_joined = events.events_joined).update(queue_no = F('queue_no') - 1)

         # update eventsjoined.is_queued to False where event name is same and queue_no = 0 
        objs1 = EventsJoined.objects.filter(events_joined = events.events_joined,queue_no = 0).update(is_queued = False)
        
        return super().perform_destroy(instance)
    
# function to download transaction data of current user    
def export_excel(request):
        response = HttpResponse(content_type="text/csv")
        response["content_Disposition"]= "attachement ; filename=transaction.csv"
        writer  = csv.writer(response)
        writer.writerow(['transaction_username','transaction_type','transaction_event_name','transaction_event_fees','transaction_created_at'])
        transactions = UserTransaction.objects.filter(transaction_username = request.user)
        for transaction in transactions:
            writer.writerow([transaction.transaction_username,
                            transaction.transaction_type,
                            transaction.transaction_event_name,
                            transaction.transaction_event_fees,
                            transaction.transaction_created_at,
                            ])
        return response

    
class UserTransactionView(viewsets.ModelViewSet):
    queryset  = UserTransaction.objects.all()
    serializer_class = UserTransactionSerailizer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        if self.request.user.is_superuser:# if currentuser is supper user(i.e: admin) than can see all transactions
            return super().get_queryset()
        else:
            return UserTransaction.objects.filter(transaction_username = self.request.user)# will only see own transactions


class UserWalletView(viewsets.ModelViewSet):
    queryset  = UserWallet.objects.all()
    serializer_class = UserWalltetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:# if currentuser is supper user(i.e: admin) than can see all user wallet
            return super().get_queryset()
        else:
            return UserTransaction.objects.filter(wallet_username = self.request.user)# will only see own wallet