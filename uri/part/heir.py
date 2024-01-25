from .base import ProxyPart, GroupPart


class HeirarchicalPart(GroupPart):
    __slots__ = ()

    attributes = ("auth", "host", "port", "path")
