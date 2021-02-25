from __future__ import absolute_import, unicode_literals

from django.db import migrations
from ._sql import (row_level_security, boxes_rls, reports_rls,
                   boxes_grants, reports_grants)


customer_table = 'customer'

usage_tables = [
    'usage_daily',
    'usage_customer_monthly',
    'usage_customer_quarterly',
    'usage_customer_yearly',
    'usage_calendar_monthly',
]

all_tables = [customer_table] + usage_tables


class Migration(migrations.Migration):

    dependencies = [
        ('appsembler_usage', '0001_initial'),
    ]

    operations = (row_level_security(all_tables) +
                  boxes_rls([customer_table], 'id') +
                  boxes_rls(usage_tables, 'customer_id') +
                  reports_rls(all_tables) +
                  boxes_grants(all_tables) +
                  reports_grants(all_tables))
