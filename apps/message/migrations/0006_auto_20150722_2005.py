# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_messagegroup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagegroup',
            old_name='receiver',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='messagegroup',
            old_name='sender',
            new_name='user',
        ),
    ]
