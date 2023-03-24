import datetime

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomDateFieldListFilter(admin.DateFieldListFilter):

    def __init__(self, *args, **kwargs):
        super(CustomDateFieldListFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.links = (
            (_("Any date"), {}),
            (
                _("Today"),
                {
                    self.lookup_kwarg_since: today,
                    self.lookup_kwarg_until: tomorrow,
                },
            ),
            (
                _("Tomorrow"),
                {
                    self.lookup_kwarg_since: tomorrow,
                    self.lookup_kwarg_until: tomorrow + datetime.timedelta(
                        days=1),
                },
            ),
            (
                _("Next 7 days"),
                {
                    self.lookup_kwarg_since: today,
                    self.lookup_kwarg_until: tomorrow + datetime.timedelta(
                        days=7),
                },
            ),
            (
                _("Next 4 weeks"),
                {
                    self.lookup_kwarg_since: today,
                    self.lookup_kwarg_until: tomorrow + datetime.timedelta(
                        days=28),
                },
            ),
            (
                _("Rest of this year"),
                {
                    self.lookup_kwarg_since: today,
                    self.lookup_kwarg_until: next_year,
                },
            ),
        )
