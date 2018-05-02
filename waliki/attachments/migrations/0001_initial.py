# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import waliki.settings


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0003_auto_20141110_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('file', models.FileField(upload_to=waliki.settings.WALIKI_UPLOAD_TO)),
                ('page', models.ForeignKey(related_name='attachments', to='waliki.Page', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
            bases=(models.Model,),
        ),
    ]
