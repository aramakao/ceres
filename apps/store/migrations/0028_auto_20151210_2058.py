# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20151202_2238'),
        ('store', '0027_auto_20151207_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='product',
            field=models.ForeignKey(default=1, to='product.Product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipping',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
