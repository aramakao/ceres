# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150901_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', unique_with=(b'name',), editable=False),
            preserve_default=True,
        ),
    ]
