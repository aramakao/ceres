# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20150824_2125'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Advert',
        ),
    ]
