from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Client)
admin.site.register(Owner)
admin.site.register(Option)
admin.site.register(Place)
admin.site.register(OptionPlace)
admin.site.register(Story)
admin.site.register(Event)