import datetime
import hashlib
import typing

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger


class Cron:
    def __init__(
        self,
        storage: typing.Any,
        *jobs: tuple[typing.Callable, CronTrigger | DateTrigger, dict[str, typing.Any] | None],
    ) -> None:
        self.scheduler = AsyncIOScheduler(
            timezone=datetime.UTC,
            jobstores={"default": storage},
            job_defaults={
                "coalesce": False,
                "max_instances": 1,
            },
        )

        for func, trigger, kwargs in jobs:
            self.add(func, trigger, kwargs or {})

    def add(
        self,
        func: typing.Callable,
        trigger: CronTrigger | DateTrigger,
        kwargs: dict[str, typing.Any] | None = None,
    ) -> None:
        self.scheduler.add_job(
            func,
            trigger,
            id=hashlib.md5(f"{func.__name__}-{kwargs.__str__()}".encode()).hexdigest(),
            replace_existing=True,
            misfire_grace_time=3600,
            kwargs=kwargs,
        )

    def start(self) -> None:
        self.scheduler.start()

    def shutdown(self) -> None:
        self.scheduler.shutdown()
