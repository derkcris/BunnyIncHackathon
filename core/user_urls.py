from django.conf.urls import url

from . import user_views

urlpatterns = [
    url(r'^login/', user_views.user_login, name='login'),
    url(r'^logout/', user_views.user_logout, name='logout'),
    url(r'^register/', user_views.register, name='register'),
]