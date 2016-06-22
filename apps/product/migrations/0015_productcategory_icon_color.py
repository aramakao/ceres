# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_productcategory_svg'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='icon_color',
            field=models.ImageField(default=b'farm_category/no_image.jpg', upload_to=b'farm_category'),
            preserve_default=True,
        ),
    ]
