from django.contrib import admin
from .models import *
# Register your models here.
    

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('creator',)


# registering models here
admin.site.register(Events,EventAdmin)
admin.site.register(BookEvent)
admin.site.register(UserWallet)
admin.site.register(UserTransaction)