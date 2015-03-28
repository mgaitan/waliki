# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0005_auto_20141124_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='markup',
            field=models.CharField(max_length=20, choices=[('reStructuredText', 'reStructuredText')], default='reStructuredText', verbose_name='Markup'),
            preserve_default=True,
        ),
    ]
