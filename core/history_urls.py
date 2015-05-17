from django.conf.urls import url

from . import history_views

urlpatterns = [
    url(r'^search/', history_views.search, name='search'),
    url(r'^(?P<history_id>[0-9]+)/$', history_views.view, name='view'),
]