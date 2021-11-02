from io import open_code
from django.db import models
from django.contrib.auth.models import User

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