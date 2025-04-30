from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Sqlalchemy:
    def __init__(self, dsn: str) -> None:
        self.store = SQLAlchemyJobStore(dsn)
