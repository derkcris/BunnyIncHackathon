from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def index(request):
	context = {
		'user'			: user_status(request),
		'shopping_cart' : shopping_cart_status(request)
	}
	return render(request, 'landing/home.html', context)

def shopping_cart_status(request):
	if settings.SHOPPING_CART_KEY in request.session:
		return request.session[settings.SHOPPING_CART_KEY]

def user_status(request):
	if request.user.is_authenticated():
		return request.user
