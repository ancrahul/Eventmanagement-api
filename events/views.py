# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import EventSerializer, BookEventSerializer, UserTransactionSerailizer, UserWalltetSerializer
from .models import *
from rest_framework.permissions import IsAuthenticated
from .eventmanager import *
from .transactionmanager import *
from rest_framework.decorators import api_view
from .manager import *

class EventViewset(viewsets.ModelViewSet):
    queryset  = Events.objects.all()
    serializer_class = EventSerializer 
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if event_date_validation(request) == None:
            return super().create(request, *args, **kwargs)
        else:
            return  Response(event_date_validation(request))
    
    # user can delete only those event created by current user or supperuser(i.e:admin)
    def destroy(self, request, *args, **kwargs):
        if delete_event(self,request) == None:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(delete_event(self,request))
    

    # user can update only those event created by current user
    def update(self, request, *args, **kwargs):
        if update_event(self,request) == None:
            return super().update(request, *args, **kwargs)
        else:
            return Response(update_event(self,request))



class BookEventView(viewsets.ModelViewSet):
    queryset  = BookEvent.objects.all()
    serializer_class = BookEventSerializer 
    permission_classes = [IsAuthenticated]


    #BookEvent / Joining an event
    def create(self, request, *args, **kwargs):
        if book_event(self,request) != None:
            return Response(book_event(self,request))
        else:
            return super().create(request, *args, **kwargs)
        
    

    # user can only see those event which is joined by him/her but superuser(i.e: admin) can see all joined events
    def get_queryset(self):
        if self.request.user.is_superuser:# if currentuser is supper user(i.e: admin) than can see all events joined 
            return super().get_queryset()
        else:
            return BookEvent.objects.filter(username_id = self.request.user.id)# will only see event created by hiim/her
    
    # delete an event
    def destroy(self, request, *args, **kwargs):
        delete_booked_event(self,request)
        return super().destroy(request, *args, **kwargs)


    
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



        
@api_view(http_method_names=['GET'])
def total_cash(request):
    return total_cash_manager(request )   


@api_view(http_method_names=['GET'])
def invested_most_money(request):
    return invested_most_money_manager(request)
    

@api_view(http_method_names=['GET'])
def seat_status(request):
    return seat_status_manager(request)


@api_view(http_method_names=['GET'])
def created_most_event(request):
    return created_most_event_manager(request)
