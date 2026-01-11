from datetime import datetime, timezone


class TimeProvider:
    def now(self) -> datetime:
        return datetime.now()

    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)


time = TimeProvider()
