# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0009_auto_20150604_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmprofile',
            name='location_slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, populate_from=b'location', always_update=True),
            preserve_default=False,
        ),
    ]
