from django.core.management.base import BaseCommand, CommandError

import logging
import django_rq
from django_rq.management.commands import rqscheduler

scheduler = django_rq.get_scheduler()
log = logging.getLogger(__name__)


def test():
    print("test")

def clear_scheduled_jobs():
    # Delete any existing jobs in the scheduler when the app starts up
    for job in scheduler.get_jobs():
        log.debug("Deleting scheduled job %s", job)
        job.delete()

def register_scheduled_jobs():
    # do your scheduling here
    scheduler.cron(
    '* * * * 1-5',  
    func=test,
    )


class Command(rqscheduler.Command):
    def handle(self, *args, **kwargs):
        # This is necessary to prevent dupes
        clear_scheduled_jobs()
        register_scheduled_jobs()
        super(Command, self).handle(*args, **kwargs)