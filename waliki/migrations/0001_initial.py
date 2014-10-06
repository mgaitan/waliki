# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ACLRule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=200, verbose_name='Name')),
                ('slug', models.CharField(max_length=200)),
                ('as_namespace', models.BooleanField(default=False, verbose_name='As namespace')),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name_plural': 'ACL rules',
                'verbose_name': 'ACL rule',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.CharField(unique=True, max_length=200)),
                ('path', models.CharField(unique=True, max_length=200)),
                ('markup', models.CharField(max_length=20, default='reStructuredText', choices=[('reStructuredText', 'reStructuredText'), ('Markdown', 'Markdown')], verbose_name='Markup')),
            ],
            options={
                'permissions': (('view_page', 'Can view page'),),
                'verbose_name_plural': 'Pages',
                'verbose_name': 'Page',
            },
            bases=(models.Model,),
        ),
    ]
