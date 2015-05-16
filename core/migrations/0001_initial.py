# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=50)),
                ('model_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField()),
                ('type', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OptionsPlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.ForeignKey(to='core.Option')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('price_base', models.DecimalField(max_digits=10, decimal_places=2)),
                ('currency', models.CharField(max_length=5)),
                ('location', models.CharField(max_length=50)),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin', models.BooleanField()),
                ('owner', models.BooleanField()),
                ('client', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='optionsplace',
            name='place',
            field=models.ForeignKey(to='core.Place'),
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='history',
            field=models.ForeignKey(to='core.History'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='core.Place'),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
    ]
