from django.http import HttpResponse
from .models import *
import csv


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