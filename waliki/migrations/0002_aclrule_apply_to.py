# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aclrule',
            name='apply_to',
            field=models.CharField(choices=[('any', 'Any user'), ('logged', 'Any logged in user'), ('staff', 'Any staff member'), ('superusers', 'Any superuser'), ('explicit', 'Any user/group explicitly defined')], max_length=25, default='explicit'),
            preserve_default=True,
        ),
    ]
