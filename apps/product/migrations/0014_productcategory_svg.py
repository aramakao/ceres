# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productcategory_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='svg',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
    ]
