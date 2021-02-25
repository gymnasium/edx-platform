from __future__ import absolute_import, unicode_literals

from django.core.mail import send_mail
from django.utils import timezone
from django.utils.formats import date_format
from tabulate import tabulate
from souvenirs.management.commands._commands import ReportCommand


class Command(ReportCommand):
    help = "Email usage report"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--from', metavar='EMAIL', required=True,
                            help="from address")
        parser.add_argument('emails', nargs='+', metavar='EMAIL',
                            help="to address(es)")

    def handle(self, *args, **options):
        headers, rows = super(Command, self).handle(*args, **options)

        # rows is a generator, need a list to render twice into text and html
        rows = list(rows)

        text = tabulate(rows, headers)
        html = tabulate(rows, headers, tablefmt='html')
        css = 'table {border-collapse: collapse;} table, th, td {border: 1px solid black;}'

        exc = None

        for email in options['emails']:
            try:
                send_mail(
                    from_email=options['from'],
                    recipient_list=[email],
                    subject=('Appsembler usage report for {}'
                             .format(date_format(timezone.now()))),
                    message=text,
                    html_message=('<html><head><style>{}</style></head><body>{}</body></html>'
                                  .format(css, html)),
                    fail_silently=False,
                )
            except Exception as exc:
                pass

        if exc:
            raise exc
