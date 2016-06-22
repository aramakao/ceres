# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0011_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='picture',
            field=models.ImageField(default=1, upload_to=b'states_img', blank=True),
            preserve_default=False,
        ),
    ]
