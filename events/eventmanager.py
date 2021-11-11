from rest_framework.response import Response
from .models import *
from django.utils import timezone
from django.db.models import F



now = timezone.now()


def create_user_transaction(self,user,event_name,transaction_event_fees,transaction_type):
        UserTransaction.objects.create(
            transaction_username=user,
            transaction_event_name=event_name,
            transaction_event_fees=transaction_event_fees,
            transaction_type=transaction_type
        )

#######################################################################################################
# Event  

def event_date_validation(request):
    data = request.data
    eventname = data['eventname']
    event_joining_start_date = data['joining_start_date']
    event_joining_end_date = data['joining_end_date']
    event_start_date =  data['start_date']
    event_end_date = data['end_date']
    no_seats = int(data['seat_avail'])


    # date validation and available seat should be more than 0
    if event_joining_start_date > event_joining_end_date:
        return 'Event joining start date must be greater than event joining end date'
    if event_joining_end_date > event_start_date:
        return 'event joining end date should be greater than event start date'
    if event_start_date > event_end_date:
        return 'event start date should be greater than event end date'
    if no_seats < 1:
        return 'number of seats cannot be zero'
    else:
        return None


def delete_event(self,request):
    instance = self.get_object()
    if request.user.id == instance.creator.id or request.user.id == request.user.is_superuser:
        return None
    else:
        return "User doesn't have permission to delete this event"


def update_event(self,request):
    instance  = self.get_object()
    if request.user.id == instance.creator.id:
        return None
    else:
        return "User doesn't have permission to Update this event"


#######################################################################################################

# BookEvent


# user can join only those event which is currently between the joining start and joining end date.
# if user has already joined the event then it will show already joined.
def book_event(self,request):
    data = request.data
    id = data['events_joined'] # id of current event which we are joining
    event_obj = Events.objects.filter(id = id).first()# refrencing object of Events model with id
    filtered = BookEvent.objects.filter(username=request.user,events_joined=event_obj).exists()#user with event if exist then true
    event_joining_start_date = getattr(event_obj, 'joining_start_date') 
    event_joining_end_date = getattr(event_obj, 'joining_end_date')
    user_wallet_obj , created= UserWallet.objects.get_or_create(wallet_username = request.user)
        
    if now > event_joining_start_date and now < event_joining_end_date: #and event_obj.seat_avail > 0:# can join event if current date is between join start and join end date and seat should be more than zero
        
        if event_obj.seat_avail > 0 :
            if not filtered: # if user exist with same event then go to else part
                if user_wallet_obj.wallet_amount >= event_obj.fees:
                    user_wallet_obj.wallet_amount = F('wallet_amount') - event_obj.fees 
                    user_wallet_obj.save()
                    create_user_transaction(self,request.user,event_obj,event_obj.fees, debit)
                    event_obj.seat_avail = F("seat_avail") - 1 # decreament in availabel seats in event models if seat > 1
                    event_obj.save()
                    return None
                else:
                    return 'insufficient amount in wallet'
            else:
                return  'Event already exists'
        
        elif event_obj.seat_avail < 1:
            if not filtered:
                if user_wallet_obj.wallet_amount >= event_obj.fees:
                    user_wallet_obj.wallet_amount = F('wallet_amount') - event_obj.fees 
                    user_wallet_obj.save()
                    create_user_transaction(self,request.user,event_obj,event_obj.fees,debit)
                    event_obj.queue_no = F('queue_no') + 1 # increment the queue in events model if seat == 0
                    event_obj.save()
                    return None
                else:
                    return 'insufficient amount in wallet'
            else:
                return 'Event already exists'
    else:
        return 'cant join event now date already passed or not yet there or no seats avialable'
    

def delete_booked_event(self,request):
    user_wallet_obj , created= UserWallet.objects.get_or_create(wallet_username = request.user)
    join_event = self.get_object()# retriving current joined_events data
    event_obj = Events.objects.get(id=join_event.events_joined.id)
    
    # filter out  data if the current user and current event is present in trasaction model
    transaction_wallet_obj = UserTransaction.objects.filter(transaction_event_name = event_obj.id,transaction_username = request.user).first()
    
    if Events.objects.filter(queue_no = 0, seat_avail = 0).exists():
        event_obj.seat_avail = F('seat_avail') + 1 # decrement in queue_no in event model
        event_obj.queue_no = 0
    if Events.objects.filter(queue_no = 0, seat_avail__gt = 0).exists():
        event_obj.seat_avail = F("seat_avail") + 1 # increment in seat_avail in event model
        event_obj.queue_no = 0
    if Events.objects.filter(queue_no__gt = 0, seat_avail = 0).exists(): 
        event_obj.queue_no = F("queue_no") - 1 # increment in seat_avail in event model
        event_obj.seat_avail = 0


    # add amount to user wallet by reffering to transaction model
    user_wallet_obj.wallet_amount = F('wallet_amount') + transaction_wallet_obj.transaction_event_fees 
    user_wallet_obj.save()
    event_obj.save()
    create_user_transaction(self,request.user,event_obj,transaction_wallet_obj.transaction_event_fees, credit)
    
    events = self.get_object() # instance of current event

    BookEvent.objects.filter(events_joined = events.events_joined).update(queue_no = F('queue_no') - 1)
    # update BookEvent.is_queued to False where event name is same and queue_no = 0 
    BookEvent.objects.filter(events_joined = events.events_joined,queue_no = 0).update(is_queued = False)
    # if queue_no will less than 0 then it will be updated to zero 
    BookEvent.objects.filter(queue_no__lt = 0).update(queue_no = 0)
