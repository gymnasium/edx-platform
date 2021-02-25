from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.db.models import Q
from souvenirs.control import count_active_users
from souvenirs.models import Souvenir
from souvenirs.reports import _usage_for_periods


def usage_for_periods(periods):
    """
    Augment django-souvenirs's usage_for_periods with learners and staff.

    django-souvenirs uses this wrapper via
    settings.SOUVENIRS_USAGE_REPORTS_FUNCTION

    """
    for d in _usage_for_periods(periods):
        d['usage'].update(learners_and_staff(start=d['period']['start'],
                                             end=d['period']['end']))
        yield d


def learners_and_staff(start, end):
    """
    Return a dict counting the registered, activated and active learners and
    staff as of the given date. See also souvenirs.reports.registered_users_as_of
    """
    users = get_user_model().objects.filter(date_joined__lt=end)

    is_admin = Q(is_superuser=True)
    none_of_the_above = ~is_admin

    is_global_staff = Q(is_staff=True) & none_of_the_above
    none_of_the_above = none_of_the_above | ~is_global_staff

    is_course_staff = Q(courseaccessrole__role='staff') & none_of_the_above
    none_of_the_above = none_of_the_above | ~is_course_staff

    is_instructor = Q(courseaccessrole__role='instructor') & none_of_the_above
    none_of_the_above = none_of_the_above | ~is_instructor

    is_learner = none_of_the_above

    registered = lambda q: users.filter(q).count()
    activated = lambda q: users.filter(is_active=True).filter(q).count()
    active = lambda q: count_active_users(
        start, end, qs=Souvenir.objects.filter(user=users.filter(q)))

    return dict(
        registered_admins=registered(is_admin),
        activated_admins=activated(is_admin),
        active_admins=active(is_admin),

        registered_staff=registered(is_global_staff | is_course_staff),
        activated_staff=activated(is_global_staff | is_course_staff),
        active_staff=active(is_global_staff | is_course_staff),

        registered_instructors=registered(is_instructor),
        activated_instructors=activated(is_instructor),
        active_instructors=active(is_instructor),

        registered_learners=registered(is_learner),
        activated_learners=activated(is_learner),
        active_learners=active(is_learner),
    )
