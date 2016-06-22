# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productorder_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackproduct',
            name='order',
        ),
        migrations.AddField(
            model_name='feedbackproduct',
            name='product',
            field=models.OneToOneField(default=1, to='store.ProductOrder'),
            preserve_default=False,
        ),
    ]
