# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='index',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
