"""Attempt to parse a database "connection string", retrieving the relevant component parts."""

from pytest import fixture

from .. import URI


def parse_dburi(url: str, uppercase: bool = False) -> dict:
    """Parse a given URL or URI string and return the component parts relevant for database connectivity.

    These come in the general UNIX form:

            engine://[user:pass@]host[:port]/database[?options]
    """

    uri = URI(url)

    parts = {
        "engine": str(uri.scheme),
        "name": uri.path.parts[0],
        "host": uri.host,
        "user": uri.user,
        "password": uri.password,
        "port": uri.port,
        "options": uri.query,
    }

    if not uri.scheme:
        del parts["engine"]  # Parity with dj-mongohq-url

    if "," in parts["host"]:
        parts["hosts"] = [i.strip() for i in parts.pop("host").split(",")]

    if uppercase:
        for k in list(parts):
            parts[k.upper()] = parts.pop(k)

    return parts
