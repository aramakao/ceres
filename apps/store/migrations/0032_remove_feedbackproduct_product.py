# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_purchaseorder_total_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackproduct',
            name='product',
        ),
    ]
