# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_feedbackseller_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackproduct',
            name='description',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedbackproduct',
            name='price',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedbackproduct',
            name='quality',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=True,
        ),
    ]
