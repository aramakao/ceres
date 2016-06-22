# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20150715_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(related_name='friend_friend', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='friend_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('user', 'friend')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 16, 14, 54, 22, 940327)),
            preserve_default=True,
        ),
    ]
