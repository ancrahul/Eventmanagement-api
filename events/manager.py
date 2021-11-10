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
        events = Events.objects.filter(creator__username = user).values_list('creator__username',flat=True).aggregate(count = Count('eventname'))
        user_and_event_count_list.append({user:events['count']})

    # converting list of dictionaries(user_and_event_count_list) to dictionaries
    user_and_event_count_dictionary = {}
    for data in user_and_event_count_list:
        user_and_event_count_dictionary.update(data)

    #get user and count of user who created most event in tuple``
    most_event_count = max(user_and_event_count_dictionary.items(), key=lambda x: x[1])

    return Response({"user who created most event": most_event_count[0],"number of event created by user":most_event_count[1]})



def seat_status_manager(request):
    pass