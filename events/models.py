from io import open_code
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING

credit = 'credit'
debit = 'debit'
transaction_choice = [(credit,'Credit'),(debit,'Debit')]
# Create your models here.
class Events(models.Model):
    eventname = models.CharField(max_length=200)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    seat_avail = models.IntegerField()
    fees = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    joining_end_date = models.DateTimeField()
    joining_start_date = models.DateTimeField()
    queue_no = models.IntegerField(null=True ,blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.eventname



class EventsJoined(models.Model):
    username = models.ForeignKey(User,on_delete = models.CASCADE)
    events_joined = models.ForeignKey(Events,on_delete=models.CASCADE)
    joining_date = models.DateTimeField(auto_now_add=True)
    queue_no = models.IntegerField(null=True,blank=True, default=0)
    is_queued = models.BooleanField(default=False)


    def __str__(self) :
        return self.events_joined.eventname  

class UserWallet(models.Model):
    wallet_username = models.ForeignKey(User,on_delete = models.CASCADE)
    wallet_amount = models.DecimalField(max_digits=10,decimal_places=2,default=15000)

    def __str__(self) :
        return self.wallet_username.username  


class UserTransaction(models.Model):
    transaction_type = models.CharField(max_length=300,choices=transaction_choice)
    transaction_username = models.CharField(max_length=300)
    transaction_event_fees = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_event_name = models.ForeignKey(Events,on_delete=models.CASCADE)
    transaction_created_at = models.DateTimeField(auto_now_add=True)
    transaction_updated_At = models.DateTimeField(auto_now=True)
# id amt type user evebt created daste ypdated date
    def __str__(self) :
        return self.transaction_username     
