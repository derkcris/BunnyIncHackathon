from django.conf.urls import url

from . import card_views

urlpatterns = [
    url(r'^add/(?P<model>[a-z]+)/(?P<model_id>[0-9]+)/$', card_views.add, name='add'),
]