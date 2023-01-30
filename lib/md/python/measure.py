import typing
import time

# Metadata
__author__ = 'https://md.land/md'
__version__ = '1.0.0'

__all__ = (
    # Metadata
    '__author__',
    '__version__',
    # Implementation
    'Time',
)


# Implementation
class Time:
    def __init__(
        self,
        start: typing.Optional[float] = None,
        end: typing.Optional[float] = None,
        now: typing.Callable[[], float] = None
    ) -> None:
        self.start = start
        self.end = end
        self._now = now or time.monotonic

    def time(self) -> typing.Optional[float]:
        if self.start is None:
            return None

        return max((self.end or self._now()) - self.start, 0)

    def __enter__(self) -> 'Time':
        self.end = None  # for instance reuse case
        self.start = self._now()
        return self

    def __exit__(self, *exc) -> None:
        self.end = self._now()

    def __repr__(self) -> str:
        return f'Time(start={self.start}, end={self.end})'
