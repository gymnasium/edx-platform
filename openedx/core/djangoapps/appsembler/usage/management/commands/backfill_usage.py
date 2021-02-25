from __future__ import absolute_import, unicode_literals

import collections
import glob
import gzip
import itertools
import json
import logging
import operator
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
import isodate
from souvenirs.control import souvenez
from ._helpers import DateAction


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Backfills django-souvenirs from tracking logs"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.hacked_user_ids = None
        self.missing_user_ids = set()

    def add_arguments(self, parser):
        parser.add_argument('--after', metavar='DATE', action=DateAction, help="(inclusive)")
        parser.add_argument('--before', metavar='DATE', action=DateAction, help="(exclusive)")
        parser.add_argument('--ratelimit', type=int, default=True, help="override rate-limiting")
        parser.add_argument('--hack', action='store_true', help="add user ids to DB")
        parser.add_argument('logs', nargs='*', help="tracking logs (default: /edx/var/log/tracking)")

        # this works to speed things up on the first run, but it's probably
        # better to leave it commented because if you accidentally run twice
        # with this, you'll have double the rows in the souvenirs table.
        #parser.add_argument('--no-check', action='store_true', help="don't check for dups (first time optimization)")

    def handle(self, *args, **options):
        if options['hack'] and not settings.DEBUG:
            raise CommandError("unwilling to hack users on deployed system")

        logs = check_and_sort_logs(options['logs'])

        self.override_cache()

        counters = collections.defaultdict(int, added=0)

        for log in logs:
            self.stdout.write("processing {}".format(log))
            for lineno, event, exc in json_records_from(log):
                result = self.souvenez_event(log, lineno, event, exc, options)
                counters[result] += 1

        self.stdout.write("done!\n\n")

        total = reduce(operator.add, counters.values())
        output = "processed {} lines:\n".format(total)
        for k, v in sorted(counters.items()):
            output += '{:>8} {}\n'.format(v, k)

        return output  # prints on stdout

    def souvenez_event(self, log, lineno, event, exc, options):
        """
        Process one line from a tracking log, calling souvenez if there's a
        usable user_id and time stamp.
        """
        if exc:
            self.stderr.write("{} (json) at line {}: {}\n".format(
                exc.__class__.__name__, lineno, exc))
            return 'json exception'

        try:
            user_id = event['context']['user_id']
            time = event['time']
        except (KeyError, TypeError):
            return 'ignored (no user id)'
        if not user_id:
            return 'ignored (no user id)'

        try:
            # time value in JSON should be strict, so use isodate
            # rather than dateutil to parse.
            dt = isodate.parse_datetime(time)
        except Exception as e:
            self.stderr.write("{} (isodate) at line {}: {}\n".format(
                e.__class__.__name__, lineno, e))
            return 'date parsing exception'

        if options['hack']:
            self.hack_user(user_id, time)

        if options['after'] and dt < options['after']:
            return 'ignored (after)'
        if options['before'] and dt >= options['before']:
            return 'ignored (before)'

        result = 'ignored (user id not in DB)'
        if user_id not in self.missing_user_ids:
            try:
                result = souvenez(user_id, dt, ratelimit=options['ratelimit'],
                                  check_duplicate=not options.get('no_check'))
            except IntegrityError:
                if get_user_model().objects.filter(id=user_id).exists():
                    raise
                self.stderr.write("user id {} not in DB\n".format(user_id))
                self.missing_user_ids.add(user_id)
        return result

    def hack_user(self, user_id, date_joined):
        """
        Hack non-existent user id into the DB. This is for running on devstack
        with logs from a deployed host.
        """
        User = get_user_model()

        if self.hacked_user_ids is None:
            self.hacked_user_ids = set(User.objects.values_list('id', flat=True))

        if user_id not in self.hacked_user_ids:
            self.stderr.write("hacking user id {}\n".format(user_id))
            User.objects.create(id=user_id,
                                username='hacked-{}'.format(user_id),
                                date_joined=date_joined)
            self.hacked_user_ids.add(user_id)

    def override_cache(self):
        """
        Override the souvenirs rate-limiting cache
        """
        # If souvenirs middleware is running, then it's rate-limiting *current*
        # users while this management command wants to rate-limit *past* users.
        # To keep them separate, override the cache. This is fine because this
        # is a management command running as a separate process, so any changes
        # to settings here are isolated and don't affect the server.
        settings.CACHES['souvenirs'] = {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'souvenirs',
        }
        settings.SOUVENIRS_CACHE_NAME = 'souvenirs'


def check_and_sort_logs(logs):
    if not logs:
        # This path is hard-coded rather than referring to settings because
        # the platform (including devstack) logs through syslog, so the
        # destination paths are configured in rsyslog.
        logs = ['/edx/var/log/tracking']

    # Expand any dirs in list to dir/tracking.log*
    logs = set(itertools.chain.from_iterable([
        [log for log in logs if not os.path.isdir(log)],
        [log for dir in logs if os.path.isdir(dir)
         for log in glob.glob(os.path.join(dir, 'tracking.log*'))],
    ]))

    if not logs:
        raise CommandError("no tracking logs to import")

    # Rotated logs are naturally sorted by filename, but the live tracking.log
    # should always go last.
    logs = sorted(logs, key=lambda s: '{}{}'.format(
        '1' if os.path.basename(s) == 'tracking.log' else '0', s))

    # Make sure all the logs are readable, rather than starting to import and
    # tripping on one later.
    unreadable = [log for log in logs if not os.access(log, os.R_OK)]
    if unreadable:
        raise CommandError("can't read: {}".format(unreadable[0]))

    return logs


def json_records_from(filename):
    """
    Read lines from filename, parsing each as JSON. Generate tuples of (lineno,
    data, exc) where either data or exc will be populated, and the other will
    be None.
    """
    with open(filename) as f:
        if filename.endswith('gz'):
            f = gzip.GzipFile(fileobj=f)
        for lineno, line in enumerate(f):
            # Can't defer try/except to caller, because there's no way to
            # resume the generator.
            try:
                yield lineno, json.loads(line), None
            except Exception as e:
                yield lineno, None, e
