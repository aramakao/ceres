# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20150831_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='icon',
            field=models.ImageField(default=b'farm_category/no_image.jpg', upload_to=b'farm_category'),
            preserve_default=True,
        ),
    ]
