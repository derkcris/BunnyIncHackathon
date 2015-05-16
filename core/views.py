from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

# Create your views here.

def index(request):
	context = {}
	return render(request, 'landing/home.html', context)