# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20150822_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackseller',
            name='reply',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
