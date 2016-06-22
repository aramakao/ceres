# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_mailbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='mail',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='phone',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailbox',
            name='user',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
