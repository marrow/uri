from .base import GroupPart


class AuthorityPart(GroupPart):
    __slots__ = ()

    attributes = ("auth", "host", "port")
