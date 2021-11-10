from django.urls import path,include
from rest_framework import routers
from events import transactionmanager
from . import views

router  = routers.DefaultRouter()
router.register(r'events',views.EventViewset)
router.register(r'booked',views.BookEventView)
router.register(r'usertransaction',views.UserTransactionView)
router.register(r'userwallet',views.UserWalletView)

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('totalcash/',views.total_cash),
    path('investedmostmoney/',views.invested_most_money),
    path('seatstatus/',views.seat_status),
    path('createdmostevent/',views.created_most_event),
    

    path('download',transactionmanager.export_excel)
]
