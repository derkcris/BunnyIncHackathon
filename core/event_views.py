from django.http import HttpResponse
from django.shortcuts import redirect

from core.models import Event

def view(request, event_id):
	event = Event.objects.get(pk=int(event_id))
	return redirect('/history/' + str(event.history.id))