# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20150816_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackproduct',
            name='order',
            field=models.ForeignKey(default=12, to='store.PurchaseOrder'),
            preserve_default=False,
        ),
    ]
