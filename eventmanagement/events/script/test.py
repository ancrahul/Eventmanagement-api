from django.http import request
from events.models import Events
from django.http import request

def run():
    return request.user.get_username()

run()