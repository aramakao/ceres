# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_stategroup_stategroupcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stategroupcomment',
            old_name='state_group',
            new_name='state',
        ),
    ]
