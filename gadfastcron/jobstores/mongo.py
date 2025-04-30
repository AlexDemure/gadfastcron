import urllib.parse

from apscheduler.jobstores.mongodb import MongoDBJobStore
from gadfastcron import const


class Mongo:
    def __init__(self, dsn: str) -> None:
        parsed = urllib.parse.urlparse(dsn)
        path = parsed.path.lstrip(const.SYMBOL_FORWARD_SLASH)
        database, collection = path.split(const.SYMBOL_DOT, 1)
        self.store = MongoDBJobStore(
            host=parsed.hostname,
            port=parsed.port,
            username=parsed.username,
            password=parsed.password,
            database=database,
            collection=collection,
        )
