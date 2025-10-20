from collections import deque
from typing import TypeVar, TypeAlias

T = TypeVar("T")

File: TypeAlias = deque[T]

def creer() -> File[T]:
    return deque()

def est_vide(f: File[T]):
    return len(f) == 0

def enfiler(e: T, f: File[T]):
    f.appendleft(e)

def defiler(f: File[T]) -> T:
    assert not est_vide(f), "La file est vide"
    return f.pop()
