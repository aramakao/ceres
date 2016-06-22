# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0014_remove_farmprofile_google_analytics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='user',
        ),
        migrations.RemoveField(
            model_name='statecomment',
            name='state',
        ),
        migrations.DeleteModel(
            name='State',
        ),
        migrations.RemoveField(
            model_name='statecomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='StateComment',
        ),
    ]
