# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0013_statecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmprofile',
            name='google_analytics',
        ),
    ]
