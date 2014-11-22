# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waliki', '0003_auto_20141110_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('old_slug', models.CharField(max_length=200, unique=True)),
                ('new_slug', models.CharField(max_length=200)),
                ('status_code', models.IntegerField(default=302, max_length=3, choices=[(302, '302 Found'), (301, '301 Moved Permanently')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
