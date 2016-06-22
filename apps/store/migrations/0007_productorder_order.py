# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_productorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(default=12, to='store.PurchaseOrder'),
            preserve_default=False,
        ),
    ]
