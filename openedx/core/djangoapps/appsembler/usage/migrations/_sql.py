from __future__ import absolute_import, unicode_literals

from django.db import migrations


def row_level_security(tables):
    return [
        migrations.RunSQL(
            "ALTER TABLE {table} ENABLE  ROW LEVEL SECURITY;".format(table=table),
            "ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;".format(table=table)
        ) for table in tables
    ]


def boxes_rls(tables, customer_id_column):
    return [
        migrations.RunSQL(
            """CREATE POLICY {table}_boxes ON {table} TO boxes
               USING ({customer_id_column} LIKE current_user || '__%')
               WITH CHECK ({customer_id_column} LIKE current_user || '__%');""".format(
                       table=table,
                       customer_id_column=customer_id_column,
               ),
            "DROP POLICY {table}_boxes ON {table};".format(table=table)
        ) for table in tables
    ]


def reports_rls(tables):
    return [
        migrations.RunSQL(
            "CREATE POLICY {table}_reports ON {table} TO reports USING (true);".format(
                table=table,
            ),
            "DROP POLICY {table}_reports ON {table};".format(table=table)
        ) for table in tables
    ]


def boxes_grants(tables):
    return [
        migrations.RunSQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON {tables} TO boxes;".format(
                tables=', '.join(tables)),
            "REVOKE ALL ON {tables} FROM boxes;".format(tables=', '.join(tables))
        ),
        migrations.RunSQL(
            "GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO boxes;",
            "REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM boxes;"
        )
    ]


def reports_grants(tables):
    return [
        migrations.RunSQL(
            "GRANT SELECT ON {tables} TO reports;".format(tables=', '.join(tables)),
            "REVOKE ALL ON {tables} FROM reports;".format(tables=', '.join(tables))
        )
    ]
