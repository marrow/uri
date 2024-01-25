from typing import ClassVar, Iterable, Mapping, Optional, Protocol, T, Union, abstractmethod


class Stringy(Protocol):
    """Objects implementing this protocol may be cast to strings by way of `str()`."""

    __slots__ = ()

    @abstractmethod
    def __str__(self) -> str:
        pass


class PathURI(Protocol):
    """Some objects may implement an `as_uri` method which returns a URI instance."""

    __slots__ = ()

    @abstractmethod
    def as_uri(self) -> Optional["URI"]:
        pass


class Linkable(Protocol):
    """Some objects may expose a URI instance by way of `__link__` attribute."""

    __slots__ = ()

    __link__: "URI"


class LinkableMethod(Protocol):
    """The dynamic version of Linkable, where `__link__` is a method similar to `as_uri`."""

    __slots__ = ()

    @abstractmethod
    def __link__(self) -> "URI":
        pass


# Any object that may in some way provide a URI.
URILike = Union[Stringy, PathURI, Linkable, LinkableMethod]
