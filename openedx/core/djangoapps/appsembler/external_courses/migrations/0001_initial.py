# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalCourseTile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_key', models.CharField(unique=True, max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('org', models.CharField(max_length=255)),
                ('course_link', models.URLField()),
                ('image_url', models.URLField()),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField()),
                ('pacing_type', models.CharField(max_length=255)),
                ('is_credit_eligible', models.BooleanField(default=False)),
                ('is_verified_eligible', models.BooleanField(default=False)),
            ],
        ),
    ]
