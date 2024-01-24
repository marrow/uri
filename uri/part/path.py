from pathlib import PurePosixPath as Path
from re import compile as r

from .base import ProxyPart


class PathPart(ProxyPart):
    __slots__ = ()

    attribute = "_path"
    cast = Path
    empty = "/"

    def __get__(self, obj, cls=None):
        value = super(PathPart, self).__get__(obj, cls)

        if value is None:
            value = Path()
            obj._trailing = False

        return value

    def __set__(self, obj, value):
        value = str(value)
        obj._trailing = value.endswith("/")

        if obj.authority and not value.startswith("/"):
            raise ValueError("Can only assign rooted paths to URI with authority.")

        super(PathPart, self).__set__(obj, value)

    def render(self, obj, value, raw=False):
        result = super(PathPart, self).render(obj, value, raw)

        if result is None or result == ".":
            if not obj._host:
                return ""

            return self.empty

        if obj._trailing and not result.endswith("/"):
            result += "/"

        return result
