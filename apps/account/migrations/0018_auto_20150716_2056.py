# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20150716_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='InivitationFriend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(related_name='invitation_friend_friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='invitation_friend_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='inivitationfriend',
            unique_together=set([('user', 'friend')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 16, 20, 56, 41, 672515)),
            preserve_default=True,
        ),
    ]
