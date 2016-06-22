# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
