import operator
from itertools import chain
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from core.models import Client, Owner, Option, Place, OptionPlace, Card, History, Event

def index(request):
	context = {}
	return render(request, 'landing/home.html', context)


def history_search(request):
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
		'q'			: q,
		'histories'	: histories,
		'filters'	: filters,
		'query'		: query_log
	}
	return render(request, 'history/search.html', context)


def history_view(request, history_id):
	history = get_object_or_404(History, pk=history_id)
	context = {
		'history' : history
	}
	return render(request, 'history/view.html', context)