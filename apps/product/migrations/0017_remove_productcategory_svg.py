# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20151202_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='svg',
        ),
    ]
