from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.


# @admin.action(description='Join Event')
# class JoinEvent():
#     def join_event(modeladmin, request, queryset):
#         queryset.update()
#         request.user     
    

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('creator',)
    # actions = [JoinEvent.join_event]

    # def save_model(self, request, obj, form, change):
    #     obj.creator = request.user
    #     obj.creator_id = request.user.id
    #     obj.last_modified_by = request.user
    #     obj.save()
    #     super().save_model(request, obj, form, change)


# registering models here
admin.site.register(Events,EventAdmin)
admin.site.register(EventsJoined)
admin.site.register(UserWallet)
admin.site.register(UserTransaction)