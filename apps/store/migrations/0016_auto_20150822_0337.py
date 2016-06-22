# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20150822_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackseller',
            name='reply',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
