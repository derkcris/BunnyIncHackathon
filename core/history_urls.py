from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/', views.history_search, name='search'),
    url(r'^(?P<history_id>[0-9]+)/$', views.history_view, name='view'),
]