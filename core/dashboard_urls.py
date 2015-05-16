from django.conf.urls import url

from . import dashboard_views

urlpatterns = [
    url(r'^$', dashboard_views.dashboard, name='dashboard'),
]