from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User)
    created = models.DateTimeField()

    def __str__(self):
    	return self.user.first_name + ' ' + self.user.last_name


class Owner(models.Model):
    user = models.OneToOneField(User)
    created = models.DateTimeField()

    def __str__(self):
    	return self.user.first_name + ' ' + self.user.last_name


class Option(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
    	return self.name


class Place(models.Model):
    owner = models.ForeignKey(Owner)
    name = models.CharField(max_length=200)
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5)
    location = models.CharField(max_length=50)
    created = models.DateTimeField()

    def cards(self):
    	return Card.objects.filter(
    		model = 'place',
    		model_id = self.id
    	)

    def stories(self):
    	return Story.objects.filter(event__place__id = self.id)

    def price(self):
    	return float(self.price_base) + float(self.price_base) * settings.SERVICE_FEE

    def __str__(self):
    	return self.name


class OptionPlace(models.Model):
    place = models.ForeignKey(Place)
    option = models.ForeignKey(Option)

    def __str__(self):
    	return str(self.place) + ' - ' + str(self.option)


class Card(models.Model):
    user = models.ForeignKey(User)
    model = models.CharField(max_length=50)
    model_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created = models.DateTimeField()
    type = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
    	return self.name + ' (' + self.model + ')'


class Story(models.Model):
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=100)
    sumary = models.TextField()
    created = models.DateTimeField()

    def start(self):
    	result = self.event_set.all().order_by('start')[:1]
    	if result:
    		return result[0].created

    def end(self):
    	result = self.event_set.all().order_by('-end')[:1]
    	if result:
    		return result[0].end

    def __str__(self):
    	return self.name

# TODO find a better name
class Event(models.Model):
    story = models.ForeignKey(Story)
    place = models.ForeignKey(Place)
    created = models.DateTimeField()
    start = models.DateField()
    end = models.DateField()

    def cards(self):
    	return Card.objects.filter(
    		model = 'event',
    		model_id = self.id
    	)

    def __str__(self):
    	return str(self.place) + ' (' + str(self.story) + ')'

