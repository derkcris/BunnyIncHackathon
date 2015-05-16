from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from . import views
from core.models import Client, Owner, Story

@login_required
def dashboard(request):
	client = Client.objects.filter(user__id = request.user.id)
	if client:
		return dashboard_client(request, client[0])

	owner = Owner.objects.filter(user__id = request.user.id)
	if owner:
		return dashboard_owner(request, owner[0])

	return redirect('/admin')

def dashboard_client(request, client):
	stories = Story.objects.filter(client_id = client.id).order_by('-created')
	context = {
		'stories'		: stories,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'dashboard/client.html', context)


def dashboard_owner(request, owner):
	context = {
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'dashboard/owner.html', context)