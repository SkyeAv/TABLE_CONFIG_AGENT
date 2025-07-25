__author__ = "Skye Lane Goetz"

from textwrap import dedent


def collapse(x: str) -> str:
    return dedent(x).replace("\n", " ").strip()
