# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20150824_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailbox',
            old_name='mail',
            new_name='email',
        ),
    ]
