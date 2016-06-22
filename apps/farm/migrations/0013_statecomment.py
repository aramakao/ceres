# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farm', '0012_auto_20150605_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('hearts', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(upload_to=b'states_img', blank=True)),
                ('state', models.ForeignKey(to='farm.State')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
