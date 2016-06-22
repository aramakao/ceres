# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20150820_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackseller',
            name='reply',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
