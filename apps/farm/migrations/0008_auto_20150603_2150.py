# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0001_initial'),
        ('farm', '0007_remove_farmprofile_web_site2'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmprofile',
            name='city',
            field=models.ForeignKey(blank=True, to='extras.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='farmprofile',
            name='region',
            field=models.ForeignKey(blank=True, to='extras.Region', null=True),
            preserve_default=True,
        ),
    ]
