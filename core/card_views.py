import sys

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from . import views
from core.models import Place, Event, Card

@login_required
def add(request, model, model_id):
	model = model.lower()
	obj = loadObject(model, int(model_id))
	error_message = False
	if request.POST:
		name = request.POST['name']
		type = request.POST['type']
		if name and type:
			card = Card(
				user = request.user,
				model = model,
				model_id = model_id,
				name = name,
				created = timezone.now(),
				type = type,
				content = generateContent(type)
			)
			card.save()
			return redirect('/' + model + '/' + model_id)
		else:
			error_message = 'Some fields are required.'
	context = {
		'obj'			: obj,
		'model'			: model,
		'model_id'		: model_id,
		'types'			: supportedTypes(),
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'card/add.html', context)


def loadObject(model, model_id):
	if model == 'place':
		return Place.objects.get(pk=model_id)
	if model == 'event':
		return Event.objects.get(pk=model_id)


def supportedTypes():
	types = [{
			'id' 	: 'link',
			'name' 	: 'Link',
			'text' 	: 'Share content from other services',
			'class'	: 'glyphicon glyphicon-link'
		}, {
			'id' 	: 'text',
			'name' 	: 'Text',
			'text' 	: 'Describe your trip, places, moments, etc.',
			'class'	: 'glyphicon glyphicon-align-left'
		}, {
			'id'	: 'facebook',
			'name'	: 'Facebook',
			'text'	: 'Add content from your Facebook profile',
			'class'	: 'glyphicon glyphicon-thumbs-up'
		}, {
			'id'	: 'instagram',
			'name'	: 'Instagram',
			'text'	: 'Include your best pictures!',
			'class'	: 'glyphicon glyphicon-picture'
		}, {
			'id' 	: 'map',
			'name' 	: 'Google maps',
			'text' 	: 'Include the exactly ubication',
			'class'	: 'glyphicon glyphicon-map'
		}
	]
	return types


def generateContent(type):
	if type == 'link':
		return '<a href="http://runway.is/" class="btn btn-default">runway.is</a>'
	if type == 'text':
		return '<ul><li>Golden Gate Park</li><li>Embarcadero</li><li>Chocolate store</li></ul>'
	if type == 'facebook':
		return '<img src="http://img.svbtle.com/pugis6oroxzxcg.png" width="100%">'
	if type == 'instagram':
		return '<img src="https://igcdn-photos-a-a.akamaihd.net/hphotos-ak-xaf1/t51.2885-15/11256822_1418709128449920_1504567737_n.jpg" width="100%">'
	if type == 'map':
		return '<img src="http://mike.teczno.com/img/google-maps-track.png" width="100%">'
