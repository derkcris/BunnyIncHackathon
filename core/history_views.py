import operator
from datetime import datetime, timedelta
from itertools import chain
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from . import views
from core.models import Option, Place, OptionPlace, Card, History, Event, Client


def search(request):
	q = request.GET.get('q', '')
	if q:
		filters = q.lower().split(' ')
		# Histories
		query = reduce(operator.or_, (
			Q(name__icontains = f) | Q(sumary__icontains = f) for f in filters)
		)
		query_log = str(query)
		histories = History.objects.filter(query).order_by('-created')

		# Places
		query = reduce(operator.or_, (
			Q(name__icontains = f) | Q(location__icontains = f) for f in filters)
		)
		query_log += ' - ' + str(query)
		places = Place.objects.filter(query).order_by('-created')

		# Add place results to histories
		histories = list(chain(histories))
		for place in places:
			place_histories = list(chain(place.histories()))
			for h in place_histories:
				if h not in histories:
					histories.append(h)
	else:
		histories = []
		filters = []
		query_log = ''

	context = {
		'q'				: q,
		'histories'		: histories,
		'filters'		: filters,
		'query'			: query_log,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'history/search.html', context)


def view(request, history_id):
	history = get_object_or_404(History, pk=history_id)
	context = {
		'history' 		: history,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'history/view.html', context)

@login_required
def checkout(request):
	name = ''
	sumary = ''
	error_message = False
	cart = []
	if request.POST:
		name = request.POST['name']
		sumary = request.POST['sumary']
		if name and sumary:
			cart = request.session[settings.SHOPPING_CART_KEY]
			# Check client status
			client = Client.objects.filter(user__id = request.user.id)
			if client: # User is already registered as client
				client = client[0]
			else:
				client = Client(user=request.user, created=timezone.now())
				client.save()
			# Create history and events
			history = History(
				client = client,
				name = name,
				sumary = sumary,
				created = timezone.now()
			)
			history.save()
			for ev in cart:
				place = Place.objects.get(pk=ev['place'])
				ev = complete_event(ev, place)
				event = Event(
					history = history,
					place = place,
					created = timezone.now(),
					start = ev['start'],
					end = ev['end']
				)
				event.save()
			del request.session[settings.SHOPPING_CART_KEY]
			return redirect('/history/' + str(history.id))

		else:
			error_message = 'Some fields are required.'

	if settings.SHOPPING_CART_KEY in request.session:
		cart = request.session[settings.SHOPPING_CART_KEY]
		i = 0
		for ev in cart:
			place = Place.objects.get(pk=ev['place'])
			ev['index'] = i
			ev = complete_event(ev, place)
			i = i+1

	context = {
		'name'			: name,
		'sumary'		: sumary,
		'cart'			: cart,
		'error_message'	: error_message,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'history/checkout.html', context)


def complete_event(ev, place):
	ev['days'] = int(ev['days'])
	ev['start'] = date_object = datetime.strptime(ev['start'], '%m/%d/%Y') # 12/31/2015
	ev['end'] = ev['start'] + timedelta(days=ev['days'])
	ev['place_name'] = place.name
	ev['location'] = place.location
	ev['price_base'] = float(place.price_base)
	ev['price'] = place.price() * ev['days']
	ev['currency'] = place.currency
	return ev


@login_required
def checkout_remove(request, index):
	if settings.SHOPPING_CART_KEY in request.session:
		cart = request.session[settings.SHOPPING_CART_KEY]
		index = int(index)
		cart.remove( cart[index] )
		request.session[settings.SHOPPING_CART_KEY] = cart

	return redirect('/history/checkout')


def ajax_add_place(request):
	context = {}
	if request.POST:
		cart = []
		event = {
			'place'		: request.POST['place'],
			'days'		: request.POST['days'],
			'start'		: request.POST['start']
		}
		# Add shopping card, if not exist
		if settings.SHOPPING_CART_KEY in request.session:
			cart = request.session[settings.SHOPPING_CART_KEY]

		cart.append(event)
		request.session[settings.SHOPPING_CART_KEY] = cart
		context['status'] = 'success'
		context['length'] = len(cart) # TODO remove

	return JsonResponse(context)

