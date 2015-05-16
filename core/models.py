from django.db import models


class User(models.Model):
    admin = models.BooleanField()
    owner = models.BooleanField()
    client = models.BooleanField()

    def __str__(self):
    	return self.user.first_name + ' ' + self.user.last_name


class Option(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
    	return self.name


class Place(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5)
    location = models.CharField(max_length=50)
    created = models.DateTimeField()

    def __str__(self):
    	return self.name


class OptionsPlace(models.Model):
    place = models.ForeignKey(Place)
    option = models.ForeignKey(Option)

    def __str__(self):
    	return self.place + ' - ' + self.option


class Card(models.Model):
    user = models.ForeignKey(User)
    model = models.CharField(max_length=50)
    model_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created = models.DateTimeField()
    type = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
    	return self.type + ' - ' + self.name


class History(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    created = models.DateTimeField()

    def __str__(self):
    	return self.name

# TODO find a better name
class Event(models.Model):
    history = models.ForeignKey(History)
    place = models.ForeignKey(Place)
    created = models.DateTimeField()
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
    	return self.history + ' - ' + self.place

