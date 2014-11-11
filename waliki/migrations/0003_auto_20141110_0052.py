# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0002_aclrule_apply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aclrule',
            name='apply_to',
            field=models.CharField(choices=[('any', 'Any user'), ('logged', 'Any authenticated user'), ('staff', 'Any staff member'), ('superusers', 'Any superuser'), ('explicit', 'Any user/group explicitly defined')], default='explicit', max_length=25),
            #preserve_default=True,
        ),
    ]
