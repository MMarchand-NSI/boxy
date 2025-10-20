from typing import Literal

from .abstract import AbstractCrafter


BackendName = Literal["tkinter", "arcade"]

__all__ = ["AbstractCrafter", "BackendName"]
