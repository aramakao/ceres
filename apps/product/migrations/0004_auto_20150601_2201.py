# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', unique_with=(b'name',), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', unique_with=(b'name',), editable=False),
            preserve_default=True,
        ),
    ]
