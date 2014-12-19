# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import project_share.models


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('lib_file', models.FileField(upload_to=project_share.models.module_library)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('module_file', models.FileField(null=True, upload_to=project_share.models.module_module, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='module',
            field=models.ForeignKey(blank=True, to='project_share.Module', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='f',
            field=models.FileField(upload_to=b'files/%Y-%m-%d/'),
            preserve_default=True,
        ),
    ]
