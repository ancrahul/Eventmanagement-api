from collections import Counter
from .models import *
from django.db.models import Avg,Sum,Count,Max,Min
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from django.db.models.fields import DecimalField
from django.db.models.query_utils import Q
from django.db.models import Sum,Value,Count



def total_cash_manager(request):
    credit = UserTransaction.objects.filter(transaction_type = 'credit').aggregate(totalamt = Sum('transaction_event_fees'))
    debit = UserTransaction.objects.filter(transaction_type = 'debit').aggregate(totalamt = Sum('transaction_event_fees'))
    total = int(credit['totalamt'] - debit['totalamt'])
    return Response({"total cash":total}) 


def invested_most_money_manager(request):

    #get distinct user from UserTrasacction module 
    distinct_user = UserTransaction.objects.values('transaction_username').distinct()
    all_distinct_user_list = []
    for user in distinct_user:
        all_distinct_user_list.append(user['transaction_username'])   
    
    #creating list of dictionaries with distinct user and sum(credit money) - sum(debit money)
    user_spending_list = []
    for user in all_distinct_user_list :
        user_total_credited_amount = UserTransaction.objects.filter(transaction_username = user).values_list('transaction_event_fees',flat=True).aggregate(amt = Coalesce(Sum('transaction_event_fees',filter = Q(transaction_type='credit')),Value(0), output_field = DecimalField()) - Coalesce(Sum('transaction_event_fees',output_field = DecimalField(),filter= Q(transaction_type = 'debit')),Value(0), output_field = DecimalField()))
        user_spending_list.append({ user : user_total_credited_amount['amt']})

    # converting list of dictionaries(user_spending_list) to dictionaries
    user_spending_dictionary = {}
    for data in user_spending_list:
        user_spending_dictionary.update(data)

    most_spending_user = max(user_spending_dictionary.items(), key=lambda x: x[1])

    return Response({"invested most money user": most_spending_user[0] , "amount spend":most_spending_user[1]})


def created_most_event_manager(request):

    #get distinct user from Events module 
    distinct_user = Events.objects.values('creator__username').distinct()
    all_distinct_user_list = []
    for user in distinct_user:
        all_distinct_user_list.append(user['creator__username']) 

    #creating list of dictionaries with distinct user and event count
    user_and_event_count_list = []
    for user in all_distinct_user_list:
        events = Events.objects.filter(creator__username = user).values_list('creator__username',flat=True).aggregate(count = Count('id'))
        user_and_event_count_list.append({user:events['count']})

    # converting list of dictionaries(user_and_event_count_list) to dictionaries
    user_and_event_count_dictionary = {}
    for data in user_and_event_count_list:
        user_and_event_count_dictionary.update(data)

    #get user and count of user who created most event in tuple``
    most_event_count = max(user_and_event_count_dictionary.items(), key=lambda x: x[1])
    return Response({"user who created most event": most_event_count[0],"number of event created by user":most_event_count[1]})



def seat_status_manager(request):

    # initail seat  = total seat booked + seat left - queued_seat 
     
    
    # get all distinct event into a list
    distinct_event = Events.objects.values('id').distinct()
    all_distinct_event_list = []
    for event in distinct_event:
        all_distinct_event_list.append(event['id'])



    #get count of seat booked in each event into list of dictionaries
    each_event_total_seat_booked_list = []
    for event in all_distinct_event_list:
        total_seat_booked = BookEvent.objects.filter(events_joined__id = event).aggregate(count = Count('events_joined'))
        each_event_total_seat_booked_list.append({event:total_seat_booked['count']})

    # converting list of dictionaries(each_event_total_seat_booked_list) to dictionaries
    each_event_total_seat_booked_dictionary = {}
    for data in each_event_total_seat_booked_list:
        each_event_total_seat_booked_dictionary.update(data)




    #get count of seat left from Events model into list of dictionaries
    each_event_total_seat_left_list = []
    for event in all_distinct_event_list:
        total_seat_left = Events.objects.filter(id = event).values_list('seat_avail',flat=True).first()
        each_event_total_seat_left_list.append({event : total_seat_left})

    # converting list of dictionaries(each_event_total_seat_left_list) to dictionaries
    each_event_total_seat_left_dictionary = {}
    for data in each_event_total_seat_left_list:
        each_event_total_seat_left_dictionary.update(data)




    # get count of seat queued from BookEvent model into list of dictionaries
    each_event_total_seat_queued_list = []
    for event in all_distinct_event_list:
        total_seat_booked = BookEvent.objects.filter(is_queued = True,events_joined__id = event).aggregate(count = Count('events_joined'))
        each_event_total_seat_queued_list.append({event:total_seat_booked['count']})

    # converting list of dictionaries(each_event_total_seat_queued_list) to dictionaries
    each_event_total_seat_queued_dictionary = {}
    for data in each_event_total_seat_queued_list:
        each_event_total_seat_queued_dictionary.update(data)
    

    # creating counter of dictionaries for calculating initailseat

    each_event_total_seat_booked_dictionary_counter =  Counter(each_event_total_seat_booked_dictionary)
    each_event_total_seat_left_dictionary_counter = Counter(each_event_total_seat_left_dictionary)
    each_event_total_seat_queued_dictionary_counter = Counter(each_event_total_seat_queued_dictionary)
    each_Event_inital_seat_dictionary= dict(each_event_total_seat_booked_dictionary_counter + each_event_total_seat_left_dictionary_counter - each_event_total_seat_queued_dictionary_counter)



    
    each_event_seat_available_percentage = {}
    for key, value in each_Event_inital_seat_dictionary.items():
        if key in each_event_total_seat_booked_dictionary:
            if value <= each_event_total_seat_booked_dictionary[key]:
                each_event_seat_available_percentage.update({key:"All seat is booked"})
            if value > each_event_total_seat_booked_dictionary[key]:
                percentage = (each_event_total_seat_booked_dictionary[key]/value)*100
                each_event_seat_available_percentage.update({key:(f'{percentage}% booked')})
    
    return Response(each_event_seat_available_percentage)
                



