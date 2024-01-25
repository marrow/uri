from functools import partial
from socket import inet_pton, AF_INET6, error as SocketError
from typing import Any, Optional, Union

from .base import ProxyPart


class HostPart(ProxyPart):
    __slots__ = ()

    attribute = "_host"

    def cast(self, value: str) -> str:
        value = value.rstrip(".")  # Remove extraneous "DNS root authority" notation.

        if value.startswith("xn--"):  # Process IDNA - internationalized domain names.
            value = value.encode("ascii").decode("idna")

        return value

    def render(self, obj, value, raw: bool = False) -> str:
        result = super().render(obj, value)

        if result:
            try:
                if not raw:
                    result.encode("ascii")
            except UnicodeEncodeError:
                result = result.encode("idna").decode("ascii")

            try:  # Identify and armour IPv6 address literals.
                inet_pton(AF_INET6, value)
            except SocketError:
                pass
            else:
                result = "[" + result + "]"

        return result

    def __set__(self, obj, value):
        if isinstance(value, bytes):
            value = value.decode("idna")
        elif value.startswith("xn--"):
            value = value.encode("ascii").decode("idna")

        value = value.lower().rstrip(".")

        super().__set__(obj, value)
