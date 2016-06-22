# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_remove_feedbackproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackproduct',
            name='order',
            field=models.OneToOneField(to='store.PurchaseOrder'),
        ),
    ]
