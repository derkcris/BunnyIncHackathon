import operator
from datetime import datetime, timedelta
from itertools import chain
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from . import views
from core.models import Option, Place, OptionPlace, Card, History, Event


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

def checkout(request):
	cart = []
	if settings.SHOPPING_CART_KEY in request.session:
		cart = request.session[settings.SHOPPING_CART_KEY]
		i = 0
		for event in cart:
			place = Place.objects.get(pk=event['place'])
			event['index'] = i
			event['days'] = int(event['days'])
			event['start'] = date_object = datetime.strptime(event['start'], '%m/%d/%Y') # 12/31/2015
			event['end'] = event['start'] + timedelta(days=event['days'])
			event['place_name'] = place.name
			event['location'] = place.location
			event['price_base'] = float(place.price_base)
			event['price'] = place.price() * event['days']
			event['currency'] = place.currency
			i = i+1
	context = {
		'cart'			: cart,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'history/checkout.html', context)


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
		context['cart'] = cart # TODO remove

	return JsonResponse(context)

