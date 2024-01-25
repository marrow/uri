from .base import ProxyPart


class PortPart(ProxyPart):
    __slots__ = ()

    attribute = "_port"
    prefix = ":"
    cast = int
