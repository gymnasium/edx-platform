from __future__ import absolute_import, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsembler_usage', '0002_add_row_level_security'),
    ]

    operations = [
        migrations.RunSQL(
            "GRANT SELECT ON django_migrations TO boxes;",
            migrations.RunSQL.noop  # don't actually REVOKE
        ),
    ]
