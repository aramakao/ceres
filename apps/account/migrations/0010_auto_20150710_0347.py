# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20150630_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('hearts', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(upload_to=b'states_img', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StateUserComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('hearts', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(upload_to=b'states_img', blank=True)),
                ('state', models.ForeignKey(to='account.StateUser')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 10, 3, 47, 10, 161267)),
            preserve_default=True,
        ),
    ]
