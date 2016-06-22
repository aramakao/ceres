# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(default=b'farm_category/category.jpg', upload_to=b'farm_category'),
            preserve_default=True,
        ),
    ]
