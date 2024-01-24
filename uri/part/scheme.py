from importlib.metadata import entry_points
from typing import Any, ClassVar, Dict, Optional, Union  # , Self
from re import compile as r, Pattern

from .base import Part
from ..scheme import Scheme


class SchemePart(Part):
    __slots__: tuple = ()  # Do not populate a __dict__ dictionary attribute; only allocate space for these.

    registry: ClassVar[Dict[str, Optional[Scheme]]] = {"": None}  # Singleton cache of Scheme instances, by name.
    suffix: str = ":"  # Protocol suffix when utilized as part of a complete URI; e.g. ':' or '://'.
    valid: Pattern = r(r"[a-z][a-z0-9+.+-]*")  # Protocol/scheme name validated when run without optimization.

    def load(self, plugin: str) -> Scheme:
        """Attempt to retrieve a Scheme for the given named protocol.

        Utilizes a cache, which results in URI utilizing singletons of each named protocol.
        """

        assert self.valid.match(plugin), f"Invalid plugin name: {plugin!r}"
        if plugin in self.registry:
            return self.registry[plugin]  # Short circuit if we've seen this before.

        # If we haven't, attempt to load the explicit Scheme subclass to utilize for this named scheme.
        try:
            result = entry_points(group="uri.scheme")[plugin].load()
        except KeyError:
            result = Scheme(plugin)  # Can't look up by registered name? It's generic.
        else:
            result = result(plugin)  # Otherwise, instantiate the subclass, informing it of its name.

        self.registry[plugin] = result  # Record the instance in a local registry / cache and return it.

        return result

    def render(self, obj, value, raw=False):
        """Render the scheme component of a whole URI."""
        result = super(SchemePart, self).render(obj, value, raw)

        if obj._scheme and obj.scheme.slashed:
            result = result + "//"

        elif not obj._scheme and obj.authority:
            result = "//"

        return result

    def __get__(self, obj: Any, cls: Optional[type] = None) -> Optional[Union["SchemePart", Scheme]]:
        """Accessed as a class attribute, return this instance, otherwise decant a Scheme from the containing object."""

        if obj is None:
            return self
        return None if obj._scheme is None else self.load(obj._scheme)

    def __set__(self, obj: Any, value: Optional[Union[str, bytes]]) -> None:
        """Assign a new named scheme to this URI."""

        if isinstance(value, bytes):
            value = value.decode("ascii")

        if not value:
            obj._scheme = None
            return

        obj._scheme = self.load(value).name  # This gives the plugin registry a chance to normalize the recorded name.
