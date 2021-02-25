# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('quota', models.IntegerField()),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='UsageCalendarMonthly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('sum_registered_users', models.IntegerField()),
                ('sum_registered_learners', models.IntegerField()),
                ('sum_registered_staff', models.IntegerField()),
                ('sum_activated_users', models.IntegerField()),
                ('sum_activated_learners', models.IntegerField()),
                ('sum_activated_staff', models.IntegerField()),
                ('sum_active_users', models.IntegerField()),
                ('sum_active_learners', models.IntegerField()),
                ('sum_active_staff', models.IntegerField()),
                ('label_calendar_year_month', models.CharField(max_length=20)),
                ('label_calendar_year', models.IntegerField()),
                ('customer', models.ForeignKey(to='appsembler_usage.Customer')),
            ],
            options={
                'db_table': 'usage_calendar_monthly',
            },
        ),
        migrations.CreateModel(
            name='UsageCustomerMonthly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('sum_registered_users', models.IntegerField()),
                ('sum_registered_learners', models.IntegerField()),
                ('sum_registered_staff', models.IntegerField()),
                ('sum_activated_users', models.IntegerField()),
                ('sum_activated_learners', models.IntegerField()),
                ('sum_activated_staff', models.IntegerField()),
                ('sum_active_users', models.IntegerField()),
                ('sum_active_learners', models.IntegerField()),
                ('sum_active_staff', models.IntegerField()),
                ('label_year_month', models.CharField(max_length=20)),
                ('label_year_quarter', models.CharField(max_length=20)),
                ('label_year', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(to='appsembler_usage.Customer')),
            ],
            options={
                'db_table': 'usage_customer_monthly',
            },
        ),
        migrations.CreateModel(
            name='UsageCustomerQuarterly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('sum_registered_users', models.IntegerField()),
                ('sum_registered_learners', models.IntegerField()),
                ('sum_registered_staff', models.IntegerField()),
                ('sum_activated_users', models.IntegerField()),
                ('sum_activated_learners', models.IntegerField()),
                ('sum_activated_staff', models.IntegerField()),
                ('sum_active_users', models.IntegerField()),
                ('sum_active_learners', models.IntegerField()),
                ('sum_active_staff', models.IntegerField()),
                ('label_year_quarter', models.CharField(max_length=20)),
                ('label_year', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(to='appsembler_usage.Customer')),
            ],
            options={
                'db_table': 'usage_customer_quarterly',
            },
        ),
        migrations.CreateModel(
            name='UsageCustomerYearly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('sum_registered_users', models.IntegerField()),
                ('sum_registered_learners', models.IntegerField()),
                ('sum_registered_staff', models.IntegerField()),
                ('sum_activated_users', models.IntegerField()),
                ('sum_activated_learners', models.IntegerField()),
                ('sum_activated_staff', models.IntegerField()),
                ('sum_active_users', models.IntegerField()),
                ('sum_active_learners', models.IntegerField()),
                ('sum_active_staff', models.IntegerField()),
                ('label_year', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(to='appsembler_usage.Customer')),
            ],
            options={
                'db_table': 'usage_customer_yearly',
            },
        ),
        migrations.CreateModel(
            name='UsageDaily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('period_start', models.DateTimeField()),
                ('period_end', models.DateTimeField()),
                ('sum_registered_users', models.IntegerField()),
                ('sum_registered_learners', models.IntegerField()),
                ('sum_registered_staff', models.IntegerField()),
                ('sum_activated_users', models.IntegerField()),
                ('sum_activated_learners', models.IntegerField()),
                ('sum_activated_staff', models.IntegerField()),
                ('sum_active_users', models.IntegerField()),
                ('sum_active_learners', models.IntegerField()),
                ('sum_active_staff', models.IntegerField()),
                ('date', models.DateField()),
                ('label_year_month', models.CharField(max_length=20)),
                ('label_year_quarter', models.CharField(max_length=20)),
                ('label_year', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(to='appsembler_usage.Customer')),
            ],
            options={
                'db_table': 'usage_daily',
            },
        ),
    ]
