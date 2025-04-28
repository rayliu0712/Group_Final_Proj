from typing import Callable, Any, Optional, Self
from thorpy.canonical import Element

type Action = Callable[[], Any]


def isoptcall(obj) -> bool:
    return obj is None or callable(obj)


def isstr(obj) -> bool:
    return isinstance(obj, str)


def isoptstr(obj) -> bool:
    return obj is None or isstr(obj)


def istuple3(obj) -> bool:
    return isinstance(obj, tuple) and len(obj) == 3


def isxlist(type_, obj) -> bool:
    return isinstance(obj, list) and all(isinstance(o, type_) for o in obj)


def ise(obj) -> bool:
    return isinstance(obj, Element)


def iselist(obj) -> bool:
    return isxlist(Element, obj)


def isint(obj) -> bool:
    return isinstance(obj, int)


def isintlist(obj) -> bool:
    return isxlist(int, obj)
