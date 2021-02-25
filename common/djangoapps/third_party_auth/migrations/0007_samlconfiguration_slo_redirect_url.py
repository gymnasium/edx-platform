# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('third_party_auth', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='samlconfiguration',
            name='slo_redirect_url',
            field=models.CharField(default=b'/logout', help_text=b'The url to redirect the user after process the SLO response', max_length=255, verbose_name=b'SLO post redirect URL', blank=True),
        ),
    ]
