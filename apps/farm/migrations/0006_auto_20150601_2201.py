# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0005_delete_productcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', unique_with=(b'name',), editable=False),
            preserve_default=True,
        ),
    ]
