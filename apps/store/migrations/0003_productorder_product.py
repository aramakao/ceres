# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20150804_0645'),
        ('store', '0002_remove_productorder_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(default=1, to='product.Product'),
            preserve_default=False,
        ),
    ]
