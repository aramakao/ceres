# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20150713_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateUserLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.ForeignKey(to='account.StateUser')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stateuserlike',
            unique_together=set([('user', 'state')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 15, 3, 59, 29, 817218)),
            preserve_default=True,
        ),
    ]
