# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='svg',
            field=models.TextField(default=b'none'),
            preserve_default=True,
        ),
    ]
