# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_inivitationgroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inivitationgroup',
            unique_together=set([('group', 'user')]),
        ),
    ]
