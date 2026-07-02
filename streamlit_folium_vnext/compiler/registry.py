from __future__ import annotations

from collections.abc import Callable
from typing import Any


class CompilerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[type[Any], Callable[..., Any]] = {}

    def register(self, cls: type[Any], handler: Callable[..., Any]) -> None:
        self._handlers[cls] = handler

    def resolve(self, obj: Any) -> Callable[..., Any] | None:
        for cls in type(obj).__mro__:
            handler = self._handlers.get(cls)
            if handler is not None:
                return handler
        return None
