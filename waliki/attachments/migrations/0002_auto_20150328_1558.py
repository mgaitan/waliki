# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import waliki.settings


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=waliki.settings.WALIKI_UPLOAD_TO, max_length=300),
        ),
    ]
