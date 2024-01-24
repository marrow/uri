from .typing import Union, Stringy


class Scheme:
    __slots__ = ("name",)

    slashed = False  # Do NOT include // separator between scheme and remainder.

    def __init__(self, name: Stringy):
        self.name = str(name).strip().lower()

    def __eq__(self, other: "SchemeLike"):
        if isinstance(other, str):
            return self.name == other

        if isinstance(other, self.__class__):
            return self is other

    def __hash__(self) -> int:
        return hash(self.name)

    def __neq__(self, other: "SchemeLike") -> bool:
        return not (self == other)

    def __bytes__(self) -> bytes:
        return self.name.encode("ascii")

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def is_relative(self, uri) -> bool:
        return False


class URLScheme(Scheme):
    __slots__ = ()

    slashed = True  # DO include // separator between scheme and remainder.

    def is_relative(self, uri) -> bool:
        return not uri._host or not uri._path.is_absolute()


SchemeLike = Union[Stringy, Scheme]
