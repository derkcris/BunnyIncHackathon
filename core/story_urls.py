from django.conf.urls import url

from . import story_views

urlpatterns = [
    url(r'^search/', story_views.search, name='search'),
    url(r'^(?P<story_id>[0-9]+)/$', story_views.view, name='view'),
    url(r'^checkout/$', story_views.checkout, name='checkout'),
    url(r'^checkout/remove/(?P<index>[0-9]+)/$', story_views.checkout_remove, name='checkout_remove'),
    url(r'^ajax_add_place/', story_views.ajax_add_place, name='ajax_add_place'),
]