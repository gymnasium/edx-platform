from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class CreateUpdateMixin(models.Model):
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Customer(CreateUpdateMixin, models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    quota = models.IntegerField()

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return 'id={} name={!r}'.format(self.id, self.name)


class UsageMixin(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()

    sum_registered_users = models.IntegerField()
    sum_activated_users = models.IntegerField()
    sum_active_users = models.IntegerField()

    sum_registered_admins = models.IntegerField()
    sum_activated_admins = models.IntegerField()
    sum_active_admins = models.IntegerField()

    sum_registered_staff = models.IntegerField()
    sum_activated_staff = models.IntegerField()
    sum_active_staff = models.IntegerField()

    sum_registered_instructors = models.IntegerField()
    sum_activated_instructors = models.IntegerField()
    sum_active_instructors = models.IntegerField()

    sum_registered_learners = models.IntegerField()
    sum_activated_learners = models.IntegerField()
    sum_active_learners = models.IntegerField()

    class Meta:
        abstract = True


class UsageDaily(CreateUpdateMixin, UsageMixin, models.Model):
    date = models.DateField()
    label_year_month = models.CharField(max_length=20)
    label_year_quarter = models.CharField(max_length=20)
    label_year = models.CharField(max_length=20)

    class Meta:
        db_table = 'usage_daily'


class UsageCustomerMonthly(CreateUpdateMixin, UsageMixin, models.Model):
    label_year_month = models.CharField(max_length=20)
    label_year_quarter = models.CharField(max_length=20)
    label_year = models.CharField(max_length=20)

    class Meta:
        db_table = 'usage_customer_monthly'


class UsageCustomerQuarterly(CreateUpdateMixin, UsageMixin, models.Model):
    label_year_quarter = models.CharField(max_length=20)
    label_year = models.CharField(max_length=20)

    class Meta:
        db_table = 'usage_customer_quarterly'


class UsageCustomerYearly(CreateUpdateMixin, UsageMixin, models.Model):
    label_year = models.CharField(max_length=20)

    class Meta:
        db_table = 'usage_customer_yearly'


class UsageCalendarMonthly(CreateUpdateMixin, UsageMixin, models.Model):
    label_calendar_year_month = models.CharField(max_length=20)
    label_calendar_year = models.IntegerField()

    class Meta:
        db_table = 'usage_calendar_monthly'
