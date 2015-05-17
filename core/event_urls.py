from django.conf.urls import url

from . import event_views

urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', event_views.view, name='view'),
]