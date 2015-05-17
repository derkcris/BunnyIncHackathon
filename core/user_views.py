import sys

from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from . import views
from core.models import Client, Owner


def user_login(request):
	error_message = False
	username = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		# Search by email
		if user is None:
			possible_user = User.objects.filter(email=username)
			if possible_user:
				username = possible_user[0].username
				user = authenticate(username=username, password=password)

		# Auth
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/dashboard')
			else:
				error_message = 'Disabled account'
		else:
			error_message = 'Invalid user/password'

	context = {
		'error_message'	: error_message,
		'username'		: username,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'user/login.html', context)


def user_logout(request):
	logout(request)
	return redirect('/')


def register(request):
	error_message = False
	if request.POST:

		if request.POST['username']\
			and request.POST['password']\
			and request.POST['password']\
			and request.POST['first_name']\
			and request.POST['last_name']:
			try:
				user = User.objects.create_user(
					request.POST['username'].lower(),
					request.POST['email'].lower(),
					request.POST['password']
				)

				user.first_name = request.POST['first_name']
				user.last_name = request.POST['last_name']
				user.save()

				client = Client(user=user, created=timezone.now())
				client.save()

				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request, user)
				return redirect('/dashboard')
			except ValueError as e:
				error_message = e
		else:
			error_message = 'Some fields are required.'

	context = {
		'error_message'	: error_message,
		'user'			: views.user_status(request),
		'shopping_cart'	: views.shopping_cart_status(request)
	}
	return render(request, 'user/register.html', context)