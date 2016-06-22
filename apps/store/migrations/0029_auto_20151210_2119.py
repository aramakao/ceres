# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_auto_20151210_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='price',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='product',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='shipping',
        ),
    ]
